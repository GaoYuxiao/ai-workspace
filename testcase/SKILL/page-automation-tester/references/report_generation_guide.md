# 测试报告生成指南

## 概述

本指南说明如何在测试执行完成后生成可视化的HTML报告和Markdown报告。

## 快速开始

### 1. 准备测试结果JSON

测试执行完成后，将结果保存为JSON格式：

```json
{
  "test_name": "BKLog字段管理测试",
  "description": "测试字段列表管理功能",
  "url": "https://bklog.woa.com",
  "test_cases": [
    {
      "test_name": "字段添加和排序测试",
      "description": "从可选字段列表添加字段到显示字段",
      "status": "passed",
      "note": "测试通过",
      "steps": [
        {
          "description": "导航到日志平台首页",
          "success": true,
          "duration": 2.1
        },
        {
          "description": "选择demo业务",
          "success": true,
          "duration": 1.5
        }
      ],
      "screenshots": [
        "screenshots/test_case_1_step_1.png",
        "screenshots/test_case_1_step_2.png"
      ]
    }
  ]
}
```

### 2. 调用报告生成工具

```bash
# 基本用法
python skill/page-automation-tester/scripts/generate_report.py test_results.json

# 指定输出目录
python skill/page-automation-tester/scripts/generate_report.py test_results.json testcase
```

### 3. 查看生成的报告

- HTML报告：`{test_name}_visualization.html` - 在浏览器中打开
- Markdown报告：`{test_name}_report.md` - 使用Markdown阅读器查看

## 在Agent中集成

### Python代码示例

```python
import json
import subprocess
from pathlib import Path
from datetime import datetime

def save_test_results(test_results: dict, output_path: str):
    """保存测试结果到JSON文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    print(f"✅ 测试结果已保存: {output_path}")

def generate_reports(test_results_path: str, output_dir: str = None):
    """生成测试报告"""
    script_path = Path("skill/page-automation-tester/scripts/generate_report.py")
    
    if not script_path.exists():
        print(f"❌ 报告生成脚本不存在: {script_path}")
        return False
    
    cmd = ['python', str(script_path), test_results_path]
    if output_dir:
        cmd.append(output_dir)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 报告生成成功")
        print(result.stdout)
        return True
    else:
        print(f"❌ 报告生成失败: {result.stderr}")
        return False

# 使用示例
test_results = {
    "test_name": "BKLog字段管理测试",
    "description": "测试字段列表管理功能",
    "url": "https://bklog.woa.com",
    "test_cases": [
        # ... 测试用例数据
    ]
}

# 1. 保存测试结果
results_path = "testcase/test_results.json"
save_test_results(test_results, results_path)

# 2. 生成报告
generate_reports(results_path, "testcase")
```

## JSON格式规范

### 必需字段

- `test_name`: 测试名称
- `test_cases`: 测试用例数组

### 测试用例字段

- `test_name`: 测试用例名称（必需）
- `description`: 测试用例描述（可选）
- `status`: 执行状态（必需）- `passed`/`failed`/`partial`/`skipped`
- `note`: 备注信息（可选）
- `steps`: 测试步骤数组（可选）
- `screenshots`: 截图路径数组（可选）

### 步骤字段

- `description`: 步骤描述（必需）
- `success`: 是否成功（可选，默认true）
- `duration`: 执行耗时（可选，单位：秒）

## 报告特性

### HTML报告

- 📊 美观的统计卡片展示
- 📋 详细的测试用例表格
- 📸 响应式截图网格
- 🎨 现代化UI设计
- ✅ 清晰的状态标识
- 🔄 可展开/折叠的测试用例详情

### Markdown报告

- 简洁的表格格式
- 完整的测试信息
- 截图路径引用
- 便于版本控制

## 常见问题

### Q: 截图路径如何处理？

A: 截图路径可以是相对路径或绝对路径。如果是相对路径，会相对于输出目录解析。

### Q: 如何自定义报告样式？

A: 修改 `scripts/generate_report.py` 中的HTML模板和CSS样式。

### Q: 报告生成失败怎么办？

A: 检查：
1. JSON格式是否正确
2. Python环境是否可用
3. 输出目录是否有写入权限
4. 查看错误信息进行排查

## 最佳实践

1. **统一命名**：使用有意义的测试名称和文件命名
2. **及时生成**：测试完成后立即生成报告
3. **保存截图**：关键步骤和失败场景都要截图
4. **详细记录**：记录每个步骤的执行结果和耗时
5. **版本控制**：将Markdown报告纳入版本控制

