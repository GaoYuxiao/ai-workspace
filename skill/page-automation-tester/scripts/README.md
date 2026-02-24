# 测试报告生成工具

## 文件说明

- `generate_report.py` - 报告生成主脚本，将测试结果JSON转换为HTML和Markdown报告
- `report_helper.py` - 报告生成辅助工具，提供简单的Python函数接口

## 快速使用

### 命令行使用

```bash
# 基本用法
python generate_report.py test_results.json

# 指定输出目录
python generate_report.py test_results.json ./reports
```

### Python代码中使用

```python
from report_helper import (
    generate_test_reports,
    create_test_result,
    create_test_case,
    create_test_step
)

# 创建测试结果
test_results = create_test_result(
    test_name="测试名称",
    description="测试描述",
    url="https://example.com",
    test_cases=[
        create_test_case(
            test_name="测试用例1",
            description="测试用例描述",
            status="passed",
            steps=[
                create_test_step("步骤1", True, 1.2),
                create_test_step("步骤2", True, 0.8)
            ],
            screenshots=["screenshots/step1.png"]
        )
    ]
)

# 生成报告
html_path, md_path = generate_test_reports(test_results, "testcase")
```

## 输入格式

测试结果JSON格式：

```json
{
  "test_name": "测试名称",
  "description": "测试描述",
  "url": "测试URL",
  "test_cases": [
    {
      "test_name": "测试用例名称",
      "description": "测试用例描述",
      "status": "passed",
      "note": "备注",
      "steps": [
        {
          "description": "步骤描述",
          "success": true,
          "duration": 1.2
        }
      ],
      "screenshots": ["screenshots/test.png"]
    }
  ]
}
```

## 输出文件

- `{test_name}_visualization.html` - 可视化HTML报告
- `{test_name}_report.md` - Markdown报告

## 状态值

- `passed` - 测试通过
- `failed` - 测试失败
- `partial` - 部分通过
- `skipped` - 跳过


