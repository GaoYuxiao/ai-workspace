# bklog-bkop MCP 工具使用指南

本文档说明如何使用 bklog-bkop MCP 工具进行日志多维度分析。

## 可用工具

### 1. list_index_sets - 获取索引集列表

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2"  # 业务ID
    }
}
```

**返回**: 索引集列表，包含 `index_set_id`、`index_set_name` 等信息

### 2. get_index_set_fields - 获取索引集字段

**参数格式**: `query_param` (GET)

```python
{
    "query_param": {
        "bk_biz_id": "2",
        "index_set_id": "322"
    }
}
```

**返回**: 字段列表，包含字段名、类型、描述等信息

### 3. search_logs - 搜索日志

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

**返回**: 日志记录列表

### 4. analyze_field - 分析字段分布和统计

**参数格式**: `body_param` (POST)

这是多维度分析的核心工具。

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",
        "field_name": "level",          # 要分析的字段名
        "query_string": "namespace:xxx AND svr:yyy",  # 过滤条件
        "start_time": "1702300000",     # Unix时间戳(秒)
        "end_time": "1702386400",
        "group_by": "true",             # 是否按字段值分组
        "order_by": "value",            # 排序方式: "value" 或 "time"
        "limit": "50"                   # 返回数量限制
    }
}
```

**重要参数说明**:
- `group_by`: `true` 表示按字段值分组统计，`false` 表示整体统计
- `order_by`: `"value"` 按统计值降序（用于 Top K），`"time"` 按时间排序（用于时间序列）
- `limit`: 限制返回的分组数量
- `query_string`: 支持 Lucene 查询语法，可以组合多个过滤条件

**返回格式**:
```json
{
    "data": {
        "list": [
            {
                "name": "ERROR",    # 字段值
                "value": 150        # 统计数量
            },
            {
                "name": "WARN",
                "value": 80
            }
        ]
    }
}
```

### 5. search_index_set_context - 获取日志上下文

**参数格式**: `body_param` (POST)

用于获取指定日志条目的上下文（前后相邻日志）。

```python
{
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",
        "dtEventTimeStamp": "1702300000000",  # 日志时间戳(毫秒)
        "serverIp": "9.136.132.152",
        "gseIndex": "12345",
        "begin": "0",                  # 滚动偏移，正数向前，负数向后
        "size": "50"                   # 返回数量
    }
}
```

## 多维度分析工作流

### 场景1: 按 file_name 分组，按 level 拆分

```python
# 步骤1: 获取所有 file_name 值
result1 = analyze_field(
    field_name="file_name",
    query_string="namespace:xxx AND svr:yyy",
    group_by="true",
    order_by="value"
)

# 步骤2: 对每个 file_name，分析 level 分布
for file_name in result1["data"]["list"]:
    result2 = analyze_field(
        field_name="level",
        query_string=f"namespace:xxx AND svr:yyy AND file_name:{file_name['name']}",
        group_by="true",
        order_by="value"
    )
    # 处理结果...
```

### 场景2: 多维度组合分析

```python
# 先按 namespace 分组
namespaces = analyze_field(field_name="namespace", ...)

# 对每个 namespace，按 svr 分组
for ns in namespaces:
    svrs = analyze_field(
        field_name="svr",
        query_string=f"namespace:{ns['name']}",
        ...
    )
    
    # 对每个 svr，按 level 拆分
    for svr in svrs:
        levels = analyze_field(
            field_name="level",
            query_string=f"namespace:{ns['name']} AND svr:{svr['name']}",
            ...
        )
```

## 查询字符串语法

支持 Lucene 查询语法：

- **精确匹配**: `field:value`
- **多值匹配**: `field:(value1 OR value2)`
- **范围查询**: `field:[value1 TO value2]`
- **通配符**: `field:value*`
- **逻辑组合**: `field1:value1 AND field2:value2`

## 时间范围限制

⚠️ **重要**: `analyze_field` 工具的查询时间范围不能超过 1 天（86400秒）。

如果查询跨度超过 1 天，需要：
1. 将查询拆分为多个批次，每批 ≤ 24 小时
2. 分别查询每批数据
3. 合并结果

## 常见字段名

根据日志类型不同，常见字段包括：

- **通用字段**: `level`, `timestamp`, `message`, `serverIp`
- **容器/K8s**: `namespace`, `pod`, `container`, `svr`
- **应用日志**: `file_name`, `service`, `module`, `app`
- **自定义字段**: 根据实际业务定义

## 最佳实践

1. **先获取字段列表**: 使用 `get_index_set_fields` 确认字段存在
2. **合理设置 limit**: 根据实际需求设置，避免返回过多数据
3. **使用过滤条件**: 通过 `query_string` 缩小查询范围，提高效率
4. **分批查询**: 对于大时间范围，拆分为多个小批次
5. **缓存结果**: 对于重复查询，可以缓存中间结果


