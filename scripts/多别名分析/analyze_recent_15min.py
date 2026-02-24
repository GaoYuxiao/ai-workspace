#!/usr/bin/env python3
"""
排查多别名设置验证近15分钟问题
"""
import sys
import time
import json
from pathlib import Path

# 添加路径
sys.path.append('skill/log-multi-dimensional-analyzer/scripts')
sys.path.append('skill/mcp-data-fetcher/scripts')

from log_multi_dimensional_analyzer import LogMultiDimensionalAnalyzer
from mcp_data_fetcher import MCPClient

def main():
    # 初始化MCP客户端
    client = MCPClient()
    
    # 配置参数
    bk_biz_id = "2"
    index_set_id = "2545"  # 多别名设置验证
    filter_fields = {}  # 不设置过滤条件，查询所有日志
    group_by_field = "code_file"
    split_by_field = "level"
    
    # 时间范围：近15分钟
    end_time = int(time.time())
    start_time = end_time - 15 * 60
    
    print(f"🔍 开始排查多别名设置验证近15分钟问题")
    print(f"时间范围: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))} ~ {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"索引集ID: {index_set_id}")
    print()
    
    # 创建分析器
    analyzer = LogMultiDimensionalAnalyzer(
        mcp_client=client,
        enable_metrics_query=True,
        metrics_output_dir="metrics_charts"
    )
    
    # 执行多维度分析
    print("📊 步骤1: 执行日志多维度分析...")
    result = analyzer.analyze_multi_dimensional(
        bk_biz_id=bk_biz_id,
        index_set_id=index_set_id,
        filter_fields=filter_fields,
        group_by_field=group_by_field,
        split_by_field=split_by_field,
        start_time=start_time,
        end_time=end_time
    )
    
    print(f"✅ 日志分析完成，共分析 {len(result.get('groups', {}))} 个分组")
    print()
    
    # 生成Markdown报告
    print("📝 步骤2: 生成分析报告...")
    report = analyzer.format_output(
        result,
        format_type="markdown",
        auto_query_metrics=True
    )
    
    # 保存报告
    report_file = f"多别名设置验证_近15分钟问题排查报告_{int(time.time())}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已保存: {report_file}")
    print()
    print("=" * 80)
    print("分析完成！")
    print("=" * 80)
    
    return report_file

if __name__ == "__main__":
    main()


