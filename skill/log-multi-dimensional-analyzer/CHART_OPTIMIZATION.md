# 图表生成功能优化说明

## 📊 优化概述

本次优化将实际验证过的图表生成方案整合到 skill 中，确保图表能够正确生成并嵌入到报告中。

## ✅ 已完成的优化

### 1. 中文字体支持

**问题**：之前图表中的中文显示为方框或乱码

**解决方案**：
- 在 matplotlib 初始化时配置中文字体
- 字体优先级：`Arial Unicode MS` → `SimHei` → `DejaVu Sans` → `sans-serif`
- 解决负号显示问题

```python
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
```

### 2. 指标数据解析优化

**问题**：之前无法正确解析 `bkmonitor-metrics-bkop` 返回的数据格式

**解决方案**：
- 正确解析 `datapoints` 数组格式：`[[timestamp_ms, value], ...]`
- 自动识别毫秒/秒时间戳格式
- 过滤 None 值，避免图表错误

```python
# 处理 bkmonitor-metrics-bkop 的实际返回格式
series = data.get("series", [])
for series_item in series:
    datapoints = series_item.get("datapoints", [])
    for point in datapoints:
        if isinstance(point, list) and len(point) >= 2:
            timestamp_ms = point[0]  # 毫秒时间戳
            value = point[1]
            if value is not None:  # 过滤 None 值
                timestamps.append(timestamp_ms)
                values.append(float(value))
```

### 3. 图表样式优化

**优化内容**：
- ✅ 添加数据点标记（圆点，markersize=4）
- ✅ 添加平均值参考线（红色虚线）
- ✅ 改进网格线样式（虚线，透明度0.3）
- ✅ 优化图例显示（显示平均值和单位）
- ✅ 增加线条宽度（2.5px）
- ✅ 优化图表尺寸（12x6）

```python
# 绘制主数据线
ax.plot(dt_timestamps, values, linewidth=2.5, color='#1f77b4', 
        marker='o', markersize=4, alpha=0.8)

# 添加平均值线
if statistics and 'avg' in statistics:
    avg_value = statistics['avg']
    unit = '%' if 'usage' in metric_name.lower() or 'pct' in metric_name.lower() else ''
    ax.axhline(y=avg_value, color='r', linestyle='--', linewidth=1.5, 
              alpha=0.7, label=f'平均值: {avg_value:.2f}{unit}')
    ax.legend(loc='upper right', fontsize=10)
```

### 4. 时间戳处理优化

**问题**：无法正确处理毫秒时间戳

**解决方案**：
- 自动检测时间戳格式（毫秒 vs 秒）
- 正确转换为 datetime 对象

```python
# 处理毫秒时间戳（bkmonitor返回的是毫秒）
if isinstance(timestamps[0], (int, float)):
    if timestamps[0] > 1e10:  # 毫秒时间戳（大于10位数字）
        dt_timestamps = [datetime.fromtimestamp(ts / 1000) for ts in timestamps]
    else:  # 秒时间戳
        dt_timestamps = [datetime.fromtimestamp(ts) for ts in timestamps]
```

### 5. 新增错误统计图表功能

**新增方法**：`generate_error_statistics_charts()`

**功能**：
- 生成错误级别分布饼图
- 生成错误类型分布柱状图
- 自动根据严重程度设置颜色

```python
# 使用示例
error_levels = {"CRITICAL": 30, "ERROR": 40, "WARNING": 50}
error_types = {"支付系统不可用": 10, "数据库连接失败": 20}

chart_paths = analyzer.generate_error_statistics_charts(
    error_levels=error_levels,
    error_types=error_types,
    output_prefix="error"
)
```

## 🔧 技术细节

### 文件修改

1. **`log_multi_dimensional_analyzer.py`**
   - ✅ 优化 `_parse_metric_result()` - 正确解析数据格式
   - ✅ 优化 `_generate_metric_chart()` - 改进图表样式和中文支持
   - ✅ 新增 `generate_error_statistics_charts()` - 错误统计图表

2. **`SKILL.md`**
   - ✅ 更新图表生成说明
   - ✅ 添加优化功能说明
   - ✅ 添加使用示例

### 关键改进点

| 功能 | 优化前 | 优化后 |
|------|--------|--------|
| 中文显示 | ❌ 乱码 | ✅ 正常显示 |
| 数据解析 | ❌ 格式不匹配 | ✅ 正确解析 |
| 时间戳 | ❌ 只支持秒 | ✅ 支持毫秒/秒 |
| 图表样式 | ⚠️ 基础样式 | ✅ 优化样式（标记、平均值线） |
| 错误统计 | ❌ 不支持 | ✅ 支持饼图和柱状图 |

## 📝 使用说明

### 基本使用

图表生成是自动的，无需额外配置：

```python
analyzer = LogMultiDimensionalAnalyzer(
    mcp_client=client,
    enable_metrics_query=True,
    metrics_output_dir="metrics_charts"
)

# 执行分析，系统会自动生成指标图表
result = analyzer.analyze_multi_dimensional(...)

# 图表路径在 result["metrics"]["resources"][i]["metrics"][metric_name]["chart_path"]
```

### 生成错误统计图表

```python
# 从日志分析结果中提取错误统计
error_levels = {"CRITICAL": 30, "ERROR": 40, "WARNING": 50}
error_types = {"支付系统不可用": 10, "数据库连接失败": 20}

# 生成图表
chart_paths = analyzer.generate_error_statistics_charts(
    error_levels=error_levels,
    error_types=error_types
)

# chart_paths = {
#     "levels": "metrics_charts/error_levels.png",
#     "types": "metrics_charts/error_types.png"
# }
```

## 🎯 验证结果

基于实际测试（多别名设置验证报告）：

- ✅ CPU使用率图表生成成功
- ✅ 内存使用率图表生成成功
- ✅ 磁盘使用率图表生成成功
- ✅ 磁盘IO使用率图表生成成功
- ✅ 错误级别分布饼图生成成功
- ✅ 错误类型分布柱状图生成成功
- ✅ 所有图表正确嵌入到 Markdown 报告中

## 📌 注意事项

1. **依赖要求**：需要安装 matplotlib
   ```bash
   pip install matplotlib
   ```

2. **字体支持**：如果系统没有中文字体，图表中的中文可能显示为方框
   - macOS: 通常有 `Arial Unicode MS`
   - Linux: 需要安装中文字体包
   - Windows: 通常有 `SimHei`

3. **图表目录**：确保 `metrics_output_dir` 目录有写入权限

4. **相对路径**：Markdown 报告使用相对路径引用图表，确保报告和图表目录的相对位置正确

## 🔄 后续优化建议

1. 支持更多图表类型（如堆叠柱状图、热力图等）
2. 支持自定义图表样式和颜色
3. 支持图表模板配置
4. 添加图表缓存机制，避免重复生成


