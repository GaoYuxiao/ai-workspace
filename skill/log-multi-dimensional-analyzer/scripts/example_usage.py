#!/usr/bin/env python3
"""
日志多维度分析使用示例

展示如何使用 MCP 工具进行日志多维度分析
"""

import json
import time
import sys
import os

# 添加父目录到路径，以便导入 mcp_data_fetcher
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'mcp-data-fetcher', 'scripts'))
try:
    from mcp_data_fetcher import MCPClient
except ImportError:
    print("警告: 无法导入 MCPClient，请确保 mcp-data-fetcher skill 已安装")
    MCPClient = None


def example_multi_dimensional_analysis():
    """示例: 多维度分析"""
    
    # 配置参数
    bk_biz_id = "2"
    index_set_id = "322"
    filter_fields = {
        "namespace": "ieg-blueking-gse-data-tglog",
        "svr": "xxx"  # 根据实际情况修改
    }
    group_by_field = "file_name"
    split_by_field = "level"
    
    # 时间范围（最近1小时）
    end_time = int(time.time())
    start_time = end_time - 3600
    
    if not MCPClient:
        print("错误: 需要 MCPClient 才能执行分析")
        return
    
    client = MCPClient()
    
    # 步骤1: 获取分组字段的所有值
    print("步骤1: 获取所有 file_name 值...")
    query_string = " AND ".join([f"{k}:{v}" for k, v in filter_fields.items()])
    
    group_result = client.call_tool(
        "bkmonitor-log-bkop",
        "analyze_field",
        {
            "body_param": {
                "bk_biz_id": bk_biz_id,
                "index_set_id": index_set_id,
                "field_name": group_by_field,
                "query_string": query_string,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "group_by": "true",
                "order_by": "value",
                "limit": "100"
            }
        }
    )
    
    # 提取分组值
    group_values = []
    if "data" in group_result and "list" in group_result["data"]:
        for item in group_result["data"]["list"]:
            group_values.append(item.get("name") or item.get("key", ""))
    
    print(f"找到 {len(group_values)} 个分组值")
    
    # 步骤2: 对每个分组值，分析拆分字段
    print("\n步骤2: 分析每个分组的拆分字段分布...")
    results = {}
    
    for group_value in group_values[:10]:  # 只处理前10个，避免过多请求
        print(f"  分析 {group_by_field}={group_value}...")
        
        # 构建包含分组值的查询
        group_query = f"{query_string} AND {group_by_field}:{group_value}"
        
        split_result = client.call_tool(
            "bkmonitor-log-bkop",
            "analyze_field",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "field_name": split_by_field,
                    "query_string": group_query,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "group_by": "true",
                    "order_by": "value",
                    "limit": "50"
                }
            }
        )
        
        # 组织结果
        distribution = {}
        total = 0
        if "data" in split_result and "list" in split_result["data"]:
            for item in split_result["data"]["list"]:
                key = str(item.get("name") or item.get("key", ""))
                value = item.get("value", 0)
                distribution[key] = value
                total += value
        
        results[group_value] = {
            "distribution": distribution,
            "total": total
        }
    
    # 步骤3: 生成报告
    print("\n步骤3: 生成分析报告...")
    print("\n" + "=" * 80)
    print("日志多维度分析报告")
    print("=" * 80)
    print(f"\n分析配置:")
    print(f"  业务ID: {bk_biz_id}")
    print(f"  索引集ID: {index_set_id}")
    print(f"  过滤条件: {filter_fields}")
    print(f"  分组字段: {group_by_field}")
    print(f"  拆分字段: {split_by_field}")
    print(f"  时间范围: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))} ~ {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    
    # 汇总统计
    overall_total = sum(r["total"] for r in results.values())
    split_summary = {}
    for r in results.values():
        for k, v in r["distribution"].items():
            split_summary[k] = split_summary.get(k, 0) + v
    
    print(f"\n汇总统计:")
    print(f"  总分组数: {len(results)}")
    print(f"  总日志数: {overall_total}")
    if split_summary:
        print(f"\n  按 {split_by_field} 汇总:")
        for k, v in sorted(split_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"    {k}: {v}")
    
    # 详细结果
    print(f"\n详细分析结果:")
    print("-" * 80)
    for group_value, group_data in sorted(results.items()):
        print(f"\n[{group_by_field}: {group_value}]")
        print(f"  总日志数: {group_data['total']}")
        if group_data["distribution"]:
            print(f"  按 {split_by_field} 分布:")
            for split_value, count in sorted(group_data["distribution"].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / group_data['total']) * 100 if group_data['total'] > 0 else 0
                print(f"    {split_value}: {count} ({percentage:.1f}%)")
    
    print("\n" + "=" * 80)
    
    # 保存结果到文件
    output_file = f"log_analysis_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "analysis_config": {
                "bk_biz_id": bk_biz_id,
                "index_set_id": index_set_id,
                "filter_fields": filter_fields,
                "group_by_field": group_by_field,
                "split_by_field": split_by_field,
                "time_range": {
                    "start_time": start_time,
                    "end_time": end_time
                }
            },
            "results": results,
            "summary": {
                "total_groups": len(results),
                "overall_total": overall_total,
                "split_field_summary": split_summary
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")


if __name__ == "__main__":
    example_multi_dimensional_analysis()


