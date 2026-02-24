# 自动化测试用例目录

本目录包含 BKLog 日志平台的自动化测试相关文件。

## 目录结构

```
testcase/
├── README.md                              # 本说明文件
├── test_case_bklog_context_highlight.json # BKLog上下文功能测试用例
├── test_report_bklog_automation.md        # 自动化测试报告
└── bklog_selector_mapping.md              # BKLog页面元素Selector映射表
```

## 文件说明

### 1. test_case_bklog_context_highlight.json

BKLog 日志平台的上下文功能与高亮测试用例。

**测试内容**：
- 业务选择（demo业务）
- 索引集选择（容器日志）
- WARN级别日志检索
- 上下文面板查看
- 高亮功能验证

**使用方法**：
```bash
# 通过 page-automation-tester skill 执行
# Agent 会读取此 JSON 文件并执行自动化测试
```

### 2. test_report_bklog_automation.md

自动化测试执行报告，包含：
- 测试执行概览
- 测试步骤详情
- 验证结果
- 失败原因分析（如有）

### 3. bklog_selector_mapping.md

BKLog 前端页面的元素定位映射表，用于页面自动化测试。

**包含内容**：
- 页面主要元素的定位方式
- 多种定位策略（文本、角色、选择器）
- 测试用例示例
- 特殊场景处理说明

**定位优先级**：
1. 快照定位（推荐）
2. 文本定位
3. 角色定位
4. 选择器定位（备选）

## 相关资源

- **Skill 文档**：`../skill/page-automation-tester/SKILL.md`
- **测试用例格式**：`../skill/page-automation-tester/references/test_case_format.md`
- **优化指南**：`../skill/page-automation-tester/references/optimization_guide.md`
- **页面辅助脚本**：`../skill/page-automation-tester/scripts/page_helper.js`

## 使用示例

### 执行测试用例

```json
{
  "test_name": "BKLog上下文功能测试",
  "description": "测试日志检索和上下文功能",
  "url": "https://bklog.woa.com",
  "steps": [
    {
      "action": "navigate",
      "url": "https://bklog.woa.com"
    },
    // ... 更多步骤
  ]
}
```

### 使用 Selector 映射表

在测试用例中，可以直接使用映射表中的元素描述：

```json
{
  "action": "click",
  "target": "业务选择器",  // 映射表中的描述名称
  "description": "点击业务选择器"
}
```

Agent 会根据映射表自动选择合适的定位策略。

## 注意事项

1. **测试环境**：确保 Chrome DevTools MCP 服务器已正确配置并运行
2. **测试数据**：使用独立的测试账号和数据，避免影响生产环境
3. **元素定位**：优先使用快照定位，避免使用过于具体的选择器
4. **等待策略**：关键操作后使用 `wait_for` 等待页面状态稳定

## 更新日志

- **2025-01-XX**：初始版本，整理自动化测试相关文件到 testcase 目录


