#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成错误统计可视化图表
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 错误统计数据
error_levels = {
    'CRITICAL': 30,
    'ERROR': 40,
    'WARNING': 50
}

error_types = {
    '支付系统不可用': 10,
    '数据库主从同步失败': 5,
    '系统内存不足': 5,
    '核心服务崩溃': 5,
    '安全漏洞异常访问': 4,
    '数据库连接失败/超时': 20,
    '磁盘空间不足': 5,
    '用户认证失败': 10,
    '文件上传失败': 5,
    'API调用频率过高': 3,
    '外部服务响应慢': 8
}

def generate_error_level_chart(output_dir):
    """生成错误级别分布饼图"""
    try:
        labels = list(error_levels.keys())
        sizes = list(error_levels.values())
        colors = ['#dc3545', '#fd7e14', '#ffc107']  # 红色、橙色、黄色
        
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                          startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        # 设置百分比文字颜色
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
        
        ax.set_title('错误级别分布（近15分钟）', fontsize=16, fontweight='bold', pad=20)
        
        # 添加图例
        ax.legend(wedges, [f'{label}: {size}条' for label, size in zip(labels, sizes)],
                 title="错误级别", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.tight_layout()
        
        output_path = output_dir / "error_levels.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 已生成错误级别图表: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"❌ 生成错误级别图表失败: {e}")
        return None

def generate_error_type_chart(output_dir):
    """生成错误类型分布柱状图"""
    try:
        # 按出现次数排序
        sorted_types = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in sorted_types]
        values = [item[1] for item in sorted_types]
        
        # 根据严重程度设置颜色
        colors = []
        for label in labels:
            if label in ['支付系统不可用', '数据库主从同步失败', '系统内存不足', '核心服务崩溃', '安全漏洞异常访问']:
                colors.append('#dc3545')  # 红色 - 严重
            elif label in ['数据库连接失败/超时']:
                colors.append('#fd7e14')  # 橙色 - 高
            else:
                colors.append('#ffc107')  # 黄色 - 中
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.barh(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        
        # 添加数值标签
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(value + 0.5, i, f'{value}次', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('出现次数', fontsize=12, fontweight='bold')
        ax.set_title('错误类型分布（近15分钟）', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        output_path = output_dir / "error_types.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 已生成错误类型图表: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"❌ 生成错误类型图表失败: {e}")
        return None

if __name__ == "__main__":
    output_dir = Path(__file__).parent / "metrics_charts"
    output_dir.mkdir(exist_ok=True)
    
    print("开始生成错误统计图表...")
    generate_error_level_chart(output_dir)
    generate_error_type_chart(output_dir)
    print("✅ 错误统计图表生成完成")


