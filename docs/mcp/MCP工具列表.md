# 当前可用的 MCP 工具列表

## 📋 工具概览

根据项目代码和配置，当前可用的 MCP 工具如下：

---

## 1. 蓝鲸监控日志服务 (bkmonitor-log-bkop)

**用途**: 日志查询和多维度分析

### 可用工具：

#### 1.1 `list_index_sets` - 获取索引集列表
- **方法**: GET
- **参数**: `query_param` → `{"bk_biz_id": "2"}`
- **说明**: 获取业务下的所有索引集

#### 1.2 `get_index_set_fields` - 获取索引集字段
- **方法**: GET  
- **参数**: `query_param` → `{"bk_biz_id": "2", "index_set_id": "322"}`
- **说明**: 获取指定索引集的字段列表

#### 1.3 `search_logs` - 搜索日志
- **方法**: POST
- **参数**: `body_param` → 
  ```json
  {
    "bk_biz_id": "2",
    "index_set_id": "322",
    "query_string": "*",
    "start_time": "1702300000",
    "end_time": "1702386400",
    "limit": "100"
  }
  ```
- **说明**: 搜索日志记录

#### 1.4 `analyze_field` - 分析字段分布和统计 ⭐ **核心工具**
- **方法**: POST
- **参数**: `body_param` →
  ```json
  {
    "bk_biz_id": "2",
    "index_set_id": "322",
    "field_name": "level",
    "query_string": "namespace:xxx AND svr:yyy",
    "start_time": "1702300000",
    "end_time": "1702386400",
    "group_by": "true",
    "order_by": "value",
    "limit": "50"
  }
  ```
- **说明**: 多维度分析的核心工具，支持字段分布统计

#### 1.5 `search_index_set_context` - 获取日志上下文
- **方法**: POST
- **参数**: `body_param` →
  ```json
  {
    "bk_biz_id": "2",
    "index_set_id": "322",
    "dtEventTimeStamp": "1702300000000",
    "serverIp": "9.136.132.152",
    "gseIndex": "12345",
    "begin": "0",
    "size": "50"
  }
  ```
- **说明**: 获取指定日志条目的上下文（前后相邻日志）

---

## 2. 蓝鲸监控指标服务 (bkmonitor-metrics-bkop)

**用途**: 监控指标查询（PromQL）

### 可用工具：

#### 2.1 `execute_range_query` - 执行PromQL查询 ⭐ **核心工具**
- **方法**: POST
- **参数**: `body_param` →
  ```json
  {
    "bk_biz_id": "2",
    "promql": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{ip=\"30.189.38.149\"}[1m]))",
    "start_time": "1702300000",
    "end_time": "1702386400",
    "step": "1m"
  }
  ```
- **说明**: 执行PromQL查询，获取时序指标数据

#### 2.2 `list_time_series_groups` - 获取时序组列表
- **方法**: POST
- **参数**: `body_param` →
  ```json
  {
    "bk_biz_id": "2",
    "page": "1",
    "page_size": "10"
  }
  ```
- **说明**: 获取时序组列表

---

## 3. 图表生成服务 (mcp-server-chart)

**用途**: 生成可视化图表

### 可用工具：

#### 3.1 `generate_line_chart` - 生成折线图 ⭐ **常用**
- **说明**: 生成时序折线图，用于展示监控指标趋势
- **参数**: 
  - `data`: 时序数据数组 `[{time: "2024-01-01", value: 10}, ...]`
  - `title`: 图表标题
  - `width`, `height`: 图表尺寸
  - `theme`: 主题（default/academy/dark）

#### 3.2 `generate_bar_chart` - 生成柱状图
- **说明**: 生成柱状图，用于对比数据

#### 3.3 `generate_pie_chart` - 生成饼图
- **说明**: 生成饼图，用于展示比例分布

#### 3.4 其他图表类型
- `generate_area_chart` - 面积图
- `generate_scatter_chart` - 散点图
- `generate_radar_chart` - 雷达图
- `generate_histogram_chart` - 直方图
- 等等...

---

## 4. 本地日志搜索服务 (log-search)

**配置位置**: `mcp_config.json`

**用途**: 本地日志搜索（测试/开发环境）

### 可用工具：

#### 4.1 `search_logs` - 搜索日志
- **参数**:
  - `query`: 搜索关键词（可选）
  - `level`: 日志级别（DEBUG/INFO/WARN/ERROR）
  - `service`: 服务名称
  - `start_time`, `end_time`: 时间范围（ISO格式）
  - `limit`: 返回数量限制（默认100，最大1000）
  - `offset`: 偏移量（分页）

#### 4.2 `get_log_summary` - 获取日志摘要
- **说明**: 获取日志统计摘要信息

---

## 5. 蓝鲸监控仪表盘服务 (bkmonitor-dashboard)

**用途**: Grafana仪表盘管理

### 可用工具：

#### 5.1 `get_dashboard_directory_tree_list` - 获取仪表盘目录树
- **说明**: 获取业务下所有仪表盘的完整目录树结构

#### 5.2 `get_dashboard_detail_by_uid` - 获取仪表盘详情
- **参数**: `dashboard_uid`
- **说明**: 根据UID获取指定仪表盘的详细配置

#### 5.3 `import_dashboard_config` - 导入仪表盘配置 ⭐ **核心工具**
- **参数**:
  ```json
  {
    "configs": {
      "grafana/目录名/仪表盘名.json": "JSON字符串格式的仪表盘配置"
    },
    "bk_biz_id": "业务ID",
    "overwrite": true/false
  }
  ```
- **说明**: 使用IaC方式导入仪表盘配置

---

## 6. 其他蓝鲸监控服务

### 6.1 链路追踪服务 (bkmonitor-tracing)
- `list_apm_applications` - 获取APM应用列表
- `get_apm_filter_fields` - 获取APM过滤字段
- `search_spans` - 搜索Span
- `get_trace_detail` - 获取Trace详情

### 6.2 告警服务 (bkmonitor-alarm)
- `list_alerts` - 获取告警列表
- `get_alert_info` - 获取告警详情

### 6.3 元数据服务 (bkmonitor-metadata)
- `search_spaces` - 搜索业务空间
- `list_bcs_clusters` - 获取BCS集群列表

---

## 📝 使用说明

### 通用规则

1. **GET请求** → 使用 `query_param`
2. **POST请求** → 使用 `body_param`
3. **时间参数** → Unix时间戳（秒），字符串格式
4. **分页参数** → `page`(从1开始), `page_size`
5. **业务ID** → 字符串格式的 `bk_biz_id`

### 时间范围限制

⚠️ **重要**: 
- `analyze_field` 工具的查询时间范围不能超过 1 天（86400秒）
- 如果查询跨度超过 1 天，需要拆分为多个批次

### PromQL 格式规范

蓝鲸监控的PromQL指标格式：

- **主机监控**: `bkmonitor:system:{result_table}:{metric}`
  - 示例: `bkmonitor:system:cpu_summary:usage`
- **容器监控**: `bkmonitor:{metric_name}` (无结果表层级)
  - 示例: `bkmonitor:container_cpu_usage_seconds_total`
- **自定义上报**: `custom:{result_table}:{metric}`
  - 示例: `custom:blueking_report:data_loss_output_total_data_inc`
- **计算平台**: `bkdata:{result_table}:{metric}`
  - 示例: `bkdata:10_bpf_metric_agg:delay_5min_cnt`

---

## 🔍 常用查询示例

### 查询主机CPU使用率
```promql
avg(avg_over_time(bkmonitor:system:cpu_summary:usage{ip="30.189.38.149"}[1m]))
```

### 查询内存使用率
```promql
avg(avg_over_time(bkmonitor:system:mem:pct_used{ip="30.189.38.149"}[1m]))
```

### 查询磁盘使用率
```promql
avg(avg_over_time(bkmonitor:system:disk:in_use{ip="30.189.38.149"}[1m]))
```

### 查询磁盘IO使用率
```promql
avg(avg_over_time(bkmonitor:system:io:util{ip="30.189.38.149"}[1m]))
```

### 查询系统负载
```promql
avg(avg_over_time(bkmonitor:system:system:load:load5{ip="30.189.38.149"}[5m]))
```

---

## 📚 参考文档

- **日志分析**: `skill/log-multi-dimensional-analyzer/references/mcp_tools_guide.md`
- **指标查询**: `skill/log-multi-dimensional-analyzer/references/metrics_query_example.md`
- **MCP工具指南**: `skill/mcp-data-fetcher/references/mcp_tools_guide.md`

---

**最后更新**: 2025-12-19


