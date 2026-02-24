#!/usr/bin/env python3
"""
日志检索 MCP 服务器
处理大量日志输出的解决方案：
1. 分页机制 - 支持 limit 和 offset
2. 流式传输 - 使用 MCP streaming
3. 智能过滤 - 时间范围、级别、关键词
4. 结果摘要 - 统计信息和摘要
5. 异步处理 - 大量数据的异步任务
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import Any, Optional, Sequence
from pathlib import Path

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
        LoggingLevel,
    )
except ImportError:
    print("Error: MCP package not installed. Please run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


# 日志存储模拟（实际应该连接真实的日志系统）
class LogStore:
    """日志存储抽象类，可以对接 Elasticsearch、Loki、文件系统等"""
    
    def __init__(self):
        # 模拟日志数据
        self.logs = []
        self._init_mock_data()
    
    def _init_mock_data(self):
        """初始化模拟数据"""
        levels = ["INFO", "WARN", "ERROR", "DEBUG"]
        services = ["api", "database", "cache", "worker"]
        for i in range(10000):
            self.logs.append({
                "id": i,
                "timestamp": (datetime.now() - timedelta(minutes=i)).isoformat(),
                "level": levels[i % len(levels)],
                "service": services[i % len(services)],
                "message": f"Log entry {i}: Processing request {i*100}",
                "details": {
                    "request_id": f"req-{i}",
                    "user_id": i % 1000,
                    "duration_ms": (i % 1000) + 10
                }
            })
    
    async def search(
        self,
        query: str = "",
        level: Optional[str] = None,
        service: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict:
        """
        搜索日志
        
        Args:
            query: 搜索关键词
            level: 日志级别过滤
            service: 服务名称过滤
            start_time: 开始时间 (ISO format)
            end_time: 结束时间 (ISO format)
            limit: 返回数量限制
            offset: 偏移量（分页）
        
        Returns:
            包含 logs 和 total 的字典
        """
        # 模拟搜索延迟
        await asyncio.sleep(0.1)
        
        filtered = self.logs
        
        # 应用过滤条件
        if level:
            filtered = [log for log in filtered if log["level"] == level]
        
        if service:
            filtered = [log for log in filtered if log["service"] == service]
        
        if query:
            filtered = [
                log for log in filtered
                if query.lower() in log["message"].lower()
            ]
        
        if start_time:
            filtered = [
                log for log in filtered
                if log["timestamp"] >= start_time
            ]
        
        if end_time:
            filtered = [
                log for log in filtered
                if log["timestamp"] <= end_time
            ]
        
        total = len(filtered)
        
        # 分页
        paginated = filtered[offset:offset + limit]
        
        return {
            "logs": paginated,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    
    async def get_summary(
        self,
        query: str = "",
        level: Optional[str] = None,
        service: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> dict:
        """获取日志摘要统计"""
        result = await self.search(
            query=query,
            level=level,
            service=service,
            start_time=start_time,
            end_time=end_time,
            limit=0,  # 只获取总数
            offset=0
        )
        
        # 获取实际日志进行统计
        search_result = await self.search(
            query=query,
            level=level,
            service=service,
            start_time=start_time,
            end_time=end_time,
            limit=1000,  # 获取足够的数据进行统计
            offset=0
        )
        
        logs = search_result["logs"]
        
        # 统计信息
        level_counts = {}
        service_counts = {}
        error_count = 0
        
        for log in logs:
            level_counts[log["level"]] = level_counts.get(log["level"], 0) + 1
            service_counts[log["service"]] = service_counts.get(log["service"], 0) + 1
            if log["level"] == "ERROR":
                error_count += 1
        
        return {
            "total": result["total"],
            "level_distribution": level_counts,
            "service_distribution": service_counts,
            "error_count": error_count,
            "error_rate": f"{(error_count / len(logs) * 100):.2f}%" if logs else "0%"
        }


# 全局日志存储实例
log_store = LogStore()

# 创建 MCP 服务器
server = Server("log-search-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="search_logs",
            description="搜索日志。支持分页、过滤和关键词搜索。对于大量日志，建议先使用 get_log_summary 获取摘要，然后使用分页查询。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（可选）"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                        "description": "日志级别过滤（可选）"
                    },
                    "service": {
                        "type": "string",
                        "description": "服务名称过滤（可选）"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "开始时间，ISO 格式，例如: 2024-01-01T00:00:00（可选）"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "结束时间，ISO 格式（可选）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "返回数量限制（默认 100，最大 1000）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "offset": {
                        "type": "integer",
                        "description": "偏移量，用于分页（默认 0）",
                        "default": 0,
                        "minimum": 0
                    }
                }
            }
        ),
        Tool(
            name="get_log_summary",
            description="获取日志摘要统计信息。在搜索大量日志前，建议先调用此工具了解数据概况。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（可选）"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                        "description": "日志级别过滤（可选）"
                    },
                    "service": {
                        "type": "string",
                        "description": "服务名称过滤（可选）"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "开始时间，ISO 格式（可选）"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "结束时间，ISO 格式（可选）"
                    }
                }
            }
        ),
        Tool(
            name="stream_logs",
            description="流式传输日志。用于处理大量日志，逐批返回结果。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（可选）"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                        "description": "日志级别过滤（可选）"
                    },
                    "service": {
                        "type": "string",
                        "description": "服务名称过滤（可选）"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "开始时间，ISO 格式（可选）"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "结束时间，ISO 格式（可选）"
                    },
                    "batch_size": {
                        "type": "integer",
                        "description": "每批返回的数量（默认 100）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 500
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""
    
    if name == "search_logs":
        # 限制最大返回数量
        limit = min(arguments.get("limit", 100), 1000)
        offset = arguments.get("offset", 0)
        
        result = await log_store.search(
            query=arguments.get("query", ""),
            level=arguments.get("level"),
            service=arguments.get("service"),
            start_time=arguments.get("start_time"),
            end_time=arguments.get("end_time"),
            limit=limit,
            offset=offset
        )
        
        # 格式化输出
        logs_text = "\n".join([
            f"[{log['timestamp']}] {log['level']} {log['service']}: {log['message']}"
            for log in result["logs"]
        ])
        
        summary = f"""
搜索结果摘要:
- 总数: {result['total']}
- 当前页: {offset + 1} - {min(offset + limit, result['total'])}
- 是否还有更多: {'是' if result['has_more'] else '否'}

日志内容:
{logs_text}

提示: 如果结果很多，可以使用 offset 参数进行分页查询。
"""
        
        return [TextContent(type="text", text=summary)]
    
    elif name == "get_log_summary":
        summary = await log_store.get_summary(
            query=arguments.get("query", ""),
            level=arguments.get("level"),
            service=arguments.get("service"),
            start_time=arguments.get("start_time"),
            end_time=arguments.get("end_time")
        )
        
        summary_text = f"""
日志摘要统计:
- 总日志数: {summary['total']}
- 错误数量: {summary['error_count']}
- 错误率: {summary['error_rate']}

日志级别分布:
{json.dumps(summary['level_distribution'], indent=2, ensure_ascii=False)}

服务分布:
{json.dumps(summary['service_distribution'], indent=2, ensure_ascii=False)}

建议: 如果日志数量很大，建议使用分页查询或流式传输。
"""
        
        return [TextContent(type="text", text=summary_text)]
    
    elif name == "stream_logs":
        batch_size = arguments.get("batch_size", 100)
        offset = 0
        all_results = []
        
        # 先获取总数
        first_batch = await log_store.search(
            query=arguments.get("query", ""),
            level=arguments.get("level"),
            service=arguments.get("service"),
            start_time=arguments.get("start_time"),
            end_time=arguments.get("end_time"),
            limit=batch_size,
            offset=0
        )
        
        total = first_batch["total"]
        all_results.extend(first_batch["logs"])
        
        # 流式获取剩余数据
        offset = batch_size
        while offset < total:
            batch = await log_store.search(
                query=arguments.get("query", ""),
                level=arguments.get("level"),
                service=arguments.get("service"),
                start_time=arguments.get("start_time"),
                end_time=arguments.get("end_time"),
                limit=batch_size,
                offset=offset
            )
            all_results.extend(batch["logs"])
            offset += batch_size
            
            # 避免一次性返回太多，这里只返回前几批
            if len(all_results) >= 1000:
                break
        
        logs_text = "\n".join([
            f"[{log['timestamp']}] {log['level']} {log['service']}: {log['message']}"
            for log in all_results
        ])
        
        result_text = f"""
流式传输结果:
- 总日志数: {total}
- 已返回: {len(all_results)}
- 批次大小: {batch_size}

日志内容:
{logs_text}

注意: 为了性能考虑，流式传输最多返回 1000 条日志。如需更多，请使用分页查询。
"""
        
        return [TextContent(type="text", text=result_text)]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> list[Resource]:
    """列出可用的资源"""
    return [
        Resource(
            uri="log://summary",
            name="日志摘要",
            description="获取日志系统的摘要信息",
            mimeType="application/json"
        )
    ]


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

