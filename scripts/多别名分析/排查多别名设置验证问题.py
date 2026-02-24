#!/usr/bin/env python3
"""
排查多别名设置验证近15分钟问题
"""
import sys
import time
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# 添加路径
sys.path.append('skill/mcp-data-fetcher/scripts')
from mcp_data_fetcher import MCPClient

def main():
    # 初始化MCP客户端
    client = MCPClient()
    
    # 配置参数
    bk_biz_id = "2"
    index_set_id = "2545"  # 多别名设置验证
    
    # 时间范围：近15分钟
    end_time = int(time.time())
    start_time = end_time - 15 * 60
    
    print(f"🔍 开始排查多别名设置验证近15分钟问题")
    print(f"时间范围: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} ~ {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"业务ID: {bk_biz_id}, 索引集ID: {index_set_id}")
    print()
    
    # 1. 查询日志级别分布
    print("📊 步骤1: 查询日志级别分布...")
    try:
        level_result = client.call_tool(
            "bkmonitor-log-bkop",
            "analyze_field",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "field_name": "level",
                    "query_string": "*",
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "group_by": "true",
                    "order_by": "value",
                    "limit": "50"
                }
            }
        )
        print(f"✅ 日志级别分析完成")
        print(json.dumps(level_result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ 日志级别分析失败: {e}")
        level_result = None
    
    print()
    
    # 2. 查询错误日志
    print("📊 步骤2: 查询错误日志...")
    try:
        error_logs_result = client.call_tool(
            "bkmonitor-log-bkop",
            "search_logs",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "query_string": "level:(ERROR OR CRITICAL OR WARNING)",
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "limit": "200"
                }
            }
        )
        print(f"✅ 错误日志查询完成")
        if error_logs_result and "result" in error_logs_result:
            logs = error_logs_result["result"].get("list", [])
            print(f"   找到 {len(logs)} 条错误日志")
    except Exception as e:
        print(f"❌ 错误日志查询失败: {e}")
        error_logs_result = None
    
    print()
    
    # 3. 分析服务器IP分布
    print("📊 步骤3: 分析服务器IP分布...")
    try:
        ip_result = client.call_tool(
            "bkmonitor-log-bkop",
            "analyze_field",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "field_name": "serverIp",
                    "query_string": "*",
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "group_by": "true",
                    "order_by": "value",
                    "limit": "50"
                }
            }
        )
        print(f"✅ 服务器IP分析完成")
        if ip_result and "result" in ip_result:
            ip_data = ip_result["result"].get("list", [])
            print(f"   发现 {len(ip_data)} 个服务器IP")
            for item in ip_data[:5]:
                print(f"   - {item.get('value', 'N/A')}: {item.get('count', 0)} 条日志")
    except Exception as e:
        print(f"❌ 服务器IP分析失败: {e}")
        ip_result = None
    
    print()
    
    # 4. 查询监控指标（如果有IP地址）
    if ip_result and "result" in ip_result:
        ip_data = ip_result["result"].get("list", [])
        if ip_data:
            target_ip = ip_data[0].get("value")  # 使用日志最多的IP
            print(f"📊 步骤4: 查询服务器 {target_ip} 的监控指标...")
            
            # 查询CPU使用率
            try:
                cpu_result = client.call_tool(
                    "bkmonitor-metrics-bkop",
                    "execute_range_query",
                    {
                        "body_param": {
                            "bk_biz_id": bk_biz_id,
                            "promql": f'avg(avg_over_time(bkmonitor:system:cpu_summary:usage{{ip="{target_ip}"}}[1m]))',
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "step": "1m"
                        }
                    }
                )
                print(f"✅ CPU使用率查询完成")
            except Exception as e:
                print(f"❌ CPU使用率查询失败: {e}")
                cpu_result = None
            
            # 查询内存使用率
            try:
                mem_result = client.call_tool(
                    "bkmonitor-metrics-bkop",
                    "execute_range_query",
                    {
                        "body_param": {
                            "bk_biz_id": bk_biz_id,
                            "promql": f'avg(avg_over_time(bkmonitor:system:mem:pct_used{{ip="{target_ip}"}}[1m]))',
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "step": "1m"
                        }
                    }
                )
                print(f"✅ 内存使用率查询完成")
            except Exception as e:
                print(f"❌ 内存使用率查询失败: {e}")
                mem_result = None
            
            # 查询磁盘使用率
            try:
                disk_result = client.call_tool(
                    "bkmonitor-metrics-bkop",
                    "execute_range_query",
                    {
                        "body_param": {
                            "bk_biz_id": bk_biz_id,
                            "promql": f'avg(avg_over_time(bkmonitor:system:disk:in_use{{ip="{target_ip}"}}[1m]))',
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "step": "1m"
                        }
                    }
                )
                print(f"✅ 磁盘使用率查询完成")
            except Exception as e:
                print(f"❌ 磁盘使用率查询失败: {e}")
                disk_result = None
    
    print()
    print("=" * 80)
    print("数据收集完成！")
    print("=" * 80)
    
    # 保存结果
    result_data = {
        "timestamp": end_time,
        "time_range": {
            "start": start_time,
            "end": end_time,
            "start_str": datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
            "end_str": datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        },
        "config": {
            "bk_biz_id": bk_biz_id,
            "index_set_id": index_set_id
        },
        "level_distribution": level_result,
        "error_logs": error_logs_result,
        "ip_distribution": ip_result
    }
    
    output_file = f"多别名设置验证_排查结果_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 结果已保存: {output_file}")
    
    return result_data

if __name__ == "__main__":
    main()

