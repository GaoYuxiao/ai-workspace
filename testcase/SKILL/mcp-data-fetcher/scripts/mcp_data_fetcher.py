#!/usr/bin/env python3
"""
MCP Data Fetcher - 通用MCP数据拉取工具
直接通过HTTP调用MCP服务器，无需经过AI/大模型，避免Token消耗

设计理念:
    - MCPClient 只负责协议层面的通信，不关心具体参数格式
    - 参数格式(body_param/query_param等)由调用方决定
    - 调用方可以先通过AI读取MCP工具描述，再组织正确的参数

用法:
    from mcp_data_fetcher import MCPClient, parse_mcp_result
    
    client = MCPClient()  # 自动读取 ~/.cursor/mcp.json
    
    # 日志查询 (POST请求，使用body_param)
    result = client.call_tool("bkmonitor-log", "search_logs", {
        "body_param": {"bk_biz_id": "2", "index_set_id": "322", ...}
    })
    
    # APM应用列表 (GET请求，使用query_param)
    result = client.call_tool("bkmonitor-tracing", "list_apm_applications", {
        "query_param": {"bk_biz_id": "2"}
    })
    
    # 保存结果
    client.save_result(result, "output.json")
"""

import json
import time
import uuid
import requests
import os
import threading
from pathlib import Path
from typing import Dict, Any


class MCPClient:
    """通用MCP SSE客户端 - 只负责协议通信，参数格式由调用方决定"""
    
    def __init__(self, mcp_config_path: str = None):
        """
        初始化
        Args:
            mcp_config_path: mcp.json路径，默认 ~/.cursor/mcp.json
        """
        if mcp_config_path is None:
            mcp_config_path = os.path.expanduser("~/.cursor/mcp.json")
        
        with open(mcp_config_path, 'r') as f:
            self.config = json.load(f)
        
        self.servers = self.config.get("mcpServers", {})
        self.output_dir = os.path.join(os.getcwd(), "bkmonitor-files")
    
    def list_servers(self) -> list:
        """列出可用的SSE类型MCP服务器"""
        return [s for s, c in self.servers.items() if c.get("transport") == "sse"]
    
    def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any], 
                  timeout: int = 60) -> Dict[str, Any]:
        """
        调用MCP工具
        
        Args:
            server_name: MCP服务器名称 (如 bkmonitor-log, bkmonitor-tracing)
            tool_name: 工具名称 (如 search_logs, list_apm_applications)
            arguments: 工具参数 - 格式由调用方决定，直接透传给MCP服务器
            timeout: 超时秒数
        
        Returns:
            MCP工具返回结果
        """
        if server_name not in self.servers:
            raise ValueError(f"服务器 '{server_name}' 不存在。可用: {self.list_servers()}")
        
        server_config = self.servers[server_name]
        if server_config.get("transport") != "sse":
            raise ValueError(f"服务器 '{server_name}' 非SSE类型")
        
        print(f"📡 调用 {server_name}/{tool_name}...")
        
        sse_url = server_config["url"]
        base_headers = server_config.get("headers", {}).copy()
        
        response_data = {"result": None, "error": None}
        endpoint = {"url": None}
        request_id = str(uuid.uuid4())
        
        # 建立SSE连接
        print(f"   连接: {sse_url}")
        sse_headers = base_headers.copy()
        sse_headers.update({"Accept": "text/event-stream", "Cache-Control": "no-cache"})
        
        sse_response = requests.get(sse_url, headers=sse_headers, stream=True, timeout=timeout)
        sse_response.raise_for_status()
        
        def listen_sse():
            """监听SSE事件流 - 正确处理多行数据"""
            event_type = None
            data_buffer = []
            
            for line in sse_response.iter_lines(decode_unicode=True):
                if line is None:
                    continue
                    
                if line == "":
                    # 空行表示事件结束
                    if event_type and data_buffer:
                        full_data = "".join(data_buffer)
                        
                        if event_type == "endpoint":
                            full_data = full_data.strip()
                            if full_data.startswith("/"):
                                from urllib.parse import urlparse
                                p = urlparse(sse_url)
                                endpoint["url"] = f"{p.scheme}://{p.netloc}{full_data}"
                            else:
                                endpoint["url"] = full_data
                        
                        elif event_type == "message":
                            try:
                                msg = json.loads(full_data)
                                if msg.get("id") == request_id:
                                    response_data["error"] = msg.get("error")
                                    response_data["result"] = msg.get("result")
                                    return
                            except json.JSONDecodeError:
                                pass
                    
                    event_type = None
                    data_buffer = []
                
                elif line.startswith("event:"):
                    event_type = line[6:].strip()
                
                elif line.startswith("data:"):
                    data_content = line[5:]
                    if data_content.startswith(" "):
                        data_content = data_content[1:]
                    data_buffer.append(data_content)
                
                else:
                    if data_buffer:
                        data_buffer.append(line)
                
                if response_data["result"] or response_data["error"]:
                    break
        
        listener = threading.Thread(target=listen_sse, daemon=True)
        listener.start()
        
        # 等待endpoint
        for _ in range(50):
            if endpoint["url"]:
                break
            time.sleep(0.1)
        
        if not endpoint["url"]:
            sse_response.close()
            raise Exception("无法获取endpoint")
        
        # 发送JSON-RPC请求
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments}
        }
        
        post_headers = base_headers.copy()
        post_headers["Content-Type"] = "application/json"
        
        print(f"   请求: {tool_name}")
        resp = requests.post(endpoint["url"], json=payload, headers=post_headers, timeout=timeout)
        if resp.status_code not in [200, 202]:
            resp.raise_for_status()
        
        listener.join(timeout=timeout)
        sse_response.close()
        
        if response_data["error"]:
            raise Exception(f"MCP错误: {response_data['error']}")
        if response_data["result"] is None:
            raise Exception("无响应")
        
        print(f"   ✓ 完成")
        return response_data["result"]
    
    def save_result(self, data: Any, filename: str, output_dir: str = None) -> str:
        """
        保存结果到JSON文件
        Args:
            data: 要保存的数据
            filename: 文件名
            output_dir: 输出目录，默认为当前工作目录下的bkmonitor-files
        """
        if output_dir is None:
            output_dir = self.output_dir
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已保存: {filepath}")
        return filepath


def parse_mcp_result(result: Dict) -> Dict:
    """
    解析MCP返回结果，提取实际数据
    MCP返回格式: {"content": [{"type": "text", "text": "JSON字符串"}]}
    """
    try:
        content = result.get("content", [])
        if content and content[0].get("type") == "text":
            text = content[0].get("text", "")
            if text.startswith("{"):
                return json.loads(text)
        return result
    except:
        return result


# ==================== 便捷函数 ====================

def fetch_data(server: str, tool: str, args: Dict, output_name: str = None) -> Dict:
    """
    通用数据获取函数
    Args:
        server: MCP服务器名称
        tool: 工具名称
        args: 参数（需包含正确的body_param或query_param格式）
        output_name: 输出文件名（不含扩展名），为None则不保存
    """
    client = MCPClient()
    result = client.call_tool(server, tool, args)
    
    if output_name:
        filename = f"{output_name}_{time.strftime('%Y%m%d_%H%M%S')}.json"
        client.save_result(result, filename)
    
    return result


# ==================== 示例 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Data Fetcher - 直接拉取观测数据（无需AI Token）")
    print("=" * 60)
    
    client = MCPClient()
    print(f"\n📂 工作目录: {os.getcwd()}")
    print(f"📁 数据保存: ./bkmonitor-files/")
    print(f"🖥️  可用服务: {client.list_servers()}\n")
    
    print("使用示例:")
    print("-" * 60)
    print("""
# 日志查询 (POST请求，使用body_param)
result = client.call_tool("bkmonitor-log", "search_logs", {
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",
        "query_string": "*",
        "start_time": str(int(time.time()) - 300),
        "end_time": str(int(time.time())),
        "limit": "20"
    }
})

# APM应用列表 (GET请求，使用query_param)
result = client.call_tool("bkmonitor-tracing", "list_apm_applications", {
    "query_param": {"bk_biz_id": "2"}
})

# 保存结果
client.save_result(result, "output.json")
""")
