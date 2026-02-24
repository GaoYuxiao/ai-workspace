#!/usr/bin/env python3
"""
日志多维度分析工具

支持通过 bklog-bkop MCP 工具进行日志数据的多维度分析：
- 支持自定义过滤条件（如 namespace、svr 等）
- 支持按指定字段分组（如 file_name）
- 支持按指定维度拆分（如日志级别 level）
- 生成多维度统计结果
- 自动识别日志分析结果中的资源（pod、namespace、service、host 等）
- 通过 bkmonitor-metrics-bkop MCP 工具查询相关监控指标
- 通过 mcp-server-chart MCP 工具生成指标可视化图表
- 在分析报告中嵌入指标图片和统计信息

执行流程：
1. 日志分析（使用 bkmonitor-log-bkop）
2. 指标获取（使用 bkmonitor-metrics-bkop）
3. 折线图绘制（使用 mcp-server-chart）
"""

import json
import sys
import time
import os
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class LogMultiDimensionalAnalyzer:
    """日志多维度分析器"""
    
    def __init__(self, mcp_client=None, enable_metrics_query: bool = True, metrics_output_dir: str = "metrics"):
        """
        初始化分析器
        
        Args:
            mcp_client: MCP 客户端实例，如果为 None 则需要在调用时手动传入结果
            enable_metrics_query: 是否启用指标查询功能，默认 True
            metrics_output_dir: 指标图片输出目录，默认 "metrics"
        """
        self.mcp_client = mcp_client
        self.enable_metrics_query = enable_metrics_query
        self.metrics_output_dir = Path(metrics_output_dir)
        self.metrics_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 资源识别映射：字段名 -> 资源类型
        self.resource_field_mapping = {
            "pod": "pod",
            "pod_name": "pod",
            "namespace": "namespace",
            "service": "service",
            "svc": "service",
            "host": "host",
            "serverIp": "host",
            "ip": "host",
            "container": "container",
            "container_name": "container"
        }
        
        # 资源类型对应的指标查询配置
        self.resource_metrics_config = {
            "pod": {
                "cpu": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{pod=\"%s\"}[1m]))",
                "memory": "avg(avg_over_time(bkmonitor:system:mem:pct_used{pod=\"%s\"}[1m]))"
            },
            "namespace": {
                "cpu": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{namespace=\"%s\"}[1m]))",
                "memory": "avg(avg_over_time(bkmonitor:system:mem:pct_used{namespace=\"%s\"}[1m]))"
            },
            "host": {
                "cpu": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{ip=\"%s\"}[1m]))",
                "memory": "avg(avg_over_time(bkmonitor:system:mem:pct_used{ip=\"%s\"}[1m]))",
                "disk": "avg(avg_over_time(bkmonitor:system:disk:in_use{ip=\"%s\"}[1m]))"
            },
            "service": {
                "cpu": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{service=\"%s\"}[1m]))",
                "memory": "avg(avg_over_time(bkmonitor:system:mem:pct_used{service=\"%s\"}[1m]))"
            }
        }
    
    def analyze_multi_dimensional(
        self,
        bk_biz_id: str,
        index_set_id: str,
        filter_fields: Dict[str, Any],
        group_by_field: str,
        split_by_field: str,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        query_string: str = "*",
        limit: int = 500
    ) -> Dict[str, Any]:
        """
        执行多维度分析
        
        Args:
            bk_biz_id: 业务ID
            index_set_id: 索引集ID
            filter_fields: 过滤字段字典，如 {"namespace": "xxx", "svr": "yyy"}
            group_by_field: 分组字段，如 "file_name"
            split_by_field: 拆分维度字段，如 "level"
            start_time: 开始时间戳（秒），如果为 None 则使用当前时间前1小时
            end_time: 结束时间戳（秒），如果为 None 则使用当前时间
            query_string: 查询字符串，默认为 "*"
            limit: 查询限制，默认 500
            
        Returns:
            多维度分析结果字典
        """
        # 计算时间范围
        if end_time is None:
            end_time = int(time.time())
        if start_time is None:
            start_time = end_time - 3600  # 默认最近1小时
        
        # 构建查询字符串
        query_parts = [query_string]
        for field, value in filter_fields.items():
            if isinstance(value, list):
                query_parts.append(f"({field}:({' OR '.join(value)}))")
            else:
                query_parts.append(f"{field}:{value}")
        
        final_query = " AND ".join([q for q in query_parts if q != "*" or len(query_parts) == 1])
        
        # 第一步：获取索引集字段信息（用于验证字段是否存在）
        if self.mcp_client:
            try:
                fields_result = self.mcp_client.call_tool(
                    "bkmonitor-log-bkop",
                    "get_index_set_fields",
                    {
                        "query_param": {
                            "bk_biz_id": bk_biz_id,
                            "index_set_id": index_set_id
                        }
                    }
                )
                # 验证字段是否存在
                available_fields = [f.get("field_name", "") for f in fields_result.get("fields", [])]
                if group_by_field not in available_fields:
                    print(f"警告: 分组字段 '{group_by_field}' 可能不存在于索引集中")
                if split_by_field not in available_fields:
                    print(f"警告: 拆分字段 '{split_by_field}' 可能不存在于索引集中")
            except Exception as e:
                print(f"警告: 无法获取字段信息: {e}")
        
        # 第二步：使用 analyze_field 进行字段分析
        # 先分析 group_by_field，获取所有分组值
        group_by_values = self._get_field_values(
            bk_biz_id, index_set_id, group_by_field,
            final_query, start_time, end_time
        )
        
        # 第三步：对每个分组值，分析 split_by_field
        results = {}
        for group_value in group_by_values:
            # 构建包含分组值的查询
            group_query = f"{final_query} AND {group_by_field}:{group_value}"
            
            # 分析拆分字段
            split_results = self._analyze_split_field(
                bk_biz_id, index_set_id, split_by_field,
                group_query, start_time, end_time
            )
            
            results[group_value] = split_results
        
        analysis_result = {
            "analysis_config": {
                "bk_biz_id": bk_biz_id,
                "index_set_id": index_set_id,
                "filter_fields": filter_fields,
                "group_by_field": group_by_field,
                "split_by_field": split_by_field,
                "time_range": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "start_time_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)),
                    "end_time_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
                },
                "query_string": final_query
            },
            "results": results,
            "summary": self._generate_summary(results)
        }
        
        # 如果启用指标查询，识别资源并查询指标
        if self.enable_metrics_query and self.mcp_client:
            metrics_results = self._query_related_metrics(
                bk_biz_id, filter_fields, results, start_time, end_time
            )
            analysis_result["metrics"] = metrics_results
        
        return analysis_result
    
    def _get_field_values(
        self,
        bk_biz_id: str,
        index_set_id: str,
        field_name: str,
        query_string: str,
        start_time: int,
        end_time: int
    ) -> List[str]:
        """获取字段的所有唯一值"""
        if not self.mcp_client:
            return []
        
        try:
            result = self.mcp_client.call_tool(
                "bkmonitor-log-bkop",
                "analyze_field",
                {
                    "body_param": {
                        "bk_biz_id": bk_biz_id,
                        "index_set_id": index_set_id,
                        "field_name": field_name,
                        "query_string": query_string,
                        "start_time": str(start_time),
                        "end_time": str(end_time),
                        "group_by": "true",
                        "order_by": "value",
                        "limit": "100"  # 获取 Top 100 的分组值
                    }
                }
            )
            
            # 提取字段值
            values = []
            if "data" in result and "list" in result["data"]:
                for item in result["data"]["list"]:
                    if "name" in item:
                        values.append(str(item["name"]))
                    elif "key" in item:
                        values.append(str(item["key"]))
            
            return values
        except Exception as e:
            print(f"错误: 获取字段值失败: {e}")
            return []
    
    def _analyze_split_field(
        self,
        bk_biz_id: str,
        index_set_id: str,
        field_name: str,
        query_string: str,
        start_time: int,
        end_time: int
    ) -> Dict[str, Any]:
        """分析拆分字段的分布"""
        if not self.mcp_client:
            return {}
        
        try:
            result = self.mcp_client.call_tool(
                "bkmonitor-log-bkop",
                "analyze_field",
                {
                    "body_param": {
                        "bk_biz_id": bk_biz_id,
                        "index_set_id": index_set_id,
                        "field_name": field_name,
                        "query_string": query_string,
                        "start_time": str(start_time),
                        "end_time": str(end_time),
                        "group_by": "true",
                        "order_by": "value",
                        "limit": "50"  # 获取 Top 50 的拆分值
                    }
                }
            )
            
            # 组织结果
            split_data = {}
            total_count = 0
            
            if "data" in result and "list" in result["data"]:
                for item in result["data"]["list"]:
                    key = str(item.get("name") or item.get("key", ""))
                    value = item.get("value", 0)
                    split_data[key] = value
                    total_count += value
            
            return {
                "distribution": split_data,
                "total": total_count,
                "count": len(split_data)
            }
        except Exception as e:
            print(f"错误: 分析拆分字段失败: {e}")
            return {}
    
    def _generate_summary(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """生成汇总统计"""
        summary = {
            "total_groups": len(results),
            "group_totals": {},
            "split_field_summary": defaultdict(int),
            "overall_total": 0
        }
        
        for group_value, group_data in results.items():
            if "total" in group_data:
                group_total = group_data["total"]
                summary["group_totals"][group_value] = group_total
                summary["overall_total"] += group_total
                
                # 汇总拆分字段的分布
                if "distribution" in group_data:
                    for split_value, count in group_data["distribution"].items():
                        summary["split_field_summary"][split_value] += count
        
        return summary
    
    def _identify_resources(self, filter_fields: Dict[str, Any], results: Dict[str, Dict]) -> List[Dict[str, str]]:
        """
        从分析结果中识别资源（增强版）
        
        Args:
            filter_fields: 过滤字段字典
            results: 分析结果
            
        Returns:
            资源列表，每个资源包含 type 和 value
        """
        resources = []
        seen_resources = set()  # 避免重复
        
        # 从过滤字段中识别资源（支持大小写不敏感匹配）
        for field, value in filter_fields.items():
            # 先尝试精确匹配
            resource_type = self.resource_field_mapping.get(field)
            # 如果精确匹配失败，尝试大小写不敏感匹配
            if not resource_type:
                field_lower = field.lower()
                # 创建大小写不敏感的映射
                case_insensitive_mapping = {k.lower(): v for k, v in self.resource_field_mapping.items()}
                resource_type = case_insensitive_mapping.get(field_lower)
            
            if resource_type:
                print(f"🔍 识别到资源: {resource_type} = {value} (字段: {field})")
                if isinstance(value, list):
                    for v in value:
                        resource_key = f"{resource_type}:{v}"
                        if resource_key not in seen_resources:
                            resources.append({"type": resource_type, "field": field, "value": str(v)})
                            seen_resources.add(resource_key)
                else:
                    resource_key = f"{resource_type}:{value}"
                    if resource_key not in seen_resources:
                        resources.append({"type": resource_type, "field": field, "value": str(value)})
                        seen_resources.add(resource_key)
        
        # 从结果中识别资源（如果分组字段是资源字段）
        # 例如：如果按 serverIp 分组，可以从分组值中识别主机资源
        for group_value, group_data in results.items():
            # 检查分组值是否可能是资源标识符
            # 例如：IP地址格式、Pod名称格式等
            if self._is_ip_address(group_value):
                resource_key = f"host:{group_value}"
                if resource_key not in seen_resources:
                    resources.append({"type": "host", "field": "group_value", "value": str(group_value)})
                    seen_resources.add(resource_key)
        
        return resources
    
    def _is_ip_address(self, value: str) -> bool:
        """判断字符串是否是IP地址"""
        import re
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        return bool(re.match(ip_pattern, str(value)))
    
    def _query_related_metrics(
        self,
        bk_biz_id: str,
        filter_fields: Dict[str, Any],
        results: Dict[str, Dict],
        start_time: int,
        end_time: int
    ) -> Dict[str, Any]:
        """
        查询相关指标
        
        Args:
            bk_biz_id: 业务ID
            filter_fields: 过滤字段
            results: 分析结果
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            指标查询结果字典
        """
        if not self.mcp_client:
            return {}
        
        metrics_results = {
            "resources": [],
            "queries": [],
            "charts": []
        }
        
        # 识别资源
        resources = self._identify_resources(filter_fields, results)
        
        for resource in resources:
            resource_type = resource["type"]
            resource_value = resource["value"]
            
            # 获取该资源类型的指标配置
            metrics_config = self.resource_metrics_config.get(resource_type, {})
            
            resource_metrics = {
                "resource_type": resource_type,
                "resource_value": resource_value,
                "resource_field": resource["field"],
                "metrics": {}
            }
            
            # 查询每个指标
            for metric_name, promql_template in metrics_config.items():
                try:
                    # 构建 PromQL 查询
                    promql = promql_template % resource_value
                    
                    # 执行查询
                    query_result = self.mcp_client.call_tool(
                        "bkmonitor-metrics-bkop",
                        "execute_range_query",
                        {
                            "body_param": {
                                "bk_biz_id": bk_biz_id,
                                "promql": promql,
                                "start_time": str(start_time),
                                "end_time": str(end_time),
                                "step": "1m"
                            }
                        }
                    )
                    
                    # 解析查询结果
                    metric_data = self._parse_metric_result(query_result)
                    
                    if metric_data:
                        resource_metrics["metrics"][metric_name] = metric_data
                        
                        # 生成图表
                        chart_path = self._generate_metric_chart(
                            metric_data,
                            f"{resource_type}_{resource_value}_{metric_name}",
                            f"{resource_type}_{resource_value}_{metric_name}",
                            start_time,
                            end_time
                        )
                        
                        if chart_path:
                            resource_metrics["metrics"][metric_name]["chart_path"] = chart_path
                            metrics_results["charts"].append(chart_path)
                    
                    metrics_results["queries"].append({
                        "resource": resource_value,
                        "metric": metric_name,
                        "promql": promql,
                        "success": metric_data is not None
                    })
                    
                except Exception as e:
                    print(f"警告: 查询指标失败 {resource_type}={resource_value}, metric={metric_name}: {e}")
                    metrics_results["queries"].append({
                        "resource": resource_value,
                        "metric": metric_name,
                        "promql": promql_template % resource_value,
                        "success": False,
                        "error": str(e)
                    })
            
            if resource_metrics["metrics"]:
                metrics_results["resources"].append(resource_metrics)
        
        return metrics_results
    
    def _parse_metric_result(self, query_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        解析指标查询结果
        
        Args:
            query_result: MCP 工具返回的查询结果
            
        Returns:
            解析后的指标数据，包含 timestamps 和 values 列表
        """
        try:
            # 根据实际返回格式解析
            # bkmonitor-metrics-bkop 返回格式: {"data": {"series": [{"datapoints": [[timestamp, value], ...]}]}}
            if "data" not in query_result:
                return None
            
            data = query_result["data"]
            timestamps = []
            values = []
            
            # 处理 bkmonitor-metrics-bkop 的实际返回格式
            if isinstance(data, dict):
                # 格式: {"series": [{"datapoints": [[timestamp_ms, value], ...]}]}
                series = data.get("series", [])
                for series_item in series:
                    datapoints = series_item.get("datapoints", [])
                    for point in datapoints:
                        if isinstance(point, list) and len(point) >= 2:
                            # point[0] 是时间戳（毫秒），point[1] 是值
                            timestamp_ms = point[0]
                            value = point[1]
                            if value is not None:  # 过滤掉 None 值
                                timestamps.append(timestamp_ms)
                                values.append(float(value))
            
            # 兼容其他可能的格式
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        # 可能是 {"timestamp": xxx, "value": xxx} 格式
                        if "timestamp" in item and "value" in item:
                            timestamps.append(item["timestamp"])
                            values.append(float(item["value"]))
                        # 可能是 {"time": xxx, "value": xxx} 格式
                        elif "time" in item and "value" in item:
                            timestamps.append(item["time"])
                            values.append(float(item["value"]))
            
            if not timestamps or not values:
                return None
            
            # 计算统计信息
            if values:
                avg_value = sum(values) / len(values)
                max_value = max(values)
                min_value = min(values)
            else:
                avg_value = max_value = min_value = 0
            
            return {
                "timestamps": timestamps,
                "values": values,
                "statistics": {
                    "avg": avg_value,
                    "max": max_value,
                    "min": min_value,
                    "count": len(values)
                }
            }
        except Exception as e:
            print(f"错误: 解析指标结果失败: {e}")
            return None
    
    def _generate_metric_chart(
        self,
        metric_data: Dict[str, Any],
        resource_identifier: str,
        metric_name: str,
        start_time: int,
        end_time: int
    ) -> Optional[str]:
        """
        生成指标图表（使用 chart MCP 工具）
        
        Args:
            metric_data: 指标数据，包含 timestamps 和 values
            resource_identifier: 资源标识符（用于文件名和标题）
            metric_name: 指标名称
            start_time: 开始时间（Unix时间戳，秒）
            end_time: 结束时间（Unix时间戳，秒）
            
        Returns:
            图表文件路径，如果生成失败返回 None
        """
        if not self.mcp_client:
            print("警告: MCP 客户端不可用，无法生成图表")
            return None
        
        try:
            timestamps = metric_data.get("timestamps", [])
            values = metric_data.get("values", [])
            
            if not timestamps or not values:
                return None
            
            # 转换时间戳为字符串格式（chart MCP 需要 time 字段为字符串）
            # 处理毫秒时间戳（bkmonitor返回的是毫秒）
            time_strings = []
            for ts in timestamps:
                if isinstance(ts, (int, float)):
                    if ts > 1e10:  # 毫秒时间戳
                        dt = datetime.fromtimestamp(ts / 1000)
                    else:  # 秒时间戳
                        dt = datetime.fromtimestamp(ts)
                    # chart MCP 可能需要简单的格式，如 "HH:MM" 或 "YYYY-MM-DD HH:MM:SS"
                    time_strings.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    time_strings.append(str(ts))
            
            # 准备折线图数据
            chart_data = []
            for time_str, value in zip(time_strings, values):
                chart_data.append({
                    "time": time_str,
                    "value": float(value)
                })
            
            # 构建图表标题
            title = f"{metric_name} - {resource_identifier}"
            
            # 确定 Y 轴标题
            unit = '%' if 'usage' in metric_name.lower() or 'pct' in metric_name.lower() else ''
            y_axis_title = f"{metric_name} ({unit})" if unit else metric_name
            
            # 调用 chart MCP 工具生成折线图
            chart_result = self.mcp_client.call_tool(
                "mcp-server-chart",
                "generate_line_chart",
                {
                    "data": chart_data,
                    "title": title,
                    "axisXTitle": "时间",
                    "axisYTitle": y_axis_title,
                    "width": 1200,
                    "height": 600,
                    "theme": "default"
                }
            )
            
            # chart MCP 返回的是 base64 编码的图片数据或文件路径
            # 需要保存到本地文件
            if chart_result:
                # 生成文件名（清理特殊字符）
                safe_identifier = "".join(c for c in resource_identifier if c.isalnum() or c in ('-', '_', '.'))
                safe_metric = "".join(c for c in metric_name if c.isalnum() or c in ('-', '_'))
                filename = f"{safe_identifier}_{safe_metric}.png"
                filepath = self.metrics_output_dir / filename
                
                # 使用统一的保存方法
                self._save_chart_result(chart_result, filepath)
                
                return str(filepath)
            
            return None
        except Exception as e:
            print(f"错误: 生成图表失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_error_statistics_charts(
        self,
        error_levels: Dict[str, int],
        error_types: Optional[Dict[str, int]] = None,
        output_prefix: str = "error"
    ) -> Dict[str, str]:
        """
        生成错误统计图表（使用 chart MCP 工具）
        
        Args:
            error_levels: 错误级别统计，如 {"CRITICAL": 30, "ERROR": 40, "WARNING": 50}
            error_types: 错误类型统计，如 {"支付系统不可用": 10, "数据库连接失败": 20}
            output_prefix: 输出文件前缀，默认 "error"
            
        Returns:
            生成的图表文件路径字典，如 {"levels": "path/to/error_levels.png", "types": "path/to/error_types.png"}
        """
        chart_paths = {}
        
        if not self.mcp_client:
            print("警告: MCP 客户端不可用，无法生成图表")
            return chart_paths
        
        # 生成错误级别分布饼图
        if error_levels:
            try:
                # 准备饼图数据
                pie_data = []
                for category, value in error_levels.items():
                    pie_data.append({
                        "category": category,
                        "value": value
                    })
                
                # 调用 chart MCP 工具生成饼图
                chart_result = self.mcp_client.call_tool(
                    "mcp-server-chart",
                    "generate_pie_chart",
                    {
                        "data": pie_data,
                        "title": "错误级别分布",
                        "width": 800,
                        "height": 800,
                        "theme": "default"
                    }
                )
                
                if chart_result:
                    output_path = self.metrics_output_dir / f"{output_prefix}_levels.png"
                    self._save_chart_result(chart_result, output_path)
                    chart_paths["levels"] = str(output_path)
                    print(f"✅ 已生成错误级别图表: {output_path}")
            except Exception as e:
                print(f"❌ 生成错误级别图表失败: {e}")
        
        # 生成错误类型分布柱状图
        if error_types:
            try:
                # 按出现次数排序
                sorted_types = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
                
                # 准备柱状图数据
                bar_data = []
                for category, value in sorted_types:
                    bar_data.append({
                        "category": category,
                        "value": value
                    })
                
                # 调用 chart MCP 工具生成柱状图
                chart_result = self.mcp_client.call_tool(
                    "mcp-server-chart",
                    "generate_bar_chart",
                    {
                        "data": bar_data,
                        "title": "错误类型分布",
                        "axisXTitle": "出现次数",
                        "axisYTitle": "错误类型",
                        "width": 1200,
                        "height": 800,
                        "theme": "default"
                    }
                )
                
                if chart_result:
                    output_path = self.metrics_output_dir / f"{output_prefix}_types.png"
                    self._save_chart_result(chart_result, output_path)
                    chart_paths["types"] = str(output_path)
                    print(f"✅ 已生成错误类型图表: {output_path}")
            except Exception as e:
                print(f"❌ 生成错误类型图表失败: {e}")
        
        return chart_paths
    
    def _save_chart_result(self, chart_result: Any, filepath: Path) -> None:
        """
        保存图表结果到文件
        
        Args:
            chart_result: chart MCP 工具返回的结果（可能是 base64 字符串、文件路径或其他格式）
            filepath: 保存路径
        """
        try:
            import base64
            import shutil
            
            # 如果返回的是 base64 数据，需要解码保存
            if isinstance(chart_result, dict):
                # 可能是 {"image": "base64..."} 格式
                if "image" in chart_result:
                    image_data = chart_result["image"]
                    if isinstance(image_data, str):
                        if image_data.startswith("data:image"):
                            # 移除 data:image/png;base64, 前缀
                            image_data = image_data.split(",", 1)[1]
                        with open(filepath, "wb") as f:
                            f.write(base64.b64decode(image_data))
                        return
                # 可能是 {"file": "path/to/file"} 格式
                if "file" in chart_result:
                    shutil.copy(chart_result["file"], filepath)
                    return
            elif isinstance(chart_result, str):
                # 如果返回的是 base64 字符串
                if chart_result.startswith("data:image"):
                    image_data = chart_result.split(",", 1)[1]
                    with open(filepath, "wb") as f:
                        f.write(base64.b64decode(image_data))
                    return
                # 如果返回的是文件路径
                if Path(chart_result).exists():
                    shutil.copy(chart_result, filepath)
                    return
            elif isinstance(chart_result, bytes):
                # 直接是二进制数据
                with open(filepath, "wb") as f:
                    f.write(chart_result)
                return
            
            # 其他格式，尝试直接写入
            with open(filepath, "wb") as f:
                if isinstance(chart_result, bytes):
                    f.write(chart_result)
                else:
                    f.write(str(chart_result).encode())
        except Exception as e:
            print(f"错误: 保存图表失败: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def format_output(self, analysis_result: Dict[str, Any], format_type: str = "text", auto_query_metrics: bool = True) -> str:
        """
        格式化输出结果（自动查询指标并生成图表）
        
        Args:
            analysis_result: 分析结果字典
            format_type: 输出格式，支持 "text", "json", "markdown"
            auto_query_metrics: 是否自动查询指标（如果结果中没有指标数据），默认 True
            
        Returns:
            格式化后的字符串
        """
        # 如果是 Markdown 格式且启用了自动查询指标，检查是否需要查询指标
        if format_type == "markdown" and auto_query_metrics and self.enable_metrics_query and self.mcp_client:
            config = analysis_result.get("analysis_config", {})
            metrics = analysis_result.get("metrics", {})
            
            # 如果没有指标数据，尝试自动查询
            if not metrics or not metrics.get("resources"):
                filter_fields = config.get("filter_fields", {})
                results = analysis_result.get("results", {})
                time_range = config.get("time_range", {})
                start_time = time_range.get("start_time")
                end_time = time_range.get("end_time")
                bk_biz_id = config.get("bk_biz_id")
                
                if start_time and end_time and bk_biz_id:
                    # 识别资源并查询指标
                    metrics_results = self._query_related_metrics(
                        bk_biz_id, filter_fields, results, start_time, end_time
                    )
                    if metrics_results and metrics_results.get("resources"):
                        analysis_result["metrics"] = metrics_results
        
        if format_type == "json":
            return json.dumps(analysis_result, ensure_ascii=False, indent=2)
        
        elif format_type == "markdown":
            return self._format_markdown(analysis_result)
        
        else:  # text
            return self._format_text(analysis_result)
    
    def _format_text(self, result: Dict[str, Any]) -> str:
        """文本格式输出"""
        lines = []
        config = result.get("analysis_config", {})
        results = result.get("results", {})
        summary = result.get("summary", {})
        
        lines.append("=" * 80)
        lines.append("日志多维度分析报告")
        lines.append("=" * 80)
        lines.append("")
        
        # 配置信息
        lines.append("分析配置:")
        lines.append(f"  业务ID: {config.get('bk_biz_id')}")
        lines.append(f"  索引集ID: {config.get('index_set_id')}")
        lines.append(f"  过滤条件: {config.get('filter_fields')}")
        lines.append(f"  分组字段: {config.get('group_by_field')}")
        lines.append(f"  拆分字段: {config.get('split_by_field')}")
        time_range = config.get("time_range", {})
        lines.append(f"  时间范围: {time_range.get('start_time_str')} ~ {time_range.get('end_time_str')}")
        lines.append("")
        
        # 汇总信息
        lines.append("汇总统计:")
        lines.append(f"  总分组数: {summary.get('total_groups', 0)}")
        lines.append(f"  总日志数: {summary.get('overall_total', 0)}")
        lines.append("")
        
        # 拆分字段汇总
        split_summary = summary.get("split_field_summary", {})
        if split_summary:
            lines.append(f"  按 {config.get('split_by_field')} 汇总:")
            for split_value, count in sorted(split_summary.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"    {split_value}: {count}")
            lines.append("")
        
        # 详细结果
        lines.append("详细分析结果:")
        lines.append("-" * 80)
        for group_value, group_data in sorted(results.items()):
            lines.append(f"\n[{config.get('group_by_field')}: {group_value}]")
            lines.append(f"  总日志数: {group_data.get('total', 0)}")
            
            distribution = group_data.get("distribution", {})
            if distribution:
                lines.append(f"  按 {config.get('split_by_field')} 分布:")
                for split_value, count in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / group_data.get('total', 1)) * 100 if group_data.get('total', 0) > 0 else 0
                    lines.append(f"    {split_value}: {count} ({percentage:.1f}%)")
        
        lines.append("")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _format_markdown(self, result: Dict[str, Any]) -> str:
        """Markdown 格式输出（优化版：结构清晰，避免重复）"""
        lines = []
        config = result.get("analysis_config", {})
        results = result.get("results", {})
        summary = result.get("summary", {})
        
        # 标题
        lines.append("# 日志分析报告\n")
        
        # 基本信息（简化）
        time_range = config.get("time_range", {})
        lines.append(f"**时间范围**: {time_range.get('start_time_str')} ~ {time_range.get('end_time_str')}  ")
        lines.append(f"**总日志数**: {summary.get('overall_total', 0)}  ")
        lines.append(f"**分析维度**: {summary.get('total_groups', 0)} 个 {config.get('group_by_field', '')}\n")
        
        # 关键统计（合并显示，避免重复）
        split_summary = summary.get("split_field_summary", {})
        if split_summary:
            lines.append("## 统计概览\n")
            lines.append("| 类型 | 数量 | 占比 |")
            lines.append("|---|---|---|")
            total = summary.get('overall_total', 1)
            for split_value, count in sorted(split_summary.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total) * 100 if total > 0 else 0
                lines.append(f"| {split_value} | {count} | {percentage:.1f}% |")
            lines.append("")
        
        # 错误类型分布图表（仅当分组字段是代码文件/模块时生成）
        error_chart_paths = {}
        group_by_field = config.get('group_by_field', '').lower()
        split_by_field = config.get('split_by_field', '').lower()
        
        if group_by_field in ['code_file', 'file_name', 'module', 'service', 'component']:
            # 只生成错误类型分布图表（不生成错误级别饼图）
            error_types = {}
            for group_value, group_data in results.items():
                # 只统计严重错误（CRITICAL + ERROR）
                if split_by_field in ['level', 'log_level', 'severity', 'error_level']:
                    distribution = group_data.get('distribution', {})
                    error_count = 0
                    for level, count in distribution.items():
                        level_upper = str(level).upper()
                        if level_upper in ['CRITICAL', 'ERROR']:
                            error_count += count
                    if error_count > 0:
                        error_types[str(group_value)] = error_count
            
            if error_types:
                chart_paths = self.generate_error_statistics_charts(
                    error_levels=None,
                    error_types=error_types,
                    output_prefix="error_types"
                )
                if chart_paths.get("types"):
                    error_chart_paths["types"] = chart_paths["types"]
        
        # 嵌入错误类型分布图表
        if error_chart_paths.get("types"):
            lines.append("## 错误分布\n")
            chart_path = error_chart_paths["types"]
            chart_filename = os.path.basename(chart_path)
            try:
                rel_path = os.path.relpath(chart_path)
            except ValueError:
                rel_path = f"{self.metrics_output_dir.name}/{chart_filename}"
            lines.append(f"![错误类型分布]({rel_path})\n")
            lines.append("")
        
        # 详细结果（简化表格，避免重复信息）
        if results:
            lines.append("## 详细分析\n")
            
            # 获取所有拆分字段的值作为表头
            all_split_values = set()
            for group_data in results.values():
                distribution = group_data.get("distribution", {})
                all_split_values.update(distribution.keys())
            
            if all_split_values:
                # 构建表头
                sorted_split_values = sorted(all_split_values)
                header = f"| {config.get('group_by_field', '分组')} | 总数 | "
                header += " | ".join(sorted_split_values) + " |\n"
                lines.append(header)
                
                # 表头分隔线
                header_sep = "|" + "|".join(["---"] * (2 + len(sorted_split_values))) + "|\n"
                lines.append(header_sep)
                
                # 数据行
                for group_value, group_data in sorted(results.items(), key=lambda x: x[1].get('total', 0), reverse=True):
                    total = group_data.get('total', 0)
                    distribution = group_data.get("distribution", {})
                    row = f"| {group_value} | {total} | "
                    row += " | ".join([str(distribution.get(split_value, 0)) for split_value in sorted_split_values]) + " |\n"
                    lines.append(row)
            else:
                # 如果没有拆分字段，只显示总数
                lines.append("| 分组 | 总数 |\n")
                lines.append("|---|---|\n")
                for group_value, group_data in sorted(results.items(), key=lambda x: x[1].get('total', 0), reverse=True):
                    lines.append(f"| {group_value} | {group_data.get('total', 0)} |\n")
            lines.append("")
        
        # 指标分析部分（自动生成时序图表，简化显示）
        metrics = result.get("metrics", {})
        if metrics and metrics.get("resources"):
            lines.append("## 🖥️ 设备资源监控分析\n")
            
            for resource_info in metrics["resources"]:
                resource_type = resource_info["resource_type"]
                resource_value = resource_info["resource_value"]
                resource_metrics = resource_info["metrics"]
                
                lines.append(f"### {resource_type}: {resource_value}\n")
                
                # 合并显示所有指标的统计信息
                if resource_metrics:
                    lines.append("| 指标 | 平均值 | 最大值 | 最小值 |\n")
                    lines.append("|---|---|---|---|\n")
                    
                    chart_paths = []
                    for metric_name, metric_data in resource_metrics.items():
                        # 确保图表已生成
                        chart_path = metric_data.get("chart_path")
                        if not chart_path and metric_data.get("timestamps") and metric_data.get("values"):
                            config = result.get("analysis_config", {})
                            time_range = config.get("time_range", {})
                            start_time = time_range.get("start_time")
                            end_time = time_range.get("end_time")
                            
                            if start_time and end_time:
                                chart_path = self._generate_metric_chart(
                                    metric_data,
                                    f"{resource_type}_{resource_value}_{metric_name}",
                                    f"{metric_name}",
                                    start_time,
                                    end_time
                                )
                                if chart_path:
                                    metric_data["chart_path"] = chart_path
                        
                        stats = metric_data.get("statistics", {})
                        if stats:
                            lines.append(f"| {metric_name} | {stats.get('avg', 0):.2f} | {stats.get('max', 0):.2f} | {stats.get('min', 0):.2f} |\n")
                        
                        if chart_path:
                            chart_paths.append((metric_name, chart_path))
                    
                    lines.append("")
                    
                    # 显示所有图表
                    for metric_name, chart_path in chart_paths:
                        chart_filename = os.path.basename(chart_path)
                        try:
                            rel_path = os.path.relpath(chart_path)
                        except ValueError:
                            rel_path = f"{self.metrics_output_dir.name}/{chart_filename}"
                        lines.append(f"#### {metric_name}\n")
                        lines.append(f"![{metric_name}]({rel_path})\n")
                        lines.append("")
        
        # 如果 metrics 为空或不存在，尝试回退查询主机指标
        if (not metrics or not metrics.get("resources")) and self.enable_metrics_query and self.mcp_client:
            # 即使没有识别到资源，也尝试从 filter_fields 中查询通用指标
            config = result.get("analysis_config", {})
            filter_fields = config.get("filter_fields", {})
            time_range = config.get("time_range", {})
            start_time = time_range.get("start_time")
            end_time = time_range.get("end_time")
            bk_biz_id = config.get("bk_biz_id")
            
            # 检查是否有主机IP，如果有则查询主机指标
            host_ip = None
            for field, value in filter_fields.items():
                if field.lower() in ['serverip', 'ip', 'host']:
                    host_ip = str(value) if not isinstance(value, list) else str(value[0]) if value else None
                    break
            
            # 如果没有从 filter_fields 中找到，尝试从结果中查找IP地址
            if not host_ip:
                results = result.get("results", {})
                print(f"🔍 从结果中查找IP地址，结果数量: {len(results)}")
                for group_value in results.keys():
                    if self._is_ip_address(str(group_value)):
                        host_ip = str(group_value)
                        print(f"✅ 从结果中识别到主机IP: {host_ip}")
                        break
            
            if host_ip and start_time and end_time and bk_biz_id:
                print(f"🔍 准备查询主机指标: {host_ip}, 业务ID: {bk_biz_id}, 时间范围: {start_time} ~ {end_time}")
                lines.append("## 🖥️ 设备资源监控分析\n")
                lines.append(f"### 主机: {host_ip}\n")
                
                # 查询主机通用指标
                host_metrics = self._query_host_metrics(bk_biz_id, host_ip, start_time, end_time)
                
                if host_metrics:
                    # 合并显示统计信息
                    lines.append("| 指标 | 平均值 | 最大值 | 最小值 |\n")
                    lines.append("|---|---|---|---|\n")
                    
                    chart_paths = []
                    for metric_name, metric_data in host_metrics.items():
                        # 生成图表
                        chart_path = self._generate_metric_chart(
                            metric_data,
                            f"host_{host_ip}_{metric_name}",
                            f"{metric_name}",
                            start_time,
                            end_time
                        )
                        
                        stats = metric_data.get("statistics", {})
                        if stats:
                            lines.append(f"| {metric_name} | {stats.get('avg', 0):.2f} | {stats.get('max', 0):.2f} | {stats.get('min', 0):.2f} |\n")
                        
                        if chart_path:
                            chart_paths.append((metric_name, chart_path))
                    
                    lines.append("")
                    
                    # 显示所有图表
                    for metric_name, chart_path in chart_paths:
                        chart_filename = os.path.basename(chart_path)
                        try:
                            rel_path = os.path.relpath(chart_path)
                        except ValueError:
                            rel_path = f"{self.metrics_output_dir.name}/{chart_filename}"
                        lines.append(f"#### {metric_name}\n")
                        lines.append(f"![{metric_name}]({rel_path})\n")
                        lines.append("")
        
        return "\n".join(lines)
    
    def _query_host_metrics(self, bk_biz_id: str, host_ip: str, start_time: int, end_time: int) -> Dict[str, Dict[str, Any]]:
        """
        查询主机通用指标（CPU、内存、磁盘等）
        
        Args:
            bk_biz_id: 业务ID
            host_ip: 主机IP
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            指标数据字典
        """
        if not self.mcp_client:
            return {}
        
        host_metrics = {}
        
        # 主机通用指标配置
        host_metric_configs = {
            "CPU使用率": "avg(avg_over_time(bkmonitor:system:cpu_summary:usage{ip=\"%s\"}[1m]))",
            "内存使用率": "avg(avg_over_time(bkmonitor:system:mem:pct_used{ip=\"%s\"}[1m]))",
            "磁盘使用率": "avg(avg_over_time(bkmonitor:system:disk:in_use{ip=\"%s\"}[1m]))",
            "磁盘IO使用率": "avg(avg_over_time(bkmonitor:system:io:util{ip=\"%s\"}[1m]))",
            "系统负载": "avg(avg_over_time(bkmonitor:system:system:load:load5{ip=\"%s\"}[5m]))"
        }
        
        print(f"🔍 开始查询主机指标: {host_ip}, 时间范围: {start_time} ~ {end_time}")
        
        for metric_name, promql_template in host_metric_configs.items():
            try:
                promql = promql_template % host_ip
                print(f"  📊 查询指标: {metric_name}, PromQL: {promql}")
                
                query_result = self.mcp_client.call_tool(
                    "bkmonitor-metrics-bkop",
                    "execute_range_query",
                    {
                        "body_param": {
                            "bk_biz_id": bk_biz_id,
                            "promql": promql,
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "step": "1m"
                        }
                    }
                )
                
                metric_data = self._parse_metric_result(query_result)
                if metric_data:
                    host_metrics[metric_name] = metric_data
                    print(f"  ✅ 成功获取指标: {metric_name}, 数据点数: {len(metric_data.get('values', []))}")
                else:
                    print(f"  ⚠️ 指标数据为空: {metric_name}")
            except Exception as e:
                print(f"  ❌ 查询主机指标失败 {host_ip}, metric={metric_name}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"📈 主机指标查询完成，共获取 {len(host_metrics)} 个指标")
        
        return host_metrics


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python log_multi_dimensional_analyzer.py <config_json_file>")
        print("\n配置文件格式:")
        print(json.dumps({
            "bk_biz_id": "2",
            "index_set_id": "322",
            "filter_fields": {"namespace": "xxx", "svr": "yyy"},
            "group_by_field": "file_name",
            "split_by_field": "level",
            "start_time": 1702300000,
            "end_time": 1702386400,
            "query_string": "*"
        }, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # 读取配置
    config_file = sys.argv[1]
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 创建分析器（不使用 MCP 客户端，直接使用结果）
    analyzer = LogMultiDimensionalAnalyzer()
    
    # 执行分析（需要手动调用 MCP 工具）
    print("注意: 此脚本需要配合 MCP 工具使用")
    print("请使用 MCP 工具调用 analyze_field 进行实际分析")


if __name__ == "__main__":
    main()

