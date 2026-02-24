---
name: page-automation-tester
description: 使用 Chrome DevTools MCP 工具进行页面自动化测试验证。用于根据用户提供的测试用例，通过浏览器自动化访问页面、执行操作（点击、输入、等待等）、验证预期结果（元素存在、文本内容、页面状态等），并生成详细的测试报告。适用于：(1) 功能回归测试 (2) UI 交互验证 (3) 页面行为测试 (4) 自动化测试用例执行 (5) 页面功能验收测试
---

# Page Automation Tester

## 概览

本 Skill 让 Agent 能够通过 **Chrome DevTools MCP 工具** 完成页面自动化测试，包括访问页面、执行操作、验证结果并生成测试报告。适用于功能测试、UI 验证、回归测试等场景。

典型触发语句示例：

- "帮我测试登录功能，输入用户名密码后验证是否跳转到首页"
- "验证这个页面的搜索功能是否正常工作"
- "执行这个测试用例列表，并生成测试报告"
- "测试表单提交功能，验证提交后的提示信息"

---

## 一、所需 MCP 工具与基本能力

本 Skill 使用以下 Chrome DevTools MCP 工具：

### 页面导航与基础操作
- `mcp_chrome-devtools_navigate_page` - 导航到指定 URL
- `mcp_chrome-devtools_new_page` - 创建新页面
- `mcp_chrome-devtools_select_page` - 选择当前操作的页面
- `mcp_chrome-devtools_list_pages` - 列出所有打开的页面
- `mcp_chrome-devtools_close_page` - 关闭页面

### 页面内容获取
- `mcp_chrome-devtools_take_snapshot` - 获取页面可访问性快照（推荐用于元素定位）
- `mcp_chrome-devtools_take_screenshot` - 截图（用于验证和报告）

### 元素交互操作
- `mcp_chrome-devtools_click` - 点击元素
- `mcp_chrome-devtools_fill` - 填写输入框
- `mcp_chrome-devtools_fill_form` - 批量填写表单
- `mcp_chrome-devtools_press_key` - 按键操作
- `mcp_chrome-devtools_hover` - 悬停元素
- `mcp_chrome-devtools_drag` - 拖拽操作

### 等待与验证
- `mcp_chrome-devtools_wait_for` - 等待指定文本出现
- `mcp_chrome-devtools_evaluate_script` - 执行 JavaScript 验证

### 调试与监控
- `mcp_chrome-devtools_list_console_messages` - 查看控制台消息
- `mcp_chrome-devtools_list_network_requests` - 查看网络请求

---

## 二、测试用例格式

测试用例应包含以下信息：

### 基本结构

```json
{
  "test_name": "测试用例名称",
  "description": "测试用例描述",
  "url": "要测试的页面URL",
  "steps": [
    {
      "action": "操作类型（navigate/click/fill/wait/verify等）",
      "target": "目标元素（通过snapshot获取的uid或选择器）",
      "value": "操作值（如输入内容）",
      "description": "步骤描述"
    }
  ],
  "expected_results": [
    {
      "type": "验证类型（element_exists/text_equals/url_contains等）",
      "target": "验证目标",
      "expected_value": "期望值",
      "description": "验证描述"
    }
  ]
}
```

### 操作类型说明

| 操作类型 | 说明 | 必需参数 |
|---------|------|---------|
| `navigate` | 导航到URL | `url` |
| `snapshot` | 获取页面快照 | 无 |
| `click` | 点击元素 | `target` (uid) |
| `fill` | 填写输入框 | `target` (uid), `value` |
| `fill_form` | 批量填写表单 | `elements` (数组) |
| `press_key` | 按键 | `key` |
| `wait_for` | 等待文本出现 | `text` |
| `hover` | 悬停 | `target` (uid) |
| `screenshot` | 截图 | `filePath` (可选) |

### 验证类型说明

| 验证类型 | 说明 | 必需参数 |
|---------|------|---------|
| `element_exists` | 元素存在 | `target` (uid或文本) |
| `text_equals` | 文本完全匹配 | `target`, `expected_value` |
| `text_contains` | 文本包含 | `target`, `expected_value` |
| `url_equals` | URL完全匹配 | `expected_value` |
| `url_contains` | URL包含 | `expected_value` |
| `console_no_errors` | 控制台无错误 | 无 |
| `custom_script` | 自定义JS验证 | `script` |

详细格式参考见 `references/test_case_format.md`。

---

## 三、测试执行流程

### 1. 准备阶段

1. **解析测试用例**
   - 读取用户提供的测试用例（JSON格式或自然语言描述）
   - 确认测试目标URL和测试步骤
   - 验证测试用例格式完整性

2. **初始化浏览器环境**
   - 使用 `mcp_chrome-devtools_new_page` 创建新页面（如需要）
   - 使用 `mcp_chrome-devtools_select_page` 选择目标页面
   - 设置页面尺寸（如需要）：`mcp_chrome-devtools_resize_page`

### 2. 执行阶段

对于每个测试步骤：

1. **获取页面状态**
   - 使用 `mcp_chrome-devtools_take_snapshot` 获取当前页面快照
   - 快照包含所有可交互元素的 `uid`，用于后续操作

2. **定位目标元素**
   - 从快照中查找目标元素（通过文本、角色、名称等）
   - 记录元素的 `uid` 用于操作

3. **执行操作**
   - 根据操作类型调用对应的 MCP 工具
   - 操作后适当等待（使用 `wait_for` 或 `evaluate_script` 检查）

4. **验证结果**
   - 执行验证步骤，检查预期结果
   - 记录验证结果（通过/失败）

### 3. 验证方法

#### 元素存在验证
```python
# 1. 获取快照
snapshot = take_snapshot()
# 2. 在快照中查找目标元素
element = find_element_by_text(snapshot, "登录成功")
# 3. 判断是否存在
assert element is not None
```

#### 文本内容验证
```python
# 方法1: 通过快照查找元素并检查文本
snapshot = take_snapshot()
element = find_element_by_uid(snapshot, uid)
assert expected_text in element.get("text", "")

# 方法2: 使用 evaluate_script
result = evaluate_script("() => document.querySelector('.message').textContent")
assert expected_text in result
```

#### URL验证
```python
# 使用 evaluate_script 获取当前URL
current_url = evaluate_script("() => window.location.href")
assert expected_url in current_url
```

#### 控制台错误验证
```python
console_messages = list_console_messages(types=["error"])
assert len(console_messages) == 0, f"发现控制台错误: {console_messages}"
```

### 4. 结果记录

对每个测试用例记录：

- **测试用例名称**
- **执行状态**：通过/失败/跳过
- **执行步骤详情**：每个步骤的执行结果
- **验证结果**：每个验证点的通过/失败状态
- **失败原因**：如果失败，记录具体原因
- **截图**：关键步骤的截图（失败时必截图）
- **执行时间**：开始和结束时间

---

## 四、测试报告生成

### 报告结构

测试报告应包含以下部分：

1. **测试概览**
   - 总测试用例数
   - 通过数、失败数、跳过数
   - 总执行时间
   - 通过率

2. **测试用例详情**
   - 每个测试用例的执行结果
   - 步骤执行日志
   - 验证结果详情
   - 失败时的错误信息和截图

3. **总结与建议**
   - 主要问题汇总
   - 修复建议

### 报告格式

支持以下格式：
- **Markdown**：便于阅读和版本控制
- **JSON**：便于程序化处理
- **HTML**：包含截图的可视化报告

报告模板见 `assets/test_report_template.md`。

### 报告生成工具

**重要**：测试执行完成后，必须调用报告生成工具生成可视化报告。

#### 使用报告生成脚本

测试执行完成后，使用 `scripts/generate_report.py` 生成HTML和Markdown报告：

```bash
# 基本用法
python scripts/generate_report.py <test_results.json>

# 指定输出目录
python scripts/generate_report.py <test_results.json> ./reports
```

#### 在Agent中调用

测试执行完成后，Agent应该：

1. **保存测试结果JSON**：
   - 将测试执行结果保存为JSON格式
   - 包含测试用例、步骤、验证结果、截图路径等信息

2. **调用报告生成工具**：
   ```python
   # 在测试完成后执行
   import subprocess
   subprocess.run([
       'python',
       'skill/page-automation-tester/scripts/generate_report.py',
       'test_results.json',
       'testcase'  # 输出目录
   ])
   ```

3. **生成的文件**：
   - `{test_name}_visualization.html` - 可视化HTML报告
   - `{test_name}_report.md` - Markdown报告

#### 测试结果JSON格式

报告生成工具期望的JSON格式：

```json
{
  "test_name": "测试名称",
  "description": "测试描述",
  "url": "测试URL",
  "test_cases": [
    {
      "test_name": "测试用例名称",
      "description": "测试用例描述",
      "status": "passed|failed|partial|skipped",
      "note": "备注信息",
      "steps": [
        {
          "description": "步骤描述",
          "success": true,
          "duration": 1.2
        }
      ],
      "screenshots": [
        "screenshots/test_case_1_step_1.png"
      ]
    }
  ]
}
```

#### 报告内容

生成的HTML报告包含：
- 📊 **测试概览**：统计卡片和表格
- 📋 **详细结果**：每个测试用例的完整信息
- 📸 **截图展示**：响应式截图网格
- 🎨 **美观设计**：现代化UI，渐变色彩

生成的Markdown报告包含：
- 测试概览表格
- 详细测试结果
- 步骤执行记录
- 截图路径引用

---

## 五、测试报告生成（重要⭐）

### 必须生成报告

**每次测试执行完成后，Agent必须调用报告生成工具生成可视化报告。**

### 报告生成流程

#### 1. 测试执行阶段

在执行测试时，需要记录：
- 每个测试用例的执行状态（passed/failed/partial/skipped）
- 每个步骤的执行结果和耗时
- 验证结果（通过/失败）
- 截图路径（如果有）
- 错误信息（如果失败）

#### 2. 结果整理阶段

测试完成后，将结果整理为JSON格式并保存：

```python
test_results = {
    "test_name": "测试名称",
    "description": "测试描述",
    "url": "测试URL",
    "test_cases": [
        {
            "test_name": "测试用例名称",
            "description": "测试用例描述",
            "status": "passed",  # passed/failed/partial/skipped
            "note": "备注信息",
            "steps": [
                {
                    "description": "步骤描述",
                    "success": True,
                    "duration": 1.2
                }
            ],
            "screenshots": [
                "screenshots/test_case_1_step_1.png"
            ]
        }
    ]
}

# 保存为JSON文件
import json
with open('test_results.json', 'w', encoding='utf-8') as f:
    json.dump(test_results, f, ensure_ascii=False, indent=2)
```

#### 3. 调用报告生成工具

**方式1：使用辅助函数（推荐）**

```python
from skill.page_automation_tester.scripts.report_helper import (
    generate_test_reports,
    create_test_result,
    create_test_case,
    create_test_step
)

# 创建测试结果
test_results = create_test_result(
    test_name="BKLog字段管理测试",
    description="测试字段列表管理功能",
    url="https://bklog.woa.com",
    test_cases=[
        create_test_case(
            test_name="字段添加和排序测试",
            description="从可选字段列表添加字段到显示字段",
            status="passed",
            steps=[
                create_test_step("导航到日志平台", True, 2.1),
                create_test_step("添加字段", True, 1.5)
            ],
            screenshots=["screenshots/test_case_1.png"]
        )
    ]
)

# 生成报告（自动保存JSON并生成HTML和Markdown）
html_path, md_path = generate_test_reports(test_results, "testcase")
print(f"HTML报告: {html_path}")
print(f"Markdown报告: {md_path}")
```

**方式2：直接调用脚本**

```bash
# 基本用法
python skill/page-automation-tester/scripts/generate_report.py test_results.json

# 指定输出目录
python skill/page-automation-tester/scripts/generate_report.py test_results.json testcase
```

**方式3：在Python代码中调用脚本**

```python
import subprocess
from pathlib import Path

script_path = Path("skill/page-automation-tester/scripts/generate_report.py")
results_path = Path("testcase/test_results.json")
output_dir = "testcase"

result = subprocess.run([
    'python',
    str(script_path),
    str(results_path),
    output_dir
], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ 报告生成成功")
    print(result.stdout)
else:
    print(f"❌ 报告生成失败: {result.stderr}")
```

#### 4. 生成的文件

报告生成工具会在输出目录生成两个文件：

- **`{test_name}_visualization.html`** - 可视化HTML报告
  - 美观的UI设计，渐变色彩
  - 统计卡片和表格展示
  - 可展开/折叠的测试用例详情
  - 响应式截图展示
  - 推荐在浏览器中打开查看

- **`{test_name}_report.md`** - Markdown报告
  - 便于版本控制和阅读
  - 包含完整的测试信息
  - 截图路径引用

#### 5. 查看报告

HTML报告可以直接在浏览器中打开：

```bash
# macOS
open testcase/{test_name}_visualization.html

# Linux
xdg-open testcase/{test_name}_visualization.html

# Windows
start testcase/{test_name}_visualization.html
```

### 报告内容说明

#### HTML报告包含：

1. **测试概览**
   - 统计卡片：总测试用例数、已执行、通过、部分通过、失败、通过率
   - 测试用例表格：所有测试用例的执行状态和结果

2. **详细测试结果**
   - 每个测试用例的完整信息
   - 测试步骤列表（带状态标识）
   - 测试截图（响应式网格布局）
   - 测试状态和备注

3. **测试总结**
   - 总体统计信息
   - 总体评价

#### Markdown报告包含：

- 测试概览表格
- 详细测试结果
- 步骤执行记录
- 截图路径引用

### 注意事项

1. **必须调用**：每次测试执行完成后，必须调用报告生成工具
2. **JSON格式**：确保测试结果JSON格式正确，包含所有必要字段
3. **截图路径**：截图路径可以是相对路径或绝对路径，工具会自动处理
4. **输出目录**：确保输出目录有写入权限

---

## 六、最佳实践

### 1. 元素定位策略

**优先使用快照定位**：
- `take_snapshot` 返回的可访问性树包含所有可交互元素
- 通过文本、角色、名称等属性查找元素
- 使用元素的 `uid` 进行后续操作

**避免使用选择器**：
- 除非必要，避免使用 CSS 选择器或 XPath
- 快照方式更稳定，不受页面结构变化影响

### 2. 等待策略

**显式等待**：
- 操作后使用 `wait_for` 等待关键元素出现
- 使用 `evaluate_script` 检查页面状态

**避免固定延迟**：
- 不要使用固定的 sleep 时间
- 根据实际页面响应动态等待

### 3. 错误处理

**捕获异常**：
- 每个操作都应捕获可能的异常
- 记录详细的错误信息

**失败截图**：
- 测试失败时自动截图
- 截图包含时间戳和测试用例名称

### 4. 测试数据管理

**测试数据隔离**：
- 使用独立的测试账号和数据
- 测试后清理测试数据（如需要）

**数据驱动**：
- 支持从文件读取测试数据
- 支持参数化测试用例

---

## 七、性能优化（重要⭐）

### 问题分析

当前执行流程中，每一步都需要：
1. 调用 `take_snapshot` 获取页面状态（耗时 1-2秒）
2. Agent 分析快照内容（耗时 1-2秒）
3. 查找目标元素（耗时 0.5-1秒）
4. 执行操作（相对较快）

**主要瓶颈**：每次操作都需要完整的 snapshot → 分析 → 查找流程，导致单步耗时 3-5秒。

### 优化方案：页面辅助脚本（推荐⭐⭐⭐⭐⭐）

**核心思路**：在页面中注入 JavaScript 辅助脚本，提供快速元素定位和批量操作能力，减少 snapshot 调用和 MCP 往返次数。

#### 1. 注入辅助脚本

在测试开始时注入 `scripts/page_helper.js`：

```javascript
{
  "action": "evaluate_script",
  "function": "() => { /* 注入 page_helper.js 的内容 */ }",
  "description": "注入页面辅助脚本"
}
```

注入后，页面会提供 `window.__testHelper` API。

#### 2. 快速元素查找（替代 snapshot）

**原始方式（慢）**：
```javascript
// 需要 snapshot + Agent 分析
snapshot(); // 耗时 1-2秒
// Agent 分析快照，查找元素 // 耗时 1-2秒
```

**优化方式（快）**：
```javascript
// 直接使用页面内脚本查找
evaluate_script(() => window.__testHelper.quickFind("登录按钮"));
// 耗时 0.1-0.3秒，提升 10倍
```

#### 3. 批量操作（减少 MCP 调用）

**原始方式（3次调用）**：
```javascript
fill("username", "testuser");    // MCP 调用 1
fill("password", "testpass");    // MCP 调用 2
click("loginButton");            // MCP 调用 3
```

**优化方式（1次调用）**：
```javascript
evaluate_script(() => window.__testHelper.batch.execute([
  {action: 'fill', target: 'username', value: 'testuser'},
  {action: 'fill', target: 'password', value: 'testpass'},
  {action: 'click', target: 'loginButton'}
]));
// 1次 MCP 调用完成所有操作
```

#### 4. 批量验证

```javascript
evaluate_script(() => window.__testHelper.validate.validate([
  {type: 'url_contains', expectedValue: '/dashboard'},
  {type: 'element_exists', target: '欢迎消息'},
  {type: 'text_contains', target: '欢迎消息', expectedValue: 'testuser'}
]));
```

#### 5. 元素缓存

```javascript
// 查找并缓存
const button = evaluate_script(() => window.__testHelper.find.findByText("登录按钮")[0]);
evaluate_script(() => window.__testHelper.cache.cacheElement("loginButton", button.element));

// 后续直接使用缓存
evaluate_script(() => {
  const cached = window.__testHelper.cache.getCached("loginButton");
  if (cached) cached.element.click();
});
```

### 性能对比

| 方式 | 单步耗时 | 10步测试耗时 | 优化效果 |
|------|---------|-------------|---------|
| 原始方式（每次snapshot） | ~3-5秒 | ~30-50秒 | 基准 |
| **优化方式（辅助脚本）** | **~0.5-1秒** | **~5-10秒** | **5-10倍提升** |

### 优化后的测试用例示例

```json
{
  "test_name": "优化登录测试",
  "url": "https://example.com/login",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/login"
    },
    {
      "action": "evaluate_script",
      "function": "() => { /* 注入 page_helper.js */ }",
      "description": "注入辅助脚本"
    },
    {
      "action": "evaluate_script",
      "function": "() => window.__testHelper.batch.execute([{action: 'fill', target: '用户名输入框', value: 'testuser'}, {action: 'fill', target: '密码输入框', value: 'testpass'}, {action: 'click', target: '登录按钮'}])",
      "description": "批量执行：填写表单并登录"
    },
    {
      "action": "wait_for",
      "text": "欢迎",
      "timeout": 5000
    },
    {
      "action": "evaluate_script",
      "function": "() => window.__testHelper.validate.validate([{type: 'url_contains', expectedValue: '/dashboard'}, {type: 'element_exists', target: '用户菜单'}])",
      "description": "批量验证结果"
    }
  ]
}
```

### 最佳实践

1. ✅ **测试开始时立即注入辅助脚本**
2. ✅ **使用 `quickFind` 替代频繁的 `snapshot`**
3. ✅ **批量操作减少 MCP 调用次数**
4. ✅ **批量验证提高效率**
5. ✅ **使用元素缓存避免重复查找**

详细优化指南见 `references/optimization_guide.md`。

---

## 八、常见测试场景示例

### 场景1: 登录功能测试

```json
{
  "test_name": "用户登录测试",
  "url": "https://example.com/login",
  "steps": [
    {"action": "navigate", "url": "https://example.com/login"},
    {"action": "snapshot"},
    {"action": "fill", "target": "username_input_uid", "value": "testuser"},
    {"action": "fill", "target": "password_input_uid", "value": "testpass"},
    {"action": "click", "target": "login_button_uid"},
    {"action": "wait_for", "text": "欢迎"},
    {"action": "snapshot"}
  ],
  "expected_results": [
    {"type": "url_contains", "expected_value": "/dashboard"},
    {"type": "element_exists", "target": "用户菜单"}
  ]
}
```

### 场景2: 表单提交测试

```json
{
  "test_name": "联系表单提交",
  "url": "https://example.com/contact",
  "steps": [
    {"action": "navigate", "url": "https://example.com/contact"},
    {"action": "fill_form", "elements": [
      {"uid": "name_uid", "value": "张三"},
      {"uid": "email_uid", "value": "zhangsan@example.com"},
      {"uid": "message_uid", "value": "测试消息"}
    ]},
    {"action": "click", "target": "submit_button_uid"},
    {"action": "wait_for", "text": "提交成功"}
  ],
  "expected_results": [
    {"type": "text_contains", "target": "success_message", "expected_value": "提交成功"}
  ]
}
```

### 场景3: 搜索功能测试

```json
{
  "test_name": "搜索功能验证",
  "url": "https://example.com",
  "steps": [
    {"action": "navigate", "url": "https://example.com"},
    {"action": "snapshot"},
    {"action": "fill", "target": "search_input_uid", "value": "测试关键词"},
    {"action": "press_key", "key": "Enter"},
    {"action": "wait_for", "text": "搜索结果"}
  ],
  "expected_results": [
    {"type": "url_contains", "expected_value": "search"},
    {"type": "element_exists", "target": "搜索结果列表"}
  ]
}
```

---

## 九、BKLog 页面元素映射表

当执行 BKLog 日志平台的页面自动化测试时，需要参考详细的页面元素映射表来定位元素。**映射表的详细内容存储在独立文件中，Agent 应在执行 BKLog 测试前读取该文件**。

### 使用说明

#### 定位优先级

1. **快照定位（推荐）**：使用 `take_snapshot` 获取页面快照，通过文本、角色等属性查找元素的 `uid`
2. **文本定位**：通过元素的可见文本内容定位
3. **角色定位**：通过 ARIA role 属性定位
4. **选择器定位**：作为最后备选，使用 CSS 选择器或 XPath

#### 在测试用例中的使用

测试用例中使用映射表中的元素描述名称作为 `target`：

```json
{
  "action": "click",
  "target": "业务选择器",  // 使用映射表中的描述名称
  "description": "点击业务选择器"
}
```

实际执行时，Agent 会：
1. 获取页面快照
2. 在快照中查找包含 "业务选择器" 文本的元素
3. 使用找到的元素的 `uid` 执行操作

### 映射表文件位置

**重要**：执行 BKLog 测试前，Agent 应读取以下文件获取完整的元素映射表：

- **映射表文件**：`testcase/bklog_selector_mapping.md`

该文件包含：
- 页面导航与业务选择（业务选择器、索引集选择等）
- 检索功能区域（UI模式、语句模式、时间范围选择等）
- 检索结果区域（结果列表、日志操作按钮等）
- 上下文功能区域（上下文面板、控制功能、过滤功能等）
- 字段过滤与统计
- 通用元素（加载状态、错误提示、确认对话框等）
- 定位策略示例和特殊场景处理

### 快速示例

```json
{
  "action": "snapshot",
  "description": "获取页面快照"
}
{
  "action": "click",
  "target": "业务选择器",  // 映射表中的元素描述
  "description": "点击业务选择器"
}
```

**注意**：详细的元素映射表、定位策略、测试用例示例等完整内容请参考 `testcase/bklog_selector_mapping.md` 文件。

---

## Resources

### references/
- `test_case_format.md` - 详细的测试用例格式说明和示例

### assets/
- `test_report_template.md` - 测试报告模板（Markdown格式）

### scripts/
- `page_helper.js` - 页面辅助脚本，提供快速元素定位和批量操作能力（**性能优化关键**）

**使用方式**：
1. 在测试开始时通过 `evaluate_script` 注入此脚本
2. 使用 `window.__testHelper` API 进行快速操作
3. 详细说明见 `references/optimization_guide.md`

### 外部参考文件
- `../../testcase/bklog_selector_mapping.md` - **BKLog 页面元素映射表**（执行 BKLog 测试前必须读取）
  - 包含完整的页面元素定位信息
  - 提供定位策略和测试用例示例
  - 适用于 BKLog 日志平台的自动化测试

---

**注意**：执行测试前确保 Chrome DevTools MCP 服务器已正确配置并运行。
