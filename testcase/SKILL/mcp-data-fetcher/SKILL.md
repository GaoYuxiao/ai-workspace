---
name: mcp-data-fetcher
description: 通用MCP大数据下载工具。直接调用MCP服务器拉取海量观测数据（日志、链路、指标、告警等），数据不经过AI，避免Token消耗。使用场景：(1) 用户需要下载大量日志/链路/指标数据时 (2) 用户要求"不走大模型"或"不消耗Token"获取数据时 (3) 用户需要批量拉取蓝鲸监控数据时 (4) 用户提到使用本地MCP配置获取数据时。自动读取用户本地 ~/.cursor/mcp.json 配置和鉴权Token。
---

# MCP Data Fetcher

直接通过HTTP/SSE协议调用MCP服务器，拉取海量观测数据，无需AI中转。

## 工作流程

1. **确认需求** - 确认用户要下载什么数据（日志/APM/指标等）
2. **读取MCP工具描述** - 获取对应MCP工具的参数格式
3. **组织参数** - 根据工具定义组织正确的参数（body_param/query_param）
4. **执行下载** - 运行 `scripts/mcp_data_fetcher.py` 或直接使用 MCPClient
5. **返回结果** - 数据保存到 `./bkmonitor-files/` 目录

## 快速开始

### 方式1: 直接使用MCPClient (推荐)

```python
import sys, os, time
sys.path.append('<skill-path>/scripts')
from mcp_data_fetcher import MCPClient, parse_mcp_result

os.chdir('<user-workspace>')  # 切换到用户工作目录
client = MCPClient()  # 自动读取 ~/.cursor/mcp.json

# 查看可用服务器
print(client.list_servers())
# ['bkmonitor-log', 'bkmonitor-tracing', 'bkmonitor-metrics', ...]

# 调用MCP工具 - 参数格式由MCP工具定义决定
result = client.call_tool("<server-name>", "<tool-name>", {<arguments>})
client.save_result(result, "output.json")
```

### 方式2: 命令行运行

```bash
python <skill-path>/scripts/mcp_data_fetcher.py
```

## 参数格式规则

**关键**: 不同MCP工具有不同的参数格式要求，需先读取工具描述确认：

| 请求类型 | 参数格式 | 示例 |
|---------|---------|------|
| POST请求 | `body_param` | `{"body_param": {"bk_biz_id": "2", ...}}` |
| GET请求 | `query_param` | `{"query_param": {"bk_biz_id": "2"}}` |

## 常用案例

### 案例1: 下载日志数据

```python
end_time = int(time.time())
start_time = end_time - 300  # 最近5分钟

result = client.call_tool("bkmonitor-log", "search_logs", {
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",  # 需先通过list_index_sets获取
        "query_string": "*",
        "start_time": str(start_time),
        "end_time": str(end_time),
        "limit": "100"
    }
})
client.save_result(result, f"logs_{time.strftime('%Y%m%d_%H%M%S')}.json")
```

### 案例2: 下载APM应用列表

```python
result = client.call_tool("bkmonitor-tracing", "list_apm_applications", {
    "query_param": {"bk_biz_id": "2"}
})
client.save_result(result, "apm_apps.json")
```

### 案例3: 下载索引集列表

```python
result = client.call_tool("bkmonitor-log", "list_index_sets", {
    "query_param": {"bk_biz_id": "2"}
})
client.save_result(result, "index_sets.json")
```

## 确定参数格式的流程

当不确定某个MCP工具的参数格式时:

1. 使用Cursor的MCP工具查看工具定义（查看schema中的patternProperties或properties）
2. 如果定义中包含 `body_param` → 使用 `{"body_param": {...}}`
3. 如果定义中包含 `query_param` → 使用 `{"query_param": {...}}`
4. 优先参考用户提供的工具文档或示例

## 输出位置

所有下载的数据文件保存到用户当前工作目录下的 `bkmonitor-files/` 目录：

```
<user-workspace>/
└── bkmonitor-files/
    ├── logs_biz2_322_20251212_171330.json
    ├── apm_apps_biz2_20251212_171400.json
    └── ...
```

## 可用MCP服务器

脚本自动从 `~/.cursor/mcp.json` 读取配置，常见服务器:

| 服务器 | 用途 |
|-------|------|
| bkmonitor-log | 日志查询 |
| bkmonitor-tracing | APM链路追踪 |
| bkmonitor-metrics | 指标查询 |
| bkmonitor-alarm | 告警查询 |
| bkmonitor-dashboard | 仪表盘 |
| bkmonitor-metadata | 元数据 |

## 参考资源

- **脚本**: `scripts/mcp_data_fetcher.py` - 核心数据拉取脚本
- **工具参数**: 见 `references/mcp_tools_guide.md` 了解各工具参数格式
