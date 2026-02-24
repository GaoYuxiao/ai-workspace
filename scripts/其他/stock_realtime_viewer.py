#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的终端实时看盘工具

功能：
- 在终端里实时刷新显示股票价格、涨跌幅和时间
- 支持一次查看多只股票

数据来源：Yahoo Finance (公开接口，仅供学习测试使用)
"""

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Any


YAHOO_QUOTE_API = "https://query1.finance.yahoo.com/v7/finance/quote"


def fetch_quotes(symbols: List[str]) -> Dict[str, Any]:
    """从 Yahoo Finance 拉取多只股票行情数据。"""
    params = {"symbols": ",".join(symbols)}
    url = f"{YAHOO_QUOTE_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; StockRealtimeViewer/1.0)"
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e}") from e

    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"解析行情数据失败: {e}") from e

    if "quoteResponse" not in parsed or "result" not in parsed["quoteResponse"]:
        raise RuntimeError("行情返回数据格式异常")

    result: Dict[str, Any] = {}
    for item in parsed["quoteResponse"]["result"]:
        symbol = item.get("symbol")
        if not symbol:
            continue
        result[symbol.upper()] = {
            "symbol": symbol.upper(),
            "name": item.get("shortName") or item.get("longName") or "",
            "price": item.get("regularMarketPrice"),
            "change": item.get("regularMarketChange"),
            "change_percent": item.get("regularMarketChangePercent"),
            "currency": item.get("currency"),
            "market_time": item.get("regularMarketTime"),
        }
    return result


def format_ts(ts: Any) -> str:
    """将时间戳格式化成人类可读时间（本地时区）。"""
    if not ts:
        return "-"
    try:
        return dt.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "-"


def clear_screen() -> None:
    """清空终端屏幕。"""
    if sys.platform.startswith("win"):
        import os

        os.system("cls")
    else:
        # ANSI 转义序列清屏 + 光标移动到左上角
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def print_quotes(quotes: Dict[str, Any], symbols: List[str]) -> None:
    """以表格形式打印行情数据。"""
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"实时股票行情  当前时间: {now}")
    print("-" * 80)
    print(
        f"{'代码':<12} {'价格':>12} {'涨跌额':>12} {'涨跌幅':>10} {'货币':>6} {'行情时间':>20}"
    )
    print("-" * 80)

    for s in symbols:
        s_u = s.upper()
        q = quotes.get(s_u)
        if not q:
            print(f"{s_u:<12} {'-':>12} {'-':>12} {'-':>10} {'-':>6} {'-':>20}")
            continue

        price = q.get("price")
        change = q.get("change")
        change_pct = q.get("change_percent")
        currency = q.get("currency") or "-"
        mt = format_ts(q.get("market_time"))

        price_str = f"{price:.3f}" if isinstance(price, (int, float)) else "-"
        change_str = f"{change:+.3f}" if isinstance(change, (int, float)) else "-"
        if isinstance(change_pct, (int, float)):
            change_pct_str = f"{change_pct:+.2f}%"
        else:
            change_pct_str = "-"

        print(
            f"{s_u:<12} {price_str:>12} {change_str:>12} {change_pct_str:>10} {currency:>6} {mt:>20}"
        )
    print("-" * 80)
    print("提示：Ctrl+C 退出；注意该数据仅供参考，不作为任何投资建议。")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="简单的终端实时股票价格查看工具（数据源：Yahoo Finance）"
    )
    parser.add_argument(
        "-s",
        "--symbols",
        type=str,
        help=(
            "股票代码，多个用逗号分隔。例：AAPL,MSFT,TSLA；"
            "A 股示例：000001.SS（上证）、000001.SZ（深证）"
        ),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=5.0,
        help="刷新间隔（秒），默认 5 秒",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if args.symbols:
        symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    else:
        raw = input(
            "请输入要查看的股票代码（多个用英文逗号分隔，例如：AAPL,MSFT,TSLA）：\n> "
        ).strip()
        symbols = [s.strip() for s in raw.split(",") if s.strip()]

    if not symbols:
        print("未提供有效股票代码，程序退出。")
        return 1

    interval = max(1.0, float(args.interval or 5.0))

    try:
        while True:
            try:
                quotes = fetch_quotes(symbols)
                clear_screen()
                print_quotes(quotes, symbols)
            except Exception as e:
                clear_screen()
                print(f"获取行情失败：{e}")
                print("稍后会自动重试，按 Ctrl+C 可退出。")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n已退出。")
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))



