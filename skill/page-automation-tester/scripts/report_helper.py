#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试报告生成辅助工具
提供简单的函数接口，方便在测试代码中调用
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional


def generate_test_reports(
    test_results: Dict[str, Any],
    output_dir: str = "testcase",
    results_filename: str = None
) -> tuple[str, str]:
    """
    生成测试报告（HTML和Markdown）
    
    Args:
        test_results: 测试结果字典
        output_dir: 输出目录
        results_filename: 测试结果JSON文件名，默认为 test_results.json
        
    Returns:
        (html_path, md_path) 生成的HTML和Markdown报告路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存测试结果JSON
    if results_filename is None:
        test_name = test_results.get('test_name', 'test_report').replace(' ', '_')
        results_filename = f"{test_name}_results.json"
    
    results_path = output_path / results_filename
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试结果已保存: {results_path}")
    
    # 调用报告生成工具
    script_path = Path(__file__).parent / "generate_report.py"
    
    if not script_path.exists():
        raise FileNotFoundError(f"报告生成脚本不存在: {script_path}")
    
    cmd = ['python', str(script_path), str(results_path), str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"报告生成失败: {result.stderr}")
    
    print(result.stdout)
    
    # 返回生成的文件路径
    test_name = test_results.get('test_name', 'test_report').replace(' ', '_')
    html_path = output_path / f"{test_name}_visualization.html"
    md_path = output_path / f"{test_name}_report.md"
    
    return str(html_path), str(md_path)


def create_test_result(
    test_name: str,
    description: str,
    url: str,
    test_cases: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    创建测试结果字典的辅助函数
    
    Args:
        test_name: 测试名称
        description: 测试描述
        url: 测试URL
        test_cases: 测试用例列表
        
    Returns:
        测试结果字典
    """
    return {
        "test_name": test_name,
        "description": description,
        "url": url,
        "test_cases": test_cases
    }


def create_test_case(
    test_name: str,
    description: str,
    status: str = "passed",
    note: str = "",
    steps: List[Dict[str, Any]] = None,
    screenshots: List[str] = None
) -> Dict[str, Any]:
    """
    创建测试用例字典的辅助函数
    
    Args:
        test_name: 测试用例名称
        description: 测试用例描述
        status: 执行状态 (passed/failed/partial/skipped)
        note: 备注信息
        steps: 测试步骤列表
        screenshots: 截图路径列表
        
    Returns:
        测试用例字典
    """
    return {
        "test_name": test_name,
        "description": description,
        "status": status,
        "note": note,
        "steps": steps or [],
        "screenshots": screenshots or []
    }


def create_test_step(
    description: str,
    success: bool = True,
    duration: float = None
) -> Dict[str, Any]:
    """
    创建测试步骤字典的辅助函数
    
    Args:
        description: 步骤描述
        success: 是否成功
        duration: 执行耗时（秒）
        
    Returns:
        测试步骤字典
    """
    step = {
        "description": description,
        "success": success
    }
    if duration is not None:
        step["duration"] = duration
    return step


# 使用示例
if __name__ == '__main__':
    # 示例：创建测试结果并生成报告
    test_results = create_test_result(
        test_name="BKLog字段管理测试",
        description="测试字段列表管理功能",
        url="https://bklog.woa.com",
        test_cases=[
            create_test_case(
                test_name="字段添加和排序测试",
                description="从可选字段列表添加字段到显示字段",
                status="passed",
                note="测试通过",
                steps=[
                    create_test_step("导航到日志平台首页", True, 2.1),
                    create_test_step("选择demo业务", True, 1.5),
                    create_test_step("添加字段到显示列表", True, 1.2),
                    create_test_step("调整字段排序", True, 0.8)
                ],
                screenshots=[
                    "screenshots/test_case_1_step_1.png",
                    "screenshots/test_case_1_step_2.png"
                ]
            )
        ]
    )
    
    # 生成报告
    html_path, md_path = generate_test_reports(test_results, "testcase")
    print(f"\n✅ 报告生成完成！")
    print(f"   HTML报告: {html_path}")
    print(f"   Markdown报告: {md_path}")


