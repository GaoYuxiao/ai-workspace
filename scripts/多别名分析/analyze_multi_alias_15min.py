#!/usr/bin/env python3
"""
查询并分析"多别名设置验证"索引集近15分钟的日志，生成分析报告
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

def format_timestamp(ts):
    """格式化时间戳"""
    return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

def analyze_logs():
    """分析日志"""
    # 初始化MCP客户端
    client = MCPClient()
    
    # 配置参数
    bk_biz_id = "2"
    index_set_id = "2545"  # 多别名设置验证
    
    # 时间范围：近15分钟
    end_time = int(time.time())
    start_time = end_time - 15 * 60
    
    print(f"🔍 开始分析多别名设置验证索引集近15分钟日志")
    print(f"时间范围: {format_timestamp(start_time)} ~ {format_timestamp(end_time)}")
    print(f"业务ID: {bk_biz_id}, 索引集ID: {index_set_id}")
    print()
    
    results = {
        "timestamp": end_time,
        "time_range": {
            "start": start_time,
            "end": end_time,
            "start_str": format_timestamp(start_time),
            "end_str": format_timestamp(end_time)
        },
        "config": {
            "bk_biz_id": bk_biz_id,
            "index_set_id": index_set_id
        }
    }
    
    # 1. 查询总日志数
    print("📊 步骤1: 查询总日志数...")
    try:
        total_logs_result = client.call_tool(
            "bkmonitor-log-bkop",
            "search_logs",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "query_string": "*",
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "limit": "1"
                }
            }
        )
        total_count = total_logs_result.get("result", {}).get("total", 0)
        print(f"✅ 总日志数: {total_count}")
        results["total_logs"] = total_count
    except Exception as e:
        print(f"❌ 查询总日志数失败: {e}")
        total_count = 0
    
    print()
    
    # 2. 查询日志级别分布
    print("📊 步骤2: 查询日志级别分布...")
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
        level_data = level_result.get("result", {}).get("list", [])
        print(f"   发现 {len(level_data)} 个日志级别")
        for item in level_data:
            print(f"   - {item.get('value', 'N/A')}: {item.get('count', 0)} 条")
        results["level_distribution"] = level_result
    except Exception as e:
        print(f"❌ 日志级别分析失败: {e}")
        results["level_distribution"] = None
    
    print()
    
    # 3. 查询错误日志详情
    print("📊 步骤3: 查询错误日志详情...")
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
        error_logs = error_logs_result.get("result", {}).get("list", [])
        print(f"✅ 错误日志查询完成，找到 {len(error_logs)} 条")
        results["error_logs"] = error_logs_result
    except Exception as e:
        print(f"❌ 错误日志查询失败: {e}")
        results["error_logs"] = None
    
    print()
    
    # 4. 分析服务器IP分布
    print("📊 步骤4: 分析服务器IP分布...")
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
        ip_data = ip_result.get("result", {}).get("list", [])
        print(f"✅ 服务器IP分析完成，发现 {len(ip_data)} 个服务器IP")
        for item in ip_data[:5]:
            print(f"   - {item.get('value', 'N/A')}: {item.get('count', 0)} 条日志")
        results["ip_distribution"] = ip_result
    except Exception as e:
        print(f"❌ 服务器IP分析失败: {e}")
        results["ip_distribution"] = None
    
    print()
    
    # 5. 分析code_file字段（如果有）
    print("📊 步骤5: 分析code_file字段分布...")
    try:
        code_file_result = client.call_tool(
            "bkmonitor-log-bkop",
            "analyze_field",
            {
                "body_param": {
                    "bk_biz_id": bk_biz_id,
                    "index_set_id": index_set_id,
                    "field_name": "code_file",
                    "query_string": "*",
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "group_by": "true",
                    "order_by": "value",
                    "limit": "50"
                }
            }
        )
        code_file_data = code_file_result.get("result", {}).get("list", [])
        print(f"✅ code_file分析完成，发现 {len(code_file_data)} 个文件")
        for item in code_file_data[:5]:
            print(f"   - {item.get('value', 'N/A')}: {item.get('count', 0)} 条日志")
        results["code_file_distribution"] = code_file_result
    except Exception as e:
        print(f"❌ code_file分析失败: {e}")
        results["code_file_distribution"] = None
    
    print()
    
    # 6. 查询监控指标（如果有IP地址）
    metrics_data = {}
    if results.get("ip_distribution"):
        ip_data = results["ip_distribution"].get("result", {}).get("list", [])
        if ip_data:
            target_ip = ip_data[0].get("value")  # 使用日志最多的IP
            print(f"📊 步骤6: 查询服务器 {target_ip} 的监控指标...")
            
            metrics_data["target_ip"] = target_ip
            
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
                metrics_data["cpu"] = cpu_result
            except Exception as e:
                print(f"❌ CPU使用率查询失败: {e}")
                metrics_data["cpu"] = None
            
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
                metrics_data["memory"] = mem_result
            except Exception as e:
                print(f"❌ 内存使用率查询失败: {e}")
                metrics_data["memory"] = None
            
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
                metrics_data["disk"] = disk_result
            except Exception as e:
                print(f"❌ 磁盘使用率查询失败: {e}")
                metrics_data["disk"] = None
            
            # 查询磁盘IO使用率
            try:
                disk_io_result = client.call_tool(
                    "bkmonitor-metrics-bkop",
                    "execute_range_query",
                    {
                        "body_param": {
                            "bk_biz_id": bk_biz_id,
                            "promql": f'avg(avg_over_time(bkmonitor:system:io:util{{ip="{target_ip}"}}[1m]))',
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "step": "1m"
                        }
                    }
                )
                print(f"✅ 磁盘IO使用率查询完成")
                metrics_data["disk_io"] = disk_io_result
            except Exception as e:
                print(f"❌ 磁盘IO使用率查询失败: {e}")
                metrics_data["disk_io"] = None
    
    results["metrics"] = metrics_data
    
    print()
    print("=" * 80)
    print("数据收集完成！")
    print("=" * 80)
    
    # 保存原始数据
    output_file = f"多别名设置验证_近15分钟分析数据_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 原始数据已保存: {output_file}")
    
    return results

def generate_report(results):
    """生成分析报告"""
    print("\n📝 生成分析报告...")
    
    time_range = results["time_range"]
    total_logs = results.get("total_logs", 0)
    
    # 分析日志级别
    level_data = []
    if results.get("level_distribution"):
        level_list = results["level_distribution"].get("result", {}).get("list", [])
        level_data = level_list
    
    # 分析code_file
    code_file_data = []
    if results.get("code_file_distribution"):
        code_file_list = results["code_file_distribution"].get("result", {}).get("list", [])
        code_file_data = code_file_list
    
    # 分析IP分布
    ip_data = []
    if results.get("ip_distribution"):
        ip_list = results["ip_distribution"].get("result", {}).get("list", [])
        ip_data = ip_list
    
    # 分析错误日志
    error_logs = []
    if results.get("error_logs"):
        error_logs = results["error_logs"].get("result", {}).get("list", [])
    
    # 统计各级别日志数量
    level_stats = {}
    for item in level_data:
        level = item.get("value", "UNKNOWN")
        count = item.get("count", 0)
        level_stats[level] = count
    
    # 统计各code_file的错误分布
    code_file_error_stats = defaultdict(lambda: {"CRITICAL": 0, "ERROR": 0, "WARNING": 0, "total": 0})
    for log in error_logs:
        code_file = log.get("code_file", "unknown")
        level = log.get("level", "UNKNOWN")
        code_file_error_stats[code_file]["total"] += 1
        if level in ["CRITICAL", "ERROR", "WARNING"]:
            code_file_error_stats[code_file][level] += 1
    
    # 生成报告
    report_lines = []
    report_lines.append("# 多别名设置验证 - 近15分钟日志分析报告\n")
    report_lines.append(f"**生成时间**: {format_timestamp(results['timestamp'])}")
    report_lines.append(f"**时间范围**: {time_range['start_str']} ~ {time_range['end_str']}")
    report_lines.append(f"**业务ID**: {results['config']['bk_biz_id']}")
    report_lines.append(f"**索引集ID**: {results['config']['index_set_id']} (多别名设置验证)")
    report_lines.append(f"**总日志数**: {total_logs}")
    report_lines.append(f"**分析维度**: {len(code_file_data)} 个 code_file\n")
    
    # 统计概览
    report_lines.append("## 统计概览\n")
    if level_stats:
        report_lines.append("| 类型 | 数量 | 占比 |")
        report_lines.append("|---|---|---|")
        for level, count in sorted(level_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_logs * 100) if total_logs > 0 else 0
            report_lines.append(f"| {level} | {count} | {percentage:.1f}% |")
        report_lines.append("")
    
    # 错误分布（按code_file）
    if code_file_error_stats:
        report_lines.append("## 错误分布（按code_file）\n")
        report_lines.append("| code_file | 总数 | CRITICAL | ERROR | WARNING |")
        report_lines.append("|---|---|---|---|---|")
        report_lines.append("")
        for code_file, stats in sorted(code_file_error_stats.items(), key=lambda x: x[1]["total"], reverse=True):
            report_lines.append(f"| {code_file} | {stats['total']} | {stats['CRITICAL']} | {stats['ERROR']} | {stats['WARNING']} |")
        report_lines.append("")
    
    # 服务器IP分布
    if ip_data:
        report_lines.append("## 服务器IP分布\n")
        report_lines.append("| IP地址 | 日志数量 | 占比 |")
        report_lines.append("|---|---|---|")
        for item in ip_data[:10]:
            ip = item.get("value", "N/A")
            count = item.get("count", 0)
            percentage = (count / total_logs * 100) if total_logs > 0 else 0
            report_lines.append(f"| {ip} | {count} | {percentage:.1f}% |")
        report_lines.append("")
    
    # 监控指标
    if results.get("metrics") and results["metrics"].get("target_ip"):
        target_ip = results["metrics"]["target_ip"]
        report_lines.append("## 监控指标\n")
        report_lines.append(f"**host**: {target_ip}\n")
        
        metrics_info = []
        for metric_name, metric_result in results["metrics"].items():
            if metric_name == "target_ip":
                continue
            if metric_result and "result" in metric_result:
                data = metric_result["result"].get("data", {}).get("result", [])
                if data and len(data) > 0:
                    values = []
                    for series in data:
                        if "values" in series:
                            for val in series["values"]:
                                if len(val) >= 2 and val[1] != "NaN":
                                    try:
                                        values.append(float(val[1]))
                                    except:
                                        pass
                    if values:
                        avg_val = sum(values) / len(values)
                        max_val = max(values)
                        min_val = min(values)
                        metric_display = {
                            "cpu": "CPU使用率",
                            "memory": "内存使用率",
                            "disk": "磁盘使用率",
                            "disk_io": "磁盘IO使用率"
                        }.get(metric_name, metric_name)
                        metrics_info.append((metric_display, avg_val, max_val, min_val))
        
        if metrics_info:
            report_lines.append("| 指标 | 平均值 | 最大值 | 最小值 |")
            report_lines.append("|---|---|---|---|")
            report_lines.append("")
            for metric_display, avg, max_v, min_v in metrics_info:
                report_lines.append(f"| {metric_display} | {avg:.2f} | {max_v:.2f} | {min_v:.2f} |")
            report_lines.append("")
    
    # 关键错误日志摘要
    if error_logs:
        report_lines.append("## 关键错误日志摘要\n")
        report_lines.append("| 时间 | 级别 | code_file | 日志内容 |")
        report_lines.append("|---|---|---|---|")
        for log in error_logs[:10]:
            timestamp = log.get("dtEventTimeStamp", 0)
            if isinstance(timestamp, str):
                try:
                    timestamp = int(timestamp) / 1000
                except:
                    timestamp = 0
            elif timestamp > 1e10:
                timestamp = timestamp / 1000
            time_str = format_timestamp(timestamp) if timestamp > 0 else "N/A"
            level = log.get("level", "UNKNOWN")
            code_file = log.get("code_file", "unknown")
            log_content = log.get("log", "")[:100]  # 截取前100字符
            report_lines.append(f"| {time_str} | {level} | {code_file} | {log_content} |")
        report_lines.append("")
    
    # 建议
    report_lines.append("## 分析建议\n")
    if level_stats.get("CRITICAL", 0) > 0:
        report_lines.append("- ⚠️ **发现CRITICAL级别日志**，建议立即检查相关服务状态")
    if level_stats.get("ERROR", 0) > 0:
        report_lines.append("- ⚠️ **发现ERROR级别日志**，建议检查错误日志详情，排查问题根源")
    if level_stats.get("WARNING", 0) > 0:
        report_lines.append("- ⚠️ **发现WARNING级别日志**，建议关注相关服务的运行状态")
    
    if code_file_error_stats:
        top_error_file = max(code_file_error_stats.items(), key=lambda x: x[1]["total"])
        report_lines.append(f"- 📍 **重点关注**: {top_error_file[0]} 文件产生了最多的错误日志（{top_error_file[1]['total']}条）")
    
    report_lines.append("")
    report_lines.append("---")
    report_lines.append(f"**报告生成时间**: {format_timestamp(results['timestamp'])}")
    report_lines.append(f"**索引集**: 多别名设置验证 (ID: {results['config']['index_set_id']})")
    
    report_content = "\n".join(report_lines)
    
    # 保存报告
    report_file = f"多别名设置验证_近15分钟日志分析报告_{int(time.time())}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ 分析报告已保存: {report_file}")
    
    return report_file, report_content

if __name__ == "__main__":
    try:
        # 分析日志
        results = analyze_logs()
        
        # 生成报告
        report_file, report_content = generate_report(results)
        
        print("\n" + "=" * 80)
        print("✅ 分析完成！")
        print("=" * 80)
        print(f"📄 报告文件: {report_file}")
        print("\n报告预览:")
        print("-" * 80)
        print(report_content[:1000] + "..." if len(report_content) > 1000 else report_content)
        
    except Exception as e:
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

