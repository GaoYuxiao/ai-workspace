# MCP工具参数格式指南

本文档说明各蓝鲸监控MCP工具的参数格式。

## 目录

- [日志服务 (bkmonitor-log)](#日志服务-bkmonitor-log)
- [链路追踪 (bkmonitor-tracing)](#链路追踪-bkmonitor-tracing)
- [指标服务 (bkmonitor-metrics)](#指标服务-bkmonitor-metrics)
- [告警服务 (bkmonitor-alarm)](#告警服务-bkmonitor-alarm)
- [元数据服务 (bkmonitor-metadata)](#元数据服务-bkmonitor-metadata)

---

## 日志服务 (bkmonitor-log)

### list_index_sets - 获取索引集列表

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2"  # 业务ID
    }
}
```

### get_index_set_fields - 获取索引集字段

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2",
        "index_set_id": "322"
    }
}
```

### search_logs - 搜索日志

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",
        "query_string": "*",           # Lucene查询语法
        "start_time": "1702300000",    # Unix时间戳(秒)
        "end_time": "1702386400",
        "limit": "100"
    }
}
```

---

## 链路追踪 (bkmonitor-tracing)

### list_apm_applications - 获取APM应用列表

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2"
    }
}
```

### get_apm_filter_fields - 获取APM过滤字段

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2",
        "app_name": "your-app"
    }
}
```

### search_spans - 搜索Span

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "app_name": "your-app",
        "start_time": "1702300000",
        "end_time": "1702386400",
        "limit": "10",
        "filters": []  # 可选过滤条件
    }
}
```

### get_trace_detail - 获取Trace详情

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "app_name": "your-app",
        "trace_id": "abc123..."
    }
}
```

---

## 指标服务 (bkmonitor-metrics)

### list_time_series_groups - 获取时序组列表

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "page": "1",
        "page_size": "10"
    }
}
```

### execute_range_query - 执行PromQL查询

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "promql": "up{job='prometheus'}",
        "start_time": "1702300000",
        "end_time": "1702386400",
        "step": "1m"
    }
}
```

---

## 告警服务 (bkmonitor-alarm)

### list_alerts - 获取告警列表

**参数格式**: `body_param` (POST)

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "bk_biz_ids": ["2"],  # 注意：需要同时传
        "start_time": "1702300000",
        "end_time": "1702386400",
        "status": ["ABNORMAL"],  # 可选: ABNORMAL, RECOVERED, CLOSED
        "page": "1",
        "page_size": "10"
    }
}
```

### get_alert_info - 获取告警详情

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2",
        "id": "alert-id-123"
    }
}
```

---

## 元数据服务 (bkmonitor-metadata)

### search_spaces - 搜索业务空间

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "space_name": "demo",
        "page": "1",
        "page_size": "10"
    }
}
```

### list_bcs_clusters - 获取BCS集群列表

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2"
    }
}
```

---

## 通用规则

1. **GET请求** → 使用 `query_param`
2. **POST请求** → 使用 `body_param`
3. **时间参数** → Unix时间戳（秒），字符串格式
4. **分页参数** → `page`(从1开始), `page_size`
5. **业务ID** → 字符串格式的 `bk_biz_id`

## 动态计算时间戳

```python
import time
end_time = int(time.time())           # 当前时间
start_time = end_time - 3600          # 1小时前
start_time = end_time - 86400         # 24小时前
start_time = end_time - 300           # 5分钟前
```
