# 指标查询功能使用示例

本文档展示如何在日志分析中使用指标查询和图表生成功能。

## 基本使用

### 示例1: 分析 Pod 日志并查询 CPU/内存指标

```python
from log_multi_dimensional_analyzer import LogMultiDimensionalAnalyzer
from mcp_data_fetcher import MCPClient

# 初始化 MCP 客户端
client = MCPClient()

# 创建分析器（启用指标查询）
analyzer = LogMultiDimensionalAnalyzer(
    mcp_client=client,
    enable_metrics_query=True,
    metrics_output_dir="metrics"
)

# 执行分析（包含 Pod 过滤条件）
result = analyzer.analyze_multi_dimensional(
    bk_biz_id="2",
    index_set_id="322",
    filter_fields={
        "namespace": "my-namespace",
        "pod": "my-app-xxx"  # Pod 名称会被自动识别
    },
    group_by_field="file_name",
    split_by_field="level",
    start_time=1702300000,
    end_time=1702386400
)

# 生成 Markdown 报告（包含指标图片）
report = analyzer.format_output(result, format_type="markdown")
print(report)
```

### 示例2: 分析主机日志并查询系统指标

```python
# 分析主机日志
result = analyzer.analyze_multi_dimensional(
    bk_biz_id="2",
    index_set_id="322",
    filter_fields={
        "serverIp": "9.136.132.152"  # 主机IP会被自动识别
    },
    group_by_field="level",
    split_by_field="file_name"
)

# 系统会自动查询以下指标：
# - CPU 使用率
# - 内存使用率
# - 磁盘使用率
```

## 指标查询结果

分析结果中的 `metrics` 字段包含指标查询结果：

```json
{
  "metrics": {
    "resources": [
      {
        "resource_type": "pod",
        "resource_value": "my-app-xxx",
        "resource_field": "pod",
        "metrics": {
          "cpu": {
            "timestamps": [1702300000, 1702300060, ...],
            "values": [45.2, 46.8, ...],
            "statistics": {
              "avg": 45.5,
              "max": 78.5,
              "min": 23.1,
              "count": 60
            },
            "chart_path": "metrics/pod_my-app-xxx_cpu.png"
          },
          "memory": {
            ...
          }
        }
      }
    ],
    "queries": [
      {
        "resource": "my-app-xxx",
        "metric": "cpu",
        "promql": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{pod=\"my-app-xxx\"}[1m]))",
        "success": true
      }
    ],
    "charts": [
      "metrics/pod_my-app-xxx_cpu.png",
      "metrics/pod_my-app-xxx_memory.png"
    ]
  }
}
```

## 报告中的指标展示

生成的 Markdown 报告会自动包含指标图表：

```markdown
## 关联指标分析

### pod: my-app-xxx

#### cpu

![cpu](metrics/pod_my-app-xxx_cpu.png)

**指标统计**:
- 平均值: 45.50
- 最大值: 78.50
- 最小值: 23.10
- 数据点数: 60

#### memory

![memory](metrics/pod_my-app-xxx_memory.png)

**指标统计**:
- 平均值: 62.30
- 最大值: 85.20
- 最小值: 45.10
- 数据点数: 60
```

## 自定义指标查询

如果需要自定义指标查询，可以修改 `resource_metrics_config`：

```python
# 在初始化后修改配置
analyzer.resource_metrics_config["pod"]["disk"] = "avg(avg_over_time(bkmonitor:system:disk:in_use{pod=\"%s\"}[1m]))"
```

## 禁用指标查询

如果不需要指标查询功能，可以在初始化时禁用：

```python
analyzer = LogMultiDimensionalAnalyzer(
    mcp_client=client,
    enable_metrics_query=False  # 禁用指标查询
)
```

## 注意事项

1. **依赖安装**: 需要安装 matplotlib 才能生成图表
   ```bash
   pip install matplotlib
   ```

2. **MCP 工具**: 需要配置 `bkmonitor-metrics-bkop` MCP 工具才能查询指标

3. **时间范围**: 指标查询使用与日志分析相同的时间范围

4. **资源识别**: 系统只能识别过滤条件中的资源字段，不会从分析结果中提取资源信息

5. **图表路径**: 图表保存在 `metrics_output_dir` 指定的目录中，Markdown 报告使用相对路径引用


