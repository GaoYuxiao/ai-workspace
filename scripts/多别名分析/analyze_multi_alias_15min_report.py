#!/usr/bin/env python3
"""
分析多别名设置验证索引集近15分钟日志并生成报告
"""
import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

def analyze_logs_and_generate_report(logs_data, bk_biz_id, index_set_id, start_time, end_time):
    """分析日志数据并生成报告"""
    
    logs = logs_data.get('list', [])
    total_logs = logs_data.get('total', len(logs))
    
    # 统计信息
    level_counter = Counter()
    code_position_counter = Counter()
    server_ip_counter = Counter()
    result_table_counter = Counter()
    
    # 错误和警告详情
    critical_issues = []
    error_issues = []
    warning_issues = []
    
    # 按时间分布
    time_distribution = defaultdict(int)
    
    for log in logs:
        # 统计日志级别
        level = log.get('lvl') or log.get('level', 'UNKNOWN')
        level_counter[level] += 1
        
        # 统计代码位置
        code_pos = log.get('code_position') or log.get('code_file', 'unknown')
        code_position_counter[code_pos] += 1
        
        # 统计服务器IP
        server_ip = log.get('serverIp', 'unknown')
        server_ip_counter[server_ip] += 1
        
        # 统计结果表
        result_table = log.get('__result_table', 'unknown')
        result_table_counter[result_table] += 1
        
        # 时间分布（按分钟）
        dt_time = log.get('dtEventTimeStamp') or log.get('_time', '')
        if dt_time:
            try:
                if isinstance(dt_time, str):
                    if len(dt_time) == 13:  # 毫秒时间戳
                        timestamp = int(dt_time) / 1000
                    else:
                        timestamp = int(dt_time)
                else:
                    timestamp = int(dt_time) / 1000 if dt_time > 1e10 else int(dt_time)
                
                time_key = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                time_distribution[time_key] += 1
            except:
                pass
        
        # 收集问题详情
        content = log.get('content') or log.get('message', '')
        log_time = log.get('data_time') or log.get('dtEventTimeStamp', '')
        
        issue_info = {
            'level': level,
            'code_position': code_pos,
            'content': content,
            'time': log_time,
            'serverIp': server_ip,
            'result_table': result_table
        }
        
        if level == 'CRITICAL':
            critical_issues.append(issue_info)
        elif level == 'ERROR':
            error_issues.append(issue_info)
        elif level == 'WARNING':
            warning_issues.append(issue_info)
    
    # 生成报告
    report_lines = []
    report_lines.append("# 多别名设置验证索引集 - 近15分钟日志分析报告\n")
    report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"**业务ID**: {bk_biz_id}\n")
    report_lines.append(f"**索引集ID**: {index_set_id}\n")
    report_lines.append(f"**查询时间范围**: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} ~ {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"**总日志数**: {total_logs} (本次查询: {len(logs)})\n")
    report_lines.append("\n---\n")
    
    # 1. 日志级别分布
    report_lines.append("## 1. 日志级别分布\n")
    report_lines.append("| 级别 | 数量 | 占比 |\n")
    report_lines.append("|------|------|------|\n")
    total_analyzed = sum(level_counter.values())
    for level, count in level_counter.most_common():
        percentage = (count / total_analyzed * 100) if total_analyzed > 0 else 0
        report_lines.append(f"| {level} | {count} | {percentage:.2f}% |\n")
    report_lines.append("\n")
    
    # 2. 代码位置分布（Top 10）
    report_lines.append("## 2. 代码位置分布（Top 10）\n")
    report_lines.append("| 代码位置 | 日志数量 |\n")
    report_lines.append("|----------|----------|\n")
    for code_pos, count in code_position_counter.most_common(10):
        report_lines.append(f"| {code_pos} | {count} |\n")
    report_lines.append("\n")
    
    # 3. 服务器IP分布
    report_lines.append("## 3. 服务器IP分布\n")
    report_lines.append("| 服务器IP | 日志数量 |\n")
    report_lines.append("|----------|----------|\n")
    for ip, count in server_ip_counter.most_common():
        report_lines.append(f"| {ip} | {count} |\n")
    report_lines.append("\n")
    
    # 4. 结果表分布
    report_lines.append("## 4. 结果表分布\n")
    report_lines.append("| 结果表 | 日志数量 |\n")
    report_lines.append("|--------|----------|\n")
    for rt, count in result_table_counter.most_common():
        rt_name = rt.split('.')[-1] if '.' in rt else rt
        report_lines.append(f"| {rt_name} | {count} |\n")
    report_lines.append("\n")
    
    # 5. 严重问题分析（CRITICAL级别）
    report_lines.append("## 5. 严重问题分析（CRITICAL级别）\n")
    report_lines.append(f"**共发现 {len(critical_issues)} 条严重问题**\n\n")
    
    if critical_issues:
        # 按问题类型分组
        critical_by_type = defaultdict(list)
        for issue in critical_issues[:20]:  # 取前20个
            key = issue['content'][:50] if issue['content'] else 'Unknown'
            critical_by_type[key].append(issue)
        
        report_lines.append("### 5.1 主要严重问题类型\n")
        for issue_type, issues in list(critical_by_type.items())[:10]:
            report_lines.append(f"#### {issue_type}\n")
            report_lines.append(f"**出现次数**: {len(issues)}\n")
            report_lines.append("**详情**:\n")
            for issue in issues[:3]:  # 每个类型显示3个示例
                report_lines.append(f"- **时间**: {issue['time']}\n")
                report_lines.append(f"  - **代码位置**: {issue['code_position']}\n")
                report_lines.append(f"  - **服务器**: {issue['serverIp']}\n")
                report_lines.append(f"  - **内容**: {issue['content']}\n")
            report_lines.append("\n")
    else:
        report_lines.append("✅ 未发现严重问题\n\n")
    
    # 6. 错误问题分析（ERROR级别）
    report_lines.append("## 6. 错误问题分析（ERROR级别）\n")
    report_lines.append(f"**共发现 {len(error_issues)} 条错误**\n\n")
    
    if error_issues:
        # 按错误类型分组
        error_by_type = defaultdict(list)
        for issue in error_issues[:30]:  # 取前30个
            content = issue['content']
            if 'Database connection' in content:
                key = 'Database connection errors'
            elif 'User authentication failed' in content:
                key = 'User authentication failures'
            elif 'File upload failed' in content:
                key = 'File upload failures'
            elif 'Payment interface' in content:
                key = 'Payment interface errors'
            elif 'Data processing exception' in content:
                key = 'Data processing exceptions'
            else:
                key = content[:40] if content else 'Unknown error'
            error_by_type[key].append(issue)
        
        report_lines.append("### 6.1 主要错误类型\n")
        for error_type, errors in list(error_by_type.items())[:10]:
            report_lines.append(f"#### {error_type}\n")
            report_lines.append(f"**出现次数**: {len(errors)}\n")
            report_lines.append("**示例**:\n")
            for error in errors[:2]:  # 每个类型显示2个示例
                report_lines.append(f"- **时间**: {error['time']}\n")
                report_lines.append(f"  - **代码位置**: {error['code_position']}\n")
                report_lines.append(f"  - **内容**: {error['content']}\n")
            report_lines.append("\n")
    else:
        report_lines.append("✅ 未发现错误\n\n")
    
    # 7. 警告问题分析（WARNING级别）
    report_lines.append("## 7. 警告问题分析（WARNING级别）\n")
    report_lines.append(f"**共发现 {len(warning_issues)} 条警告**\n\n")
    
    if warning_issues:
        # 按警告类型分组
        warning_by_type = defaultdict(list)
        for issue in warning_issues[:30]:  # 取前30个
            content = issue['content']
            if 'API call frequency too high' in content:
                key = 'API call frequency too high'
            elif 'Disk space low' in content:
                key = 'Disk space low'
            elif 'Cache space insufficient' in content:
                key = 'Cache space insufficient'
            elif 'Database connection timeout' in content:
                key = 'Database connection timeout'
            elif 'External service response slow' in content:
                key = 'External service response slow'
            else:
                key = content[:40] if content else 'Unknown warning'
            warning_by_type[key].append(issue)
        
        report_lines.append("### 7.1 主要警告类型\n")
        for warning_type, warnings in list(warning_by_type.items())[:10]:
            report_lines.append(f"#### {warning_type}\n")
            report_lines.append(f"**出现次数**: {len(warnings)}\n")
            report_lines.append("**示例**:\n")
            for warning in warnings[:2]:  # 每个类型显示2个示例
                report_lines.append(f"- **时间**: {warning['time']}\n")
                report_lines.append(f"  - **代码位置**: {warning['code_position']}\n")
                report_lines.append(f"  - **内容**: {warning['content']}\n")
            report_lines.append("\n")
    else:
        report_lines.append("✅ 未发现警告\n\n")
    
    # 8. 时间分布
    if time_distribution:
        report_lines.append("## 8. 日志时间分布\n")
        report_lines.append("| 时间 | 日志数量 |\n")
        report_lines.append("|------|----------|\n")
        for time_key in sorted(time_distribution.keys()):
            report_lines.append(f"| {time_key} | {time_distribution[time_key]} |\n")
        report_lines.append("\n")
    
    # 9. 关键发现和建议
    report_lines.append("## 9. 关键发现和建议\n\n")
    
    # 分析关键发现
    findings = []
    
    if len(critical_issues) > 0:
        findings.append(f"⚠️ **发现 {len(critical_issues)} 条严重问题**，需要立即关注")
    
    if len(error_issues) > 0:
        findings.append(f"❌ **发现 {len(error_issues)} 条错误**，需要排查")
    
    # 检查特定问题
    db_errors = sum(1 for e in error_issues if 'Database' in e['content'])
    if db_errors > 0:
        findings.append(f"🔴 **数据库相关问题**: {db_errors} 条，包括连接失败、超时、主从同步失败等")
    
    auth_errors = sum(1 for e in error_issues if 'authentication' in e['content'].lower())
    if auth_errors > 0:
        findings.append(f"🔐 **认证失败问题**: {auth_errors} 条，可能存在安全风险")
    
    payment_errors = sum(1 for e in error_issues + critical_issues if 'Payment' in e['content'])
    if payment_errors > 0:
        findings.append(f"💳 **支付系统问题**: {payment_errors} 条，包括支付接口异常、支付系统不可用等")
    
    disk_warnings = sum(1 for w in warning_issues if 'Disk space' in w['content'])
    if disk_warnings > 0:
        findings.append(f"💾 **磁盘空间警告**: {disk_warnings} 条，磁盘使用率较高")
    
    api_freq_warnings = sum(1 for w in warning_issues if 'API call frequency' in w['content'])
    if api_freq_warnings > 0:
        findings.append(f"📊 **API调用频率过高**: {api_freq_warnings} 条，可能存在性能问题")
    
    for finding in findings:
        report_lines.append(f"- {finding}\n")
    
    report_lines.append("\n### 建议措施\n\n")
    report_lines.append("1. **立即处理严重问题**: 优先处理CRITICAL级别的问题，特别是核心服务崩溃、数据库主从同步失败等\n")
    report_lines.append("2. **排查数据库连接**: 检查数据库连接池配置、网络连接状态、数据库服务状态\n")
    report_lines.append("3. **检查认证系统**: 排查用户认证失败的原因，检查认证服务是否正常\n")
    report_lines.append("4. **监控支付系统**: 关注支付系统的可用性和接口调用情况\n")
    report_lines.append("5. **优化资源使用**: 关注磁盘空间、缓存使用情况，及时清理和扩容\n")
    report_lines.append("6. **性能优化**: 对于API调用频率过高的问题，考虑限流和优化\n")
    report_lines.append("\n")
    
    # 10. 相关资源
    report_lines.append("## 10. 相关资源\n\n")
    report_lines.append("### 10.1 涉及的结果表\n")
    for rt, count in result_table_counter.most_common():
        rt_name = rt.split('.')[-1] if '.' in rt else rt
        report_lines.append(f"- **{rt_name}**: {count} 条日志\n")
    report_lines.append("\n")
    
    report_lines.append("### 10.2 涉及的服务器\n")
    for ip, count in server_ip_counter.most_common():
        report_lines.append(f"- **{ip}**: {count} 条日志\n")
    report_lines.append("\n")
    
    report_lines.append("### 10.3 主要代码模块\n")
    for code_pos, count in code_position_counter.most_common(10):
        report_lines.append(f"- **{code_pos}**: {count} 条日志\n")
    report_lines.append("\n")
    
    report_lines.append("---\n")
    report_lines.append(f"*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    return ''.join(report_lines)

if __name__ == "__main__":
    print("分析脚本已准备就绪")

