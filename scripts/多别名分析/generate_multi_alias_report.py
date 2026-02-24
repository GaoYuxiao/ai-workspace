#!/usr/bin/env python3
"""
生成多别名设置验证索引集近15分钟日志分析报告
直接使用MCP查询结果
"""
import json
import time
import sys
from datetime import datetime
from pathlib import Path

# 添加路径以导入分析模块
sys.path.insert(0, str(Path(__file__).parent))
from analyze_multi_alias_15min_report import analyze_logs_and_generate_report

# 这里需要从MCP查询结果中获取日志数据
# 由于日志数据在之前的工具调用中，我们创建一个脚本来重新查询并分析

def main():
    print("=" * 80)
    print("多别名设置验证索引集 - 近15分钟日志分析")
    print("=" * 80)
    print()
    
    # 参数配置
    bk_biz_id = "2"
    index_set_id = "2545"
    end_time = int(time.time())
    start_time = end_time - 15 * 60
    
    print(f"📋 查询参数:")
    print(f"  - 业务ID: {bk_biz_id}")
    print(f"  - 索引集ID: {index_set_id}")
    print(f"  - 时间范围: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')} ~ {datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("⚠️  注意: 此脚本需要从MCP查询结果中获取日志数据")
    print("   请使用MCP工具查询日志后，将结果传递给分析函数")
    print()
    
    # 这里应该调用MCP工具查询日志
    # 由于日志数据已经在之前的工具调用中获取，我们可以：
    # 1. 将日志数据保存到文件
    # 2. 从文件读取并分析
    # 3. 或者直接使用内存中的数据
    
    print("💡 提示: 使用以下方式之一获取日志数据:")
    print("   1. 通过MCP工具查询日志")
    print("   2. 从保存的JSON文件中读取")
    print("   3. 直接使用内存中的查询结果")
    print()
    
    return {
        'bk_biz_id': bk_biz_id,
        'index_set_id': index_set_id,
        'start_time': start_time,
        'end_time': end_time
    }

if __name__ == "__main__":
    main()

