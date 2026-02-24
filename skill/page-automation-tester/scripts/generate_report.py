#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告生成工具
用于将测试结果JSON转换为可视化的HTML报告和Markdown报告
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, test_results_path: str, output_dir: str = None):
        """
        初始化报告生成器
        
        Args:
            test_results_path: 测试结果JSON文件路径
            output_dir: 输出目录，默认为test_results_path所在目录
        """
        self.test_results_path = Path(test_results_path)
        if not self.test_results_path.exists():
            raise FileNotFoundError(f"测试结果文件不存在: {test_results_path}")
        
        self.output_dir = Path(output_dir) if output_dir else self.test_results_path.parent
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载测试结果
        with open(self.test_results_path, 'r', encoding='utf-8') as f:
            self.test_results = json.load(f)
    
    def generate_html_report(self, output_path: Optional[str] = None) -> str:
        """
        生成HTML可视化报告
        
        Args:
            output_path: 输出文件路径，默认为 {test_name}_report.html
            
        Returns:
            生成的HTML文件路径
        """
        if output_path is None:
            test_name = self.test_results.get('test_name', 'test_report')
            output_path = self.output_dir / f"{test_name}_visualization.html"
        else:
            output_path = Path(output_path)
        
        html_content = self._generate_html_content()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML报告已生成: {output_path}")
        return str(output_path)
    
    def generate_markdown_report(self, output_path: Optional[str] = None) -> str:
        """
        生成Markdown报告
        
        Args:
            output_path: 输出文件路径，默认为 {test_name}_report.md
            
        Returns:
            生成的Markdown文件路径
        """
        if output_path is None:
            test_name = self.test_results.get('test_name', 'test_report')
            output_path = self.output_dir / f"{test_name}_report.md"
        else:
            output_path = Path(output_path)
        
        md_content = self._generate_markdown_content()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Markdown报告已生成: {output_path}")
        return str(output_path)
    
    def _generate_html_content(self) -> str:
        """生成HTML内容"""
        test_name = self.test_results.get('test_name', '测试报告')
        description = self.test_results.get('description', '')
        test_cases = self.test_results.get('test_cases', [])
        
        # 统计信息
        total_tests = len(test_cases)
        passed = sum(1 for tc in test_cases if tc.get('status') == 'passed')
        failed = sum(1 for tc in test_cases if tc.get('status') == 'failed')
        partial = sum(1 for tc in test_cases if tc.get('status') == 'partial')
        skipped = sum(1 for tc in test_cases if tc.get('status') == 'skipped')
        executed = total_tests - skipped
        pass_rate = (passed / executed * 100) if executed > 0 else 0
        
        # 生成测试用例HTML
        test_cases_html = self._generate_test_cases_html(test_cases)
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{test_name} - 可视化测试报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .meta {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 15px;
        }}

        .header .meta span {{
            margin: 0 15px;
        }}

        .content {{
            padding: 40px;
        }}

        .overview {{
            margin-bottom: 40px;
        }}

        .overview h2 {{
            color: #333;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .stat-card .label {{
            font-size: 1em;
            opacity: 0.9;
        }}

        .table-container {{
            overflow-x: auto;
            margin-top: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}

        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .status-passed {{
            color: #28a745;
            font-weight: bold;
        }}

        .status-failed {{
            color: #dc3545;
            font-weight: bold;
        }}

        .status-partial {{
            color: #ffc107;
            font-weight: bold;
        }}

        .status-skipped {{
            color: #6c757d;
            font-weight: bold;
        }}

        .test-case {{
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .test-case-header {{
            background: #f8f9fa;
            padding: 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .test-case-header:hover {{
            background: #e9ecef;
        }}

        .test-case-header h3 {{
            margin: 0;
            color: #333;
        }}

        .test-case-content {{
            padding: 20px;
            display: none;
        }}

        .test-case-content.expanded {{
            display: block;
        }}

        .step-item {{
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }}

        .screenshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .screenshot-item {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}

        .screenshot-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}

        .screenshot-item .caption {{
            padding: 10px;
            background: #f8f9fa;
            text-align: center;
            font-size: 0.9em;
            color: #666;
        }}

        .summary {{
            margin-top: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}

        .summary h2 {{
            color: #333;
            margin-bottom: 15px;
        }}

        .summary ul {{
            list-style: none;
            padding: 0;
        }}

        .summary li {{
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }}

        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {test_name}</h1>
            <div class="meta">
                <span>📅 测试日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                <span>🌐 测试环境: {self.test_results.get('url', 'N/A')}</span>
                <span>🤖 测试执行者: AI Agent</span>
            </div>
        </div>

        <div class="content">
            <!-- 测试概览 -->
            <div class="overview">
                <h2>📈 测试概览</h2>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">{total_tests}</div>
                        <div class="label">总测试用例</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{executed}</div>
                        <div class="label">已执行</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{passed}</div>
                        <div class="label">通过</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{partial}</div>
                        <div class="label">部分通过</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{failed}</div>
                        <div class="label">失败</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{pass_rate:.1f}%</div>
                        <div class="label">通过率</div>
                    </div>
                </div>

                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>测试用例</th>
                                <th>测试功能</th>
                                <th>执行状态</th>
                                <th>通过/失败</th>
                                <th>备注</th>
                            </tr>
                        </thead>
                        <tbody>
                            {self._generate_test_cases_table_rows(test_cases)}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 详细测试结果 -->
            <div class="overview">
                <h2>📋 详细测试结果</h2>
                {test_cases_html}
            </div>

            <!-- 测试总结 -->
            <div class="summary">
                <h2>📊 测试总结</h2>
                <ul>
                    <li><strong>总测试用例数:</strong> {total_tests}</li>
                    <li><strong>已执行:</strong> {executed}</li>
                    <li><strong>通过:</strong> {passed}</li>
                    <li><strong>部分通过:</strong> {partial}</li>
                    <li><strong>失败:</strong> {failed}</li>
                    <li><strong>跳过:</strong> {skipped}</li>
                    <li><strong>通过率:</strong> {pass_rate:.1f}%</li>
                </ul>
            </div>
        </div>

        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 报告版本: v1.0</p>
        </div>
    </div>

    <script>
        function toggleTestCase(id) {{
            const content = document.getElementById(`content-${{id}}`);
            const toggleBtn = document.getElementById(`toggle-${{id}}`);
            const isExpanded = content.classList.contains('expanded');
            
            if (isExpanded) {{
                content.classList.remove('expanded');
                toggleBtn.querySelector('span:first-child').textContent = '展开';
            }} else {{
                content.classList.add('expanded');
                toggleBtn.querySelector('span:first-child').textContent = '折叠';
            }}
            toggleBtn.classList.toggle('expanded');
        }}
    </script>
</body>
</html>"""
        
        return html_template
    
    def _generate_test_cases_table_rows(self, test_cases: List[Dict]) -> str:
        """生成测试用例表格行"""
        rows = []
        for i, tc in enumerate(test_cases, 1):
            status = tc.get('status', 'unknown')
            status_class = f'status-{status}'
            status_text = {
                'passed': '✅ 通过',
                'failed': '❌ 失败',
                'partial': '⚠️ 部分通过',
                'skipped': '⏭️ 跳过'
            }.get(status, status)
            
            rows.append(f"""
                <tr>
                    <td>测试用例{i}</td>
                    <td>{tc.get('test_name', 'N/A')}</td>
                    <td>✅ 已完成</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{tc.get('note', '')}</td>
                </tr>
            """)
        return ''.join(rows)
    
    def _generate_test_cases_html(self, test_cases: List[Dict]) -> str:
        """生成测试用例详细HTML"""
        html_parts = []
        for i, tc in enumerate(test_cases, 1):
            status = tc.get('status', 'unknown')
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'partial': '⚠️',
                'skipped': '⏭️'
            }.get(status, '❓')
            
            steps_html = self._generate_steps_html(tc.get('steps', []))
            screenshots_html = self._generate_screenshots_html(tc.get('screenshots', []))
            
            html_parts.append(f"""
            <div class="test-case">
                <div class="test-case-header" onclick="toggleTestCase({i})" id="toggle-{i}">
                    <h3>{status_icon} 测试用例{i}: {tc.get('test_name', 'N/A')}</h3>
                    <span>展开</span>
                </div>
                <div class="test-case-content" id="content-{i}">
                    <p><strong>测试目标:</strong> {tc.get('description', 'N/A')}</p>
                    <div style="margin-top: 20px;">
                        <h4>测试步骤:</h4>
                        {steps_html}
                    </div>
                    {screenshots_html}
                    <div style="margin-top: 20px;">
                        <p><strong>测试状态:</strong> <span class="status-{status}">{status}</span></p>
                    </div>
                </div>
            </div>
            """)
        
        return ''.join(html_parts)
    
    def _generate_steps_html(self, steps: List[Dict]) -> str:
        """生成测试步骤HTML"""
        if not steps:
            return "<p>无测试步骤记录</p>"
        
        step_items = []
        for step in steps:
            status_icon = '✅' if step.get('success', True) else '❌'
            step_items.append(f"""
            <div class="step-item">
                {status_icon} {step.get('description', 'N/A')}
            </div>
            """)
        
        return ''.join(step_items)
    
    def _generate_screenshots_html(self, screenshots: List[str]) -> str:
        """生成截图HTML"""
        if not screenshots:
            return ""
        
        screenshot_items = []
        for screenshot in screenshots:
            screenshot_path = Path(screenshot)
            if screenshot_path.is_absolute():
                rel_path = screenshot
            else:
                rel_path = screenshot_path.relative_to(self.output_dir)
            
            screenshot_items.append(f"""
            <div class="screenshot-item">
                <img src="{rel_path}" alt="测试截图" onerror="this.style.display='none'">
                <div class="caption">{screenshot_path.name}</div>
            </div>
            """)
        
        return f"""
        <div style="margin-top: 20px;">
            <h4>测试截图:</h4>
            <div class="screenshot-grid">
                {''.join(screenshot_items)}
            </div>
        </div>
        """
    
    def _generate_markdown_content(self) -> str:
        """生成Markdown内容"""
        test_name = self.test_results.get('test_name', '测试报告')
        description = self.test_results.get('description', '')
        test_cases = self.test_results.get('test_cases', [])
        
        # 统计信息
        total_tests = len(test_cases)
        passed = sum(1 for tc in test_cases if tc.get('status') == 'passed')
        failed = sum(1 for tc in test_cases if tc.get('status') == 'failed')
        partial = sum(1 for tc in test_cases if tc.get('status') == 'partial')
        skipped = sum(1 for tc in test_cases if tc.get('status') == 'skipped')
        executed = total_tests - skipped
        pass_rate = (passed / executed * 100) if executed > 0 else 0
        
        md_content = f"""# {test_name}

**测试日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**测试环境**: {self.test_results.get('url', 'N/A')}  
**测试执行者**: AI Agent  
**测试范围**: {description}

---

## 测试概览

| 测试用例 | 测试功能 | 执行状态 | 通过/失败 | 备注 |
|---------|---------|---------|----------|------|
"""
        
        for i, tc in enumerate(test_cases, 1):
            status = tc.get('status', 'unknown')
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'partial': '⚠️',
                'skipped': '⏭️'
            }.get(status, '❓')
            
            md_content += f"| 测试用例{i} | {tc.get('test_name', 'N/A')} | ✅ 已完成 | {status_icon} {status} | {tc.get('note', '')} |\n"
        
        md_content += f"""
**总体统计**:
- 总测试用例数: {total_tests}
- 已执行: {executed}
- 通过: {passed}
- 部分通过: {partial}
- 失败: {failed}
- 跳过: {skipped}
- 通过率: {pass_rate:.1f}%

---

## 详细测试结果

"""
        
        for i, tc in enumerate(test_cases, 1):
            md_content += f"""### 测试用例{i}: {tc.get('test_name', 'N/A')}

**测试目标**: {tc.get('description', 'N/A')}

**测试步骤**:
"""
            for step in tc.get('steps', []):
                status_icon = '✅' if step.get('success', True) else '❌'
                md_content += f"{status_icon} {step.get('description', 'N/A')}\n"
            
            md_content += f"""
**测试状态**: {tc.get('status', 'unknown')}

---

"""
        
        return md_content


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <test_results.json> [output_dir]")
        print("示例: python generate_report.py test_results.json ./reports")
        sys.exit(1)
    
    test_results_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        generator = TestReportGenerator(test_results_path, output_dir)
        
        # 生成HTML报告
        html_path = generator.generate_html_report()
        
        # 生成Markdown报告
        md_path = generator.generate_markdown_report()
        
        print(f"\n✅ 报告生成完成！")
        print(f"   HTML报告: {html_path}")
        print(f"   Markdown报告: {md_path}")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()


