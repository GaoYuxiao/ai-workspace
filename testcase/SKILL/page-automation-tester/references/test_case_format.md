# 测试用例格式详细说明

本文档详细说明测试用例的格式规范和使用方法。

## 目录

- [基本结构](#基本结构)
- [操作类型详解](#操作类型详解)
- [验证类型详解](#验证类型详解)
- [完整示例](#完整示例)
- [自然语言转测试用例](#自然语言转测试用例)

---

## 基本结构

### 最小测试用例

```json
{
  "test_name": "测试用例名称",
  "description": "测试用例描述（可选）",
  "url": "https://example.com",
  "steps": [],
  "expected_results": []
}
```

### 完整测试用例

```json
{
  "test_name": "测试用例名称",
  "description": "详细的测试用例描述",
  "url": "https://example.com/page",
  "timeout": 30000,
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/page",
      "description": "导航到目标页面"
    },
    {
      "action": "snapshot",
      "description": "获取页面快照"
    },
    {
      "action": "click",
      "target": "button_uid_123",
      "description": "点击登录按钮",
      "wait_after": true
    }
  ],
  "expected_results": [
    {
      "type": "element_exists",
      "target": "success_message",
      "description": "验证成功消息出现"
    }
  ]
}
```

---

## 操作类型详解

### navigate - 页面导航

导航到指定URL。

```json
{
  "action": "navigate",
  "url": "https://example.com/login",
  "type": "url",
  "timeout": 30000,
  "description": "导航到登录页面"
}
```

**参数说明**：
- `url` (必需): 目标URL
- `type` (可选): 导航类型，默认为 "url"，可选 "back", "forward", "reload"
- `timeout` (可选): 超时时间（毫秒），默认使用全局timeout
- `ignoreCache` (可选): 是否忽略缓存，默认 false

### snapshot - 获取页面快照

获取页面的可访问性快照，用于元素定位。

```json
{
  "action": "snapshot",
  "verbose": false,
  "description": "获取页面快照以定位元素"
}
```

**参数说明**：
- `verbose` (可选): 是否包含详细信息，默认 false

**返回值**：快照对象，包含所有可交互元素的uid和属性。

### click - 点击元素

点击指定元素。

```json
{
  "action": "click",
  "target": "button_uid_123",
  "dblClick": false,
  "wait_after": true,
  "description": "点击提交按钮"
}
```

**参数说明**：
- `target` (必需): 元素的uid（从snapshot获取）
- `dblClick` (可选): 是否双击，默认 false
- `wait_after` (可选): 操作后是否等待，默认 true

### fill - 填写输入框

向输入框填写内容。

```json
{
  "action": "fill",
  "target": "input_uid_456",
  "value": "test@example.com",
  "description": "填写邮箱地址"
}
```

**参数说明**：
- `target` (必需): 输入框的uid
- `value` (必需): 要填写的内容

### fill_form - 批量填写表单

一次性填写多个表单字段。

```json
{
  "action": "fill_form",
  "elements": [
    {"uid": "name_input_uid", "value": "张三"},
    {"uid": "email_input_uid", "value": "zhangsan@example.com"},
    {"uid": "phone_input_uid", "value": "13800138000"}
  ],
  "description": "填写联系表单"
}
```

**参数说明**：
- `elements` (必需): 元素数组，每个元素包含uid和value

### press_key - 按键操作

模拟键盘按键。

```json
{
  "action": "press_key",
  "key": "Enter",
  "description": "按回车键提交"
}
```

**常用按键值**：
- `Enter`, `Escape`, `Tab`, `Backspace`
- `Control+A`, `Control+C`, `Control+V`
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`

### wait_for - 等待文本出现

等待指定文本出现在页面上。

```json
{
  "action": "wait_for",
  "text": "加载完成",
  "timeout": 10000,
  "description": "等待页面加载完成"
}
```

**参数说明**：
- `text` (必需): 要等待的文本
- `timeout` (可选): 超时时间（毫秒），默认使用全局timeout

### hover - 悬停元素

鼠标悬停在元素上。

```json
{
  "action": "hover",
  "target": "menu_item_uid",
  "description": "悬停在菜单项上"
}
```

### screenshot - 截图

对页面或元素进行截图。

```json
{
  "action": "screenshot",
  "filePath": "screenshots/step_1.png",
  "fullPage": false,
  "uid": "element_uid",
  "description": "截图保存验证结果"
}
```

**参数说明**：
- `filePath` (可选): 保存路径，不指定则不保存
- `fullPage` (可选): 是否全页截图，默认 false
- `uid` (可选): 元素uid，指定则只截取该元素

### evaluate_script - 执行JavaScript

执行自定义JavaScript代码进行验证或操作。

```json
{
  "action": "evaluate_script",
  "function": "() => document.querySelector('.status').textContent",
  "description": "获取状态文本"
}
```

**参数说明**：
- `function` (必需): JavaScript函数字符串，必须是可序列化的函数

---

## 验证类型详解

### element_exists - 元素存在验证

验证指定元素是否存在。

```json
{
  "type": "element_exists",
  "target": "success_message_uid",
  "description": "验证成功消息存在"
}
```

**查找方式**：
1. 如果target是uid，直接查找
2. 如果target是文本，在快照中搜索包含该文本的元素

### text_equals - 文本完全匹配

验证元素文本完全等于期望值。

```json
{
  "type": "text_equals",
  "target": "title_uid",
  "expected_value": "欢迎使用",
  "description": "验证标题文本"
}
```

### text_contains - 文本包含

验证元素文本包含期望值。

```json
{
  "type": "text_contains",
  "target": "message_uid",
  "expected_value": "成功",
  "description": "验证消息包含成功字样"
}
```

### url_equals - URL完全匹配

验证当前URL完全等于期望值。

```json
{
  "type": "url_equals",
  "expected_value": "https://example.com/dashboard",
  "description": "验证跳转到仪表盘"
}
```

### url_contains - URL包含

验证当前URL包含期望值。

```json
{
  "type": "url_contains",
  "expected_value": "/dashboard",
  "description": "验证URL包含dashboard路径"
}
```

### console_no_errors - 控制台无错误

验证控制台没有错误消息。

```json
{
  "type": "console_no_errors",
  "description": "验证页面无JavaScript错误"
}
```

### custom_script - 自定义验证

使用JavaScript进行自定义验证。

```json
{
  "type": "custom_script",
  "script": "() => document.querySelectorAll('.error').length === 0",
  "expected_value": true,
  "description": "验证页面无错误元素"
}
```

**参数说明**：
- `script` (必需): JavaScript函数字符串，返回验证结果
- `expected_value` (可选): 期望的返回值，不指定则验证返回值为truthy

---

## 完整示例

### 示例1: 登录测试

```json
{
  "test_name": "用户登录功能测试",
  "description": "验证用户可以使用正确的用户名和密码登录系统",
  "url": "https://example.com/login",
  "timeout": 30000,
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/login",
      "description": "导航到登录页面"
    },
    {
      "action": "snapshot",
      "description": "获取登录页面快照"
    },
    {
      "action": "fill",
      "target": "username_input",
      "value": "testuser",
      "description": "填写用户名"
    },
    {
      "action": "fill",
      "target": "password_input",
      "value": "testpass123",
      "description": "填写密码"
    },
    {
      "action": "click",
      "target": "login_button",
      "description": "点击登录按钮"
    },
    {
      "action": "wait_for",
      "text": "欢迎",
      "timeout": 5000,
      "description": "等待登录成功"
    },
    {
      "action": "snapshot",
      "description": "获取登录后页面快照"
    }
  ],
  "expected_results": [
    {
      "type": "url_contains",
      "expected_value": "/dashboard",
      "description": "验证跳转到仪表盘"
    },
    {
      "type": "element_exists",
      "target": "用户菜单",
      "description": "验证用户菜单存在"
    },
    {
      "type": "text_contains",
      "target": "欢迎消息",
      "expected_value": "testuser",
      "description": "验证欢迎消息包含用户名"
    },
    {
      "type": "console_no_errors",
      "description": "验证无控制台错误"
    }
  ]
}
```

### 示例2: 表单提交测试

```json
{
  "test_name": "联系表单提交测试",
  "description": "验证用户可以成功提交联系表单",
  "url": "https://example.com/contact",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/contact"
    },
    {
      "action": "snapshot"
    },
    {
      "action": "fill_form",
      "elements": [
        {"uid": "name_input", "value": "张三"},
        {"uid": "email_input", "value": "zhangsan@example.com"},
        {"uid": "phone_input", "value": "13800138000"},
        {"uid": "message_input", "value": "这是一条测试消息"}
      ],
      "description": "填写表单所有字段"
    },
    {
      "action": "click",
      "target": "submit_button",
      "description": "点击提交按钮"
    },
    {
      "action": "wait_for",
      "text": "提交成功",
      "timeout": 10000
    },
    {
      "action": "screenshot",
      "filePath": "contact_form_success.png"
    }
  ],
  "expected_results": [
    {
      "type": "text_contains",
      "target": "success_message",
      "expected_value": "提交成功",
      "description": "验证成功消息显示"
    },
    {
      "type": "custom_script",
      "script": "() => document.querySelector('.form').style.display === 'none'",
      "expected_value": true,
      "description": "验证表单已隐藏"
    }
  ]
}
```

---

## 自然语言转测试用例

当用户用自然语言描述测试需求时，需要转换为结构化测试用例。

### 转换规则

1. **识别操作动词**：
   - "打开"、"访问" → `navigate`
   - "点击" → `click`
   - "输入"、"填写" → `fill`
   - "等待" → `wait_for`
   - "验证"、"检查" → `expected_results`

2. **提取目标元素**：
   - 从描述中提取元素名称（按钮、输入框、链接等）
   - 通过snapshot定位实际uid

3. **识别验证点**：
   - "应该"、"必须"、"验证" → 预期结果
   - 提取期望的状态或值

### 示例转换

**自然语言**：
"测试登录功能：打开登录页面，输入用户名testuser和密码testpass，点击登录按钮，验证跳转到首页并显示欢迎消息"

**转换后的测试用例**：
```json
{
  "test_name": "登录功能测试",
  "steps": [
    {"action": "navigate", "url": "登录页面URL"},
    {"action": "fill", "target": "用户名输入框", "value": "testuser"},
    {"action": "fill", "target": "密码输入框", "value": "testpass"},
    {"action": "click", "target": "登录按钮"}
  ],
  "expected_results": [
    {"type": "url_contains", "expected_value": "首页路径"},
    {"type": "element_exists", "target": "欢迎消息"}
  ]
}
```

---

## 注意事项

1. **元素定位**：所有操作中的`target`应该是从`snapshot`获取的`uid`，而不是CSS选择器
2. **等待策略**：关键操作后应添加`wait_for`确保页面状态稳定
3. **错误处理**：测试用例应包含超时设置，避免无限等待
4. **数据隔离**：测试数据应独立，避免影响其他测试
5. **截图保存**：重要步骤和失败场景应保存截图用于调试

