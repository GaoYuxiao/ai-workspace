#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成监控指标可视化图表
"""

import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 监控数据（从之前的查询结果中提取）
metrics_data = {
    'cpu_usage': {
        'timestamps': [1766061300000, 1766061360000, 1766061420000, 1766061480000, 1766061540000, 
                       1766061600000, 1766061660000, 1766061720000, 1766061780000, 1766061840000,
                       1766061900000, 1766061960000, 1766062020000, 1766062080000, 1766062140000],
        'values': [22.004299884661922, 21.009449147511578, 19.613151858785688, 20.16161172800541, 19.636535496699377,
                   21.787150702826967, 21.106447791603703, 22.845051078301402, 21.74999046666921, 20.558700746032237,
                   22.00932683676484, 20.65330642888566, 20.490411987362076, 21.04561200330678, 20.724942444961016],
        'title': 'CPU使用率',
        'unit': '%',
        'y_label': 'CPU使用率 (%)'
    },
    'mem_usage': {
        'timestamps': [1766061300000, 1766061360000, 1766061420000, 1766061480000, 1766061540000,
                       1766061600000, 1766061660000, 1766061720000, 1766061780000, 1766061840000,
                       1766061900000, 1766061960000, 1766062020000, 1766062080000, 1766062140000],
        'values': [43.86085381728131, 43.82837904938664, 43.79482250288696, 43.68615581249095, 43.642102555853825,
                   43.487359463672774, 43.49129876780759, 43.614945340195774, 43.83897796416427, 43.767283604613134,
                   43.766798532111714, 43.71743151681536, 43.729353060373285, 43.83432248970048, 43.7414405707363],
        'title': '内存使用率',
        'unit': '%',
        'y_label': '内存使用率 (%)'
    },
    'disk_usage': {
        'timestamps': [1766061300000, 1766061360000, 1766061420000, 1766061480000, 1766061540000,
                       1766061600000, 1766061660000, 1766061720000, 1766061780000, 1766061840000,
                       1766061900000, 1766061960000, 1766062020000, 1766062080000, 1766062140000],
        'values': [34.24016744712, 34.19246575142935, 34.18966751910068, 34.18155910557711, 34.1843446949694,
                   34.18013356527599, 34.18334365284927, 34.183134783032024, 34.18267068371213, 34.18536848106956,
                   34.186323158546344, 34.19266527626287, 34.18698242549268, 34.1817868660297, 34.18108230464993],
        'title': '磁盘使用率',
        'unit': '%',
        'y_label': '磁盘使用率 (%)'
    },
    'disk_io': {
        'timestamps': [1766061300000, 1766061360000, 1766061420000, 1766061480000, 1766061540000,
                       1766061600000, 1766061660000, 1766061720000, 1766061780000, 1766061840000,
                       1766061900000, 1766061960000, 1766062020000, 1766062080000, 1766062140000],
        'values': [0.01940729066447262, 0.019327040093893598, 0.018578229505892798, 0.01747614731140916, 0.01803132923393467,
                   0.01875578727896595, 0.02067487945356374, 0.018695455773599202, 0.01789428192000302, 0.01870817215330273,
                   0.018940343748193138, 0.020125829853322875, 0.01910876011425314, 0.018712110410735196, 0.018442011670945793],
        'title': '磁盘IO使用率',
        'unit': '%',
        'y_label': '磁盘IO使用率 (%)'
    }
}

def generate_chart(metric_key, metric_info, output_dir):
    """生成单个指标图表"""
    try:
        # 转换时间戳（毫秒转秒）
        timestamps = [ts / 1000 for ts in metric_info['timestamps']]
        values = metric_info['values']
        
        # 转换为datetime对象
        dt_timestamps = [datetime.fromtimestamp(ts) for ts in timestamps]
        
        # 创建图表
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dt_timestamps, values, linewidth=2.5, color='#1f77b4', marker='o', markersize=4)
        ax.set_title(f"{metric_info['title']} - 30.189.38.149", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel(metric_info['y_label'], fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 添加平均值线
        avg_value = sum(values) / len(values)
        ax.axhline(y=avg_value, color='r', linestyle='--', linewidth=1.5, alpha=0.7, label=f'平均值: {avg_value:.2f}{metric_info["unit"]}')
        ax.legend(loc='upper right')
        
        # 格式化时间轴
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图片
        output_path = output_dir / f"{metric_key}.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ 已生成图表: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"❌ 生成图表失败 ({metric_key}): {e}")
        return None

def generate_all_charts():
    """生成所有指标图表"""
    output_dir = Path(__file__).parent / "metrics_charts"
    output_dir.mkdir(exist_ok=True)
    
    chart_paths = {}
    for metric_key, metric_info in metrics_data.items():
        chart_path = generate_chart(metric_key, metric_info, output_dir)
        if chart_path:
            chart_paths[metric_key] = chart_path
    
    return chart_paths

if __name__ == "__main__":
    print("开始生成监控指标图表...")
    chart_paths = generate_all_charts()
    print(f"\n✅ 共生成 {len(chart_paths)} 个图表")
    print(f"📁 图表保存目录: {Path(__file__).parent / 'metrics_charts'}")

