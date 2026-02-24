---
name: log-multi-dimensional-analyzer
description: 基于 bklog-bkop MCP 工具的日志多维度分析技能。支持用户自定义过滤条件、分组字段和拆分维度，实现灵活的日志数据多维度统计分析。使用场景：(1) 用户需要对日志进行多维度分析时 (2) 用户需要按某个字段分组并按另一个字段拆分统计时 (3) 用户需要自定义分析维度时 (4) 用户提到"按XX分组，按YY拆分"或"多维度分析"时。
---

# 日志多维度分析器

基于蓝鲸监控日志服务 (bklog-bkop) MCP 工具，提供灵活的日志多维度分析能力。

## 核心能力

1. **自定义过滤条件** - 支持通过多个字段组合过滤（如 namespace、svr、pod 等）
2. **自定义分组字段** - 按指定字段分组统计（如 file_name、service、module 等）
3. **自定义拆分维度** - 在每个分组内按指定维度拆分（如 level、status、error_type 等）
4. **多层级分析** - 支持多维度组合分析，生成详细的统计报告
5. **指标关联查询** - 自动识别日志分析结果中的资源（如 pod、namespace、service 等），查询对应的监控指标
6. **可视化图表生成** - 通过 chart MCP 工具将指标查询结果生成为图片，嵌入到分析报告中

## 执行流程

技能按照以下顺序执行：

1. **日志分析** - 使用 `bkmonitor-log-bkop` MCP 工具进行日志多维度分析
2. **识别指标信息和资源信息** - 判断是否为有效指标信息或资源信息（主机环境查看IP，容器环境查看K8S）
2. **指标获取** - 使用 `bkmonitor-metrics-bkop` MCP 工具查询相关监控指标
3. **折线图绘制** - 使用 `mcp-server-chart` MCP 工具生成时序折线图

## 工作流程

### 1. 理解用户需求

用户可能以以下方式表达需求：
- "通过 namespace、svr 过滤，以 file_name 为键值，按日志级别进行维度拆分"
- "按服务分组，统计每个服务的错误级别分布"
- "分析不同模块的日志级别分布情况"

提取关键信息：
- **过滤条件** (filter_fields): 如 `{"namespace": "xxx", "svr": "yyy"}`
- **分组字段** (group_by_field): 如 `"file_name"`
- **拆分字段** (split_by_field): 如 `"level"`
- **时间范围**: 开始时间和结束时间（Unix 时间戳，秒）

### 2. 获取索引集信息

在执行分析前，先获取索引集字段信息，验证字段是否存在：

```python
# 使用 MCP 工具获取字段列表
fields_result = mcp_bkmonitor-log-bkop_get_index_set_fields({
    "query_param": {
        "bk_biz_id": "2",
        "index_set_id": "322"
    }
})
```

### 3. 执行多维度分析

使用 `analyze_field` 工具进行多维度分析：

**步骤1**: 获取分组字段的所有值

```python
# 获取所有 file_name 值（Top 100）
group_values = mcp_bkmonitor-log-bkop_analyze_field({
    "body_param": {
        "bk_biz_id": "2",
        "index_set_id": "322",
        "field_name": "file_name",  # 分组字段
        "query_string": "namespace:xxx AND svr:yyy",  # 过滤条件
        "start_time": str(start_time),
        "end_time": str(end_time),
        "group_by": "true",
        "order_by": "value",
        "limit": "100"
    }
})
```

**步骤2**: 对每个分组值，分析拆分字段的分布

```python
results = {}
for group_item in group_values["data"]["list"]:
    group_value = group_item["name"]
    
    # 分析该分组下的拆分字段分布
    split_result = mcp_bkmonitor-log-bkop_analyze_field({
        "body_param": {
            "bk_biz_id": "2",
            "index_set_id": "322",
            "field_name": "level",  # 拆分字段
            "query_string": f"namespace:xxx AND svr:yyy AND file_name:{group_value}",
            "start_time": str(start_time),
            "end_time": str(end_time),
            "group_by": "true",
            "order_by": "value",
            "limit": "50"
        }
    })
    
    results[group_value] = split_result["data"]["list"]
```

### 4. 识别并查询相关指标

当分析结果中包含可识别的资源（如 pod、namespace、service、host 等）时，自动查询对应的监控指标：

**步骤1**: 识别资源信息
- 从日志分析结果中提取资源标识（如 pod 名称、namespace、主机 IP 等）
- 根据资源类型确定需要查询的指标类型

**步骤2**: 构建 PromQL 查询
- 根据资源类型和指标类型构建 PromQL 查询语句
- 使用 `bkmonitor-metrics-bkop` MCP 工具的 `execute_range_query` 执行查询

**步骤3**: 生成指标图表
- 使用 `mcp-server-chart` MCP 工具将指标数据可视化
- 调用 `generate_line_chart` 生成时间序列折线图
- 图表自动保存为图片文件，嵌入到分析报告中

### 5. 生成分析报告（自动生成图表和时序指标）

将分析结果格式化为易读的报告：

- **文本格式**: 适合控制台输出
- **Markdown 格式**: 适合文档和报告，**自动生成并嵌入图表**
- **JSON 格式**: 适合程序处理

报告包含：
- **简洁的统计概览**（合并显示，避免重复）
- **详细分析表格**（统一表格格式，一目了然）
- **错误类型分布**
- **时序指标图表**（折线图，显示指标随时间变化）
- **指标统计表格**（合并显示所有指标的统计信息）

**优化特点**：
- ✅ 结构清晰，避免重复内容
- ✅ 使用表格统一展示，便于对比
- ✅ 图表自动生成并嵌入
- ✅ 统计信息合并显示，不冗余

**自动图表生成规则**：


1. **时序指标图表**：
   - **自动资源识别**：从 `filter_fields` 中识别资源（如 `serverIp`、`ip`、`host`、`namespace`、`pod` 等）
   - **自动指标查询**：如果识别到主机IP、容器环境时，自动查询以下时序指标：
     - CPU使用率
     - 内存使用率
     - 磁盘使用率
     - 磁盘IO使用率
     - 系统负载
   - **自动图表生成**：为每个指标生成近15分钟的时序折线图，显示指标随时间的变化趋势
   - **智能回退**：即使没有从日志分析中识别到资源，也会尝试从 `filter_fields` 或分组结果中查找IP地址，并查询主机指标

2. **图表保存和嵌入**：
   - 所有图表自动保存到 `metrics_output_dir` 目录
   - 图表自动嵌入到 Markdown 报告的相应章节中
   - 使用相对路径引用，便于报告分享

## 使用示例

### 示例1: 基础多维度分析

**用户需求**: "通过 namespace='ieg-blueking-gse-data-tglog' 和 svr='xxx' 过滤，以 file_name 为键值，按日志级别 level 进行维度拆分"

**实现步骤**:

1. 构建查询字符串: `namespace:ieg-blueking-gse-data-tglog AND svr:xxx`
2. 获取所有 file_name 值
3. 对每个 file_name，分析 level 分布
4. 生成报告

### 示例2: 多层级分析

**用户需求**: "先按 namespace 分组，再按 svr 分组，最后按 level 拆分"

**实现步骤**:

1. 第一层: 获取所有 namespace 值
2. 第二层: 对每个 namespace，获取所有 svr 值
3. 第三层: 对每个 (namespace, svr) 组合，分析 level 分布

### 示例3: 时间序列分析

**用户需求**: "按 file_name 分组，分析每个文件在不同时间段的日志级别变化"

**实现步骤**:

1. 将时间范围拆分为多个时间段（如每小时）
2. 对每个时间段，执行多维度分析
3. 生成时间序列报告

### 示例4: 带指标查询的分析

**用户需求**: "分析 namespace='my-namespace' 的日志，并查询相关 Pod 的 CPU 和内存指标"

**实现步骤**:

1. 执行日志多维度分析（识别 namespace）
2. 自动识别资源：从日志分析结果中中识别到 `namespace="my-namespace"`
3. 查询指标：
   - CPU 使用率: `avg(avg_over_time(bkmonitor:system:cpu_summary:usage{namespace="my-namespace"}[1m]))`
   - 内存使用率: `avg(avg_over_time(bkmonitor:system:mem:pct_used{namespace="my-namespace"}[1m]))`
4. 生成指标图表并嵌入报告
5. 生成包含指标图片的 Markdown 报告

## 查询字符串构建

根据过滤条件构建 Lucene 查询字符串：

```python
def build_query_string(base_query: str, filter_fields: dict) -> str:
    """构建查询字符串"""
    query_parts = [base_query] if base_query != "*" else []
    
    for field, value in filter_fields.items():
        if isinstance(value, list):
            # 多值: field:(value1 OR value2)
            query_parts.append(f"({field}:({' OR '.join(value)}))")
        else:
            # 单值: field:value
            query_parts.append(f"{field}:{value}")
    
    return " AND ".join(query_parts) if query_parts else "*"
```

## 时间范围处理

⚠️ **重要限制**: `analyze_field` 工具的时间范围不能超过 1 天（86400秒）。

**处理策略**:

1. **检查时间范围**: 如果 `end_time - start_time > 86400`，需要拆分
2. **分批查询**: 将时间范围拆分为多个批次，每批 ≤ 24 小时
3. **合并结果**: 将各批次结果合并

```python
def split_time_range(start_time: int, end_time: int, max_span: int = 86400):
    """拆分时间范围"""
    ranges = []
    current_start = start_time
    
    while current_start < end_time:
        current_end = min(current_start + max_span, end_time)
        ranges.append((current_start, current_end))
        current_start = current_end
    
    return ranges
```

## 结果格式化

### 文本格式示例

```
================================================================================
日志多维度分析报告
================================================================================

分析配置:
  业务ID: 2
  索引集ID: 322
  过滤条件: {'namespace': 'xxx', 'svr': 'yyy'}
  分组字段: file_name
  拆分字段: level
  时间范围: 2025-12-18 08:00:00 ~ 2025-12-18 09:00:00

汇总统计:
  总分组数: 5
  总日志数: 1250

  按 level 汇总:
    ERROR: 450
    WARN: 300
    INFO: 500

详细分析结果:
--------------------------------------------------------------------------------

[file_name: handler.go]
  总日志数: 500
  按 level 分布:
    ERROR: 200 (40.0%)
    WARN: 150 (30.0%)
    INFO: 150 (30.0%)
```

### Markdown 格式示例

```markdown
# 日志多维度分析报告

## 分析配置
- **业务ID**: 2
- **索引集ID**: 322
- **过滤条件**: {'namespace': 'xxx', 'svr': 'yyy'}
- **分组字段**: file_name
- **拆分字段**: level

## 汇总统计
- **总分组数**: 5
- **总日志数**: 1250

### 按 level 汇总
| 值 | 数量 |
|---|---|
| ERROR | 450 |
| WARN | 300 |
| INFO | 500 |

## 详细分析结果

### file_name: handler.go
**总日志数**: 500

**按 level 分布**:
| 值 | 数量 | 占比 |
|---|---|---|
| ERROR | 200 | 40.0% |
| WARN | 150 | 30.0% |
| INFO | 150 | 30.0% |
```

## 常见问题

### Q: 如何确定字段名？

A: 使用 `get_index_set_fields` 工具获取索引集的所有可用字段。

### Q: 查询时间范围有限制吗？

A: 是的，`analyze_field` 工具的时间范围不能超过 1 天。超过需要分批查询。

### Q: 如何提高查询效率？

A: 
1. 使用更具体的过滤条件缩小查询范围
2. 合理设置 `limit` 参数
3. 对于大时间范围，拆分为多个小批次

### Q: 支持哪些查询语法？

A: 支持 Lucene 查询语法，包括：
- 精确匹配: `field:value`
- 多值匹配: `field:(value1 OR value2)`
- 范围查询: `field:[value1 TO value2]`
- 逻辑组合: `field1:value1 AND field2:value2`

### Q: 如何启用指标查询功能？

A: 在初始化 `LogMultiDimensionalAnalyzer` 时，`enable_metrics_query` 参数默认为 `True`。如果不需要指标查询，可以设置为 `False`。

### Q: 指标查询支持哪些资源类型？

A: 目前支持以下资源类型：
- **Pod**: 通过 `pod` 或 `pod_name` 字段识别
- **Namespace**: 通过 `namespace` 字段识别
- **Service**: 通过 `service` 或 `svc` 字段识别
- **Host**: 通过 `host`、`serverIp` 或 `ip` 字段识别
- **Container**: 通过 `container` 或 `container_name` 字段识别

### Q: 如何自定义指标查询？

A: 可以修改 `LogMultiDimensionalAnalyzer` 类中的 `resource_metrics_config` 字典，添加或修改资源类型对应的指标查询配置。

### Q: 生成的图片保存在哪里？

A: 默认保存在 `metrics` 目录下，可以通过初始化时的 `metrics_output_dir` 参数自定义。

### Q: 图表生成需要什么依赖？

A: 图表生成通过 `mcp-server-chart` MCP 工具完成，无需安装额外的 Python 依赖。确保 MCP 客户端已正确配置 chart MCP 服务。

## 指标查询功能

### 资源识别规则（增强版）

系统会自动识别日志分析结果中的以下资源类型：

| 资源类型 | 识别字段 | 查询指标示例 | 识别来源 |
|---------|---------|-------------|---------|
| Pod | `pod`, `pod_name` | CPU使用率、内存使用率 | filter_fields |
| Namespace | `namespace` | 命名空间资源使用情况 | filter_fields |
| Service | `service`, `svc` | 服务请求量、错误率 | filter_fields |
| Host | `host`, `serverIp`, `ip` | 主机CPU、内存、磁盘IO、系统负载 | filter_fields + 分组结果（IP地址格式） |
| Container | `container`, `container_name` | 容器资源使用情况 | filter_fields |

**增强功能**：
- 除了从 `filter_fields` 中识别资源外，还会从分组结果中识别IP地址格式的值
- 如果识别到主机IP，会自动查询以下时序指标：
  - CPU使用率
  - 内存使用率
  - 磁盘使用率
  - 磁盘IO使用率
  - 系统负载（5分钟平均）
- 所有指标都会自动生成时序折线图

### 指标查询示例

**示例1**: 查询 Pod CPU 使用率

```python
# 从日志分析结果中识别到 pod="my-app-xxx"
# 构建 PromQL 查询
promql = 'avg(avg_over_time(bkmonitor:system:cpu_summary:usage{pod="my-app-xxx"}[1m]))'

# 执行查询
metric_result = mcp_bkmonitor-metrics-bkop_execute_range_query({
    "body_param": {
        "bk_biz_id": "2",
        "promql": promql,
        "start_time": str(start_time),
        "end_time": str(end_time),
        "step": "1m"
    }
})
```

**示例2**: 查询主机内存使用率

```python
# 从日志分析结果中识别到 serverIp="9.136.132.152"
promql = 'avg(avg_over_time(bkmonitor:system:mem:pct_used{ip="9.136.132.152"}[1m]))'
```

### 图表生成

#### 指标图表生成（自动）

系统会自动为查询到的监控指标生成可视化图表，通过 `mcp-server-chart` MCP 工具完成：

- ✅ **自动生成** - 查询指标后自动调用 chart MCP 工具生成图表
- ✅ **折线图** - 使用 `generate_line_chart` 生成时序折线图
- ✅ **时间序列** - 支持时间序列数据可视化
- ✅ **高质量输出** - 图表自动保存为 PNG 格式

**图表生成流程**：

1. **日志分析** - 使用 `bkmonitor-log-bkop` 进行日志多维度分析
2. **指标获取** - 使用 `bkmonitor-metrics-bkop` 查询监控指标数据
3. **折线图绘制** - 使用 `mcp-server-chart` 的 `generate_line_chart` 生成图表
4. 解析时间戳（支持毫秒和秒两种格式）
5. 准备图表数据（time-value 格式）
6. 调用 chart MCP 工具生成折线图
7. 保存为 PNG 格式到 `metrics_output_dir` 目录
8. 在 Markdown 报告中自动嵌入图表引用

**示例代码**（系统内部自动执行）：

```python
# 系统会自动为每个指标生成图表
analyzer = LogMultiDimensionalAnalyzer(
    mcp_client=client,
    enable_metrics_query=True,
    metrics_output_dir="metrics_charts"
)

# 执行分析时，如果识别到资源，会自动查询指标并生成图表
result = analyzer.analyze_multi_dimensional(...)

# 结果中的 metrics 字段包含图表路径
for resource in result["metrics"]["resources"]:
    for metric_name, metric_data in resource["metrics"].items():
        if "chart_path" in metric_data:
            print(f"图表已生成: {metric_data['chart_path']}")
```



### 报告中的图片嵌入

系统在生成 Markdown 报告时会自动嵌入指标图表：

```markdown
## 关联指标分析

### pod: my-app-xxx

#### cpu

![cpu](metrics_charts/pod_my-app-xxx_cpu.png)

**指标统计**:
- 平均值: 45.50  最大值: 78.50  最小值: 23.10  数据点数: 60

#### memory

![memory](metrics_charts/pod_my-app-xxx_memory.png)

**指标统计**:
- 平均值: 45.50  最大值: 78.50  最小值: 23.10  数据点数: 60
```

**图表路径说明**：
- 图表保存在 `metrics_output_dir` 指定的目录（默认 `metrics`）
- Markdown 报告使用相对路径引用图表
- 如果图表生成失败，报告会跳过图表引用，继续生成其他内容

## 图表生成优化说明

### 已优化的功能

1. **中文字体支持**
   - 自动配置中文字体：`Arial Unicode MS`, `SimHei`, `DejaVu Sans`
   - 解决中文显示乱码问题

2. **图表样式优化**
   - 添加数据点标记（圆点）
   - 添加平均值参考线
   - 改进网格线样式
   - 优化图例显示

3. **时间戳处理**
   - 自动识别毫秒/秒时间戳格式
   - 正确转换时间戳为 datetime 对象

4. **数据解析优化**
   - 正确解析 `bkmonitor-metrics-bkop` 返回的数据格式
   - 处理 `datapoints` 数组格式：`[[timestamp_ms, value], ...]`
   - 过滤 None 值

5. **统计图表**
   - 新增 `generate_error_statistics_charts()` 方法
   - 支持生成对应的图表

### 使用示例

```python
from log_multi_dimensional_analyzer import LogMultiDimensionalAnalyzer

# 初始化分析器
analyzer = LogMultiDimensionalAnalyzer(
    mcp_client=client,
    enable_metrics_query=True,
    metrics_output_dir="metrics_charts"  # 图表输出目录
)

# 执行分析（会自动生成指标图表）
result = analyzer.analyze_multi_dimensional(
    bk_biz_id="2",
    index_set_id="2545",
    filter_fields={"serverIp": "30.189.38.149"},
    group_by_field="code_file",
    split_by_field="level",
    start_time=1766061357,
    end_time=1766062257
)

# 生成错误统计图表（可选）
error_levels = {"CRITICAL": 30, "ERROR": 40, "WARNING": 50}
error_types = {"支付系统不可用": 10, "数据库连接失败": 20}
error_charts = analyzer.generate_error_statistics_charts(
    error_levels=error_levels,
    error_types=error_types
)

# 生成 Markdown 报告（自动生成并嵌入图表，优化格式）
# 系统会自动：
# 1. 生成简洁的统计概览（合并显示，避免重复）
# 2. 检测分组字段是否为代码文件/模块，如果是则生成错误类型分布柱状图
# 3. 生成统一的详细分析表格（所有分组和拆分维度一目了然）
# 4. 自动识别资源（从 filter_fields 或分组结果中识别 IP、Pod、Namespace 等）
# 5. 自动查询时序指标（CPU、内存、磁盘、IO等）并生成时序图表
# 6. 合并显示指标统计信息（使用表格，避免重复）
# 7. 自动将图表嵌入到 Markdown 报告中
report = analyzer.format_output(result, format_type="markdown", auto_query_metrics=True)
```

## 资源

- **脚本**: `scripts/log_multi_dimensional_analyzer.py` - 多维度分析工具类（使用 chart MCP 生成图表）
- **参考文档**: `references/mcp_tools_guide.md` - MCP 工具详细使用指南
- **指标查询**: 使用 `bkmonitor-metrics-bkop` MCP 工具进行指标查询
- **图表生成**: 使用 `mcp-server-chart` MCP 工具生成指标可视化图表（折线图、饼图、柱状图）
