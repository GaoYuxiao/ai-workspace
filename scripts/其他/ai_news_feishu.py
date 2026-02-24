#!/usr/bin/env python3
"""
Daily AI news aggregator with Feishu webhook push.

Features:
- Pulls from multiple AI-focused sources (official, community, CN media)
- Filters by recency and AI keywords
- Deduplicates by link
- Sends a Feishu "post" message via incoming webhook

Usage:
  FEISHU_WEBHOOK=https://open.feishu.cn/... python ai_news_feishu.py --once
  FEISHU_WEBHOOK=... FEISHU_SECRET=xxx TZ=Asia/Shanghai \
    python ai_news_feishu.py --lookback-hours 36 --max-per-section 6

Schedule (macOS cron example):
  0 8 * * * /usr/bin/env TZ=Asia/Shanghai /usr/local/bin/python3 \
    /Users/yuxiaogao/cursor/日志AI特性/ai_news_feishu.py >> /tmp/ai_news_feishu.log 2>&1
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Sequence

import feedparser
import httpx
from html import unescape
import re

TZ = timezone(timedelta(hours=8))  # Asia/Shanghai
AI_KEYWORDS = ["ai", "人工智能", "大模型", "llm", "生成式", "gpt", "openai", "claude", "gemini", "代理", "agent", "自治体"]
RSSHUB_BASE = os.getenv("RSSHUB_BASE", "https://rsshub.app").rstrip("/")
VERIFY_SSL = not bool(os.getenv("INSECURE_SKIP_VERIFY", "").lower() in ("1", "true", "yes"))


@dataclass
class Source:
    category: str  # official | community | cn
    name: str
    url: str
    max_items: int = 8
    keyword_filter: bool = False  # apply AI keyword filter to this source


SOURCES: Sequence[Source] = [
    # 官方/厂商（优先直接源，部分使用 RSSHub，可通过 RSSHUB_BASE 覆盖）
    Source("official", "OpenAI Blog", f"{RSSHUB_BASE}/openai/blog", 6),
    Source("official", "Google AI", "https://blog.google/technology/ai/rss/", 6),
    Source("official", "DeepMind", f"{RSSHUB_BASE}/deepmind/blog", 4),
    Source("official", "Anthropic", f"{RSSHUB_BASE}/anthropic/blog", 4, True),
    Source("official", "Mistral AI", f"{RSSHUB_BASE}/mistralai/blog", 4),
    Source("official", "Meta AI", f"{RSSHUB_BASE}/facebook/ai", 4),
    Source("official", "Hugging Face", "https://huggingface.co/blog/feed.xml", 4),
    Source("official", "LangChain Blog", "https://blog.langchain.dev/rss/", 4, True),
    # MCP / Agent 专栏
    Source("agent", "Model Context Protocol Releases", "https://github.com/modelcontextprotocol/servers/releases.atom", 4, True),
    Source("agent", "AgentOps Newsletter", f"{RSSHUB_BASE}/agentops/newsletter", 4, True),
    Source("agent", "AutoGPT Blog", f"{RSSHUB_BASE}/autogpt/blog", 4, True),
    # 社区/媒体
    Source("community", "Hacker News (AI/LLM)", "https://hnrss.org/newest?q=ai+llm", 6, True),
    Source("community", "ArXiv cs.AI", "https://export.arxiv.org/rss/cs.AI", 4, True),
    Source("community", "InfoQ AI", f"{RSSHUB_BASE}/infoq/ai", 6, True),
    Source("community", "TechCrunch AI", "https://techcrunch.com/tag/ai/feed/", 6, True),
    # 国内渠道（关键词过滤）
    Source("cn", "36氪", "https://36kr.com/feed", 6, True),
    Source("cn", "少数派", "https://sspai.com/feed", 6, True),
    Source("cn", "钛媒体", "https://www.tmtpost.com/rss.xml", 6, True),
    Source("cn", "量子位", f"{RSSHUB_BASE}/qbitai", 6, True),
    # 小红书等自媒体：需 RSS 代理，支持 RSSHUB_BASE
    Source("cn", "小红书AI精选", f"{RSSHUB_BASE}/xiaohongshu/user/652968844e30370001784c3a", 4, True),
]


def parse_date(entry) -> datetime:
    if "published_parsed" in entry and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    if "updated_parsed" in entry and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
    if "published" in entry:
        try:
            return parsedate_to_datetime(entry.published)
        except Exception:
            pass
    return datetime.now(timezone.utc)


def clip_title(title: str, max_len: int = 120) -> str:
    t = (title or "").strip().replace("\n", " ")
    return t if len(t) <= max_len else t[: max_len - 1] + "…"


def looks_ai_related(title: str) -> bool:
    lower = title.lower()
    return any(k in lower for k in AI_KEYWORDS)


async def fetch_source(client: httpx.AsyncClient, source: Source) -> List[Dict]:
    try:
        resp = await client.get(source.url, timeout=15.0)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[warn] fetch failed: {source.name}: {exc}")
        return await fetch_html_fallback(client, source)

    feed = feedparser.parse(resp.text)
    items = []
    for entry in feed.entries:
        title = clip_title(entry.get("title", ""))
        link = entry.get("link", "").strip()
        if not title or not link:
            continue
        if source.keyword_filter and not looks_ai_related(title):
            continue
        published = parse_date(entry)
        items.append(
            {
                "title": title,
                "link": link,
                "published": published,
                "source": source.name,
                "category": source.category,
            }
        )

    # 如果 feed 为空，尝试 HTML fallback
    if not items:
        return await fetch_html_fallback(client, source)

    items.sort(key=lambda x: x["published"], reverse=True)
    return items[: source.max_items]


def strip_tags(html: str) -> str:
    # quick and light tag stripper
    text = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.S)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(text).strip()


def extract_links(html: str, domain_keyword: str, path_keyword: str, max_items: int) -> List[Dict]:
    links = []
    for href, inner in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, flags=re.I | re.S):
        if domain_keyword not in href and href.startswith("/"):
            href = f"https://{domain_keyword}{href}"
        if domain_keyword not in href:
            continue
        if path_keyword not in href:
            continue
        title = strip_tags(inner)
        if not title:
            continue
        links.append({"title": clip_title(title), "link": href})
    # dedupe by link
    seen = set()
    uniq = []
    for x in links:
        if x["link"] in seen:
            continue
        seen.add(x["link"])
        uniq.append(x)
        if len(uniq) >= max_items:
            break
    return uniq


async def fetch_html_fallback(client: httpx.AsyncClient, source: Source) -> List[Dict]:
    fallback_map = {
        "OpenAI Blog": ("openai.com", "/blog"),
        "Anthropic": ("anthropic.com", "/news"),
        "DeepMind": ("deepmind.google", "/blog"),
        "Meta AI": ("ai.meta.com", "/blog"),
        "Mistral AI": ("mistral.ai", "/news"),
    }
    if source.name not in fallback_map:
        return []
    domain, path_kw = fallback_map[source.name]
    url = f"https://{domain}"
    try:
        resp = await client.get(url, timeout=15.0)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[warn] html fallback failed: {source.name}: {exc}")
        return []
    items = extract_links(resp.text, domain, path_kw, source.max_items)
    now = datetime.now(timezone.utc)
    return [
        {
            "title": it["title"],
            "link": it["link"],
            "published": now,
            "source": source.name,
            "category": source.category,
        }
        for it in items
    ]


def dedupe(items: Sequence[Dict]) -> List[Dict]:
    seen = set()
    uniq = []
    for item in items:
        key = item["link"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(item)
    return uniq


def filter_recent(items: Sequence[Dict], lookback_hours: int) -> List[Dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    return [i for i in items if i["published"] >= cutoff]


def build_feishu_post(sections: Dict[str, List[Dict]]) -> Dict:
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    content_rows = []

    header = f"AI 早报 · {today}"
    content_rows.append([{"tag": "text", "text": header}])

    labels = {
        "official": "官方发布 / 厂商",
        "agent": "MCP / Agent / DevTools",
        "community": "社区 / 媒体",
        "cn": "国内优质文章",
    }

    for key in ("official", "agent", "community", "cn"):
        items = sections.get(key, [])
        if not items:
            continue
        content_rows.append([{"tag": "text", "text": labels.get(key, key)}])
        for item in items:
            # 单行：标题 + 链接，仅保留核心信息
            content_rows.append(
                [
                    {"tag": "text", "text": "• "},
                    {"tag": "a", "text": item["title"], "href": item["link"]},
                ]
            )

    if not any(sections.values()):
        content_rows.append([{"tag": "text", "text": "最近未获取到 AI 相关新闻。"}])

    return {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": header,
                    "content": content_rows,
                }
            }
        },
    }


def add_sign(payload: Dict, secret: str) -> Dict:
    if not secret:
        return payload
    timestamp = str(int(time.time()))
    sign_str = f"{timestamp}\n{secret}"
    sign = base64.b64encode(hmac.new(sign_str.encode(), digestmod=hashlib.sha256).digest()).decode()
    payload["timestamp"] = timestamp
    payload["sign"] = sign
    return payload


async def push_feishu(webhook: str, secret: str, payload: Dict) -> None:
    data = add_sign(payload, secret)
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(webhook, content=json.dumps(data), headers={"Content-Type": "application/json"})
        if resp.status_code >= 300:
            print(f"[error] Feishu push failed: {resp.status_code} {resp.text}")
        else:
            print("[info] Feishu push success")


async def collect_news(lookback_hours: int) -> Dict[str, List[Dict]]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [fetch_source(client, s) for s in SOURCES]
        results = await asyncio.gather(*tasks)

    flat = [item for sub in results for item in sub]
    flat = dedupe(flat)
    flat = filter_recent(flat, lookback_hours)

    sections: Dict[str, List[Dict]] = {"official": [], "community": [], "cn": []}
    for item in flat:
        sections.setdefault(item["category"], []).append(item)

    # keep each section sorted and limited
    for key in sections:
        sections[key].sort(key=lambda x: x["published"], reverse=True)
        sections[key] = sections[key][:12]
    return sections


async def main() -> None:
    parser = argparse.ArgumentParser(description="AI news -> Feishu")
    parser.add_argument("--lookback-hours", type=int, default=int(os.getenv("NEWS_LOOKBACK_HOURS", "36")))
    parser.add_argument("--max-per-section", type=int, default=12, help="hard cap per section before sending")
    parser.add_argument("--dry-run", action="store_true", help="only print, do not push")
    args = parser.parse_args()

    webhook = os.getenv("FEISHU_WEBHOOK", "").strip()
    secret = os.getenv("FEISHU_SECRET", "").strip()
    if not webhook and not args.dry_run:
        raise SystemExit("FEISHU_WEBHOOK is required unless --dry-run is set")

    sections = await collect_news(args.lookback_hours)
    for key in sections:
        sections[key] = sections[key][: args.max_per_section]

    payload = build_feishu_post(sections)

    if args.dry_run or not webhook:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    await push_feishu(webhook, secret, payload)


if __name__ == "__main__":
    asyncio.run(main())

