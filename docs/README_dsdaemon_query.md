# dsdaemon 日志查询与统计分析

## 目标
查询 prod-gz-mlog 采集项下包含 "dsdaemon" 的日志，并通过 skill 进行数据统计。

## 使用步骤

### 方法1: 使用 MCP 工具直接查询（推荐）

1. **搜索业务空间**
   ```
   使用工具: mcp_bkmonitor-metadata_search_spaces
   参数: {"query_param": {"space_name": "prod-gz", "page": "1", "page_size": "20"}}
   ```

2. **获取索引集列表**
   ```
   使用工具: mcp_bkmonitor-log_list_index_sets
   参数: {"query_param": {"bk_biz_id": "<从步骤1获取的业务ID>"}}
   ```

3. **搜索日志**
   ```
   使用工具: mcp_bkmonitor-log_search_logs
   参数: {
     "body_param": {
       "bk_biz_id": "<业务ID>",
       "index_set_id": "<索引集ID>",
       "query_string": "dsdaemon",
       "start_time": "<Unix时间戳(秒)>",
       "end_time": "<Unix时间戳(秒)>",
       "limit": "500"
     }
   }
   ```

4. **保存查询结果**
   将查询结果保存为 JSON 文件到 `bkmonitor-files/` 目录

5. **统计分析**
   ```bash
   python3 stat_dsdaemon_logs.py <日志JSON文件>
   ```

### 方法2: 使用完整脚本（需要安装依赖）

如果已安装 requests 等依赖，可以使用 `analyze_dsdaemon_logs.py` 脚本自动完成所有步骤。

## 输出文件

所有结果保存在 `bkmonitor-files/` 目录：
- `dsdaemon_logs_YYYYMMDD_HHMMSS.json` - 原始日志数据
- `dsdaemon_stats_YYYYMMDD_HHMMSS.json` - 统计结果（JSON格式）
- `dsdaemon_report_YYYYMMDD_HHMMSS.txt` - 统计报告（文本格式）

## 统计内容

- 总日志数
- 时间范围
- 日志级别分布
- 容器/服务分布
- 错误统计
- 消息关键词统计

## 注意事项

- 时间范围不能超过 24 小时，如需查询更长时间，需分批查询
- 查询结果会自动保存，不会直接输出到控制台
- 统计结果会同时保存为 JSON 和文本报告两种格式
