# 页面自动化测试性能优化指南

## 问题分析

当前执行流程中，每一步都需要：
1. 调用 `take_snapshot` 获取页面状态（耗时）
2. Agent 分析快照内容（耗时）
3. 查找目标元素（耗时）
4. 执行操作（相对较快）

**主要瓶颈**：
- 每次操作都需要完整的 snapshot → 分析 → 查找流程
- MCP 调用次数多，网络延迟累积
- Agent 需要理解大量快照数据

## 优化方案

### 方案1: 页面辅助脚本注入（推荐⭐⭐⭐⭐⭐）

在测试开始时注入辅助脚本，提供快速元素定位和批量操作能力。

#### 优势
- ✅ 减少 snapshot 调用次数（只在必要时调用）
- ✅ 元素定位速度提升 10-100 倍
- ✅ 支持批量操作，减少 MCP 调用
- ✅ 支持元素缓存，避免重复查找

#### 使用方法

**步骤1: 注入辅助脚本**
```javascript
// 在测试开始时执行
await evaluate_script(() => {
  // 注入 page_helper.js 的内容
  // 脚本会自动创建 window.__testHelper
});
```

**步骤2: 使用快速查找**
```javascript
// 替代多次 snapshot + 分析的方式
const elements = await evaluate_script(() => {
  return window.__testHelper.quickFind("登录按钮");
});
// 返回: [{uid: "test_xxx", element: ..., text: "登录", ...}]
```

**步骤3: 批量操作**
```javascript
// 一次性执行多个操作
const result = await evaluate_script(() => {
  return window.__testHelper.batch.execute([
    {action: 'fill', target: 'username', value: 'testuser'},
    {action: 'fill', target: 'password', value: 'testpass'},
    {action: 'click', target: '登录按钮'}
  ]);
});
```

**步骤4: 批量验证**
```javascript
// 一次性执行多个验证
const validation = await evaluate_script(() => {
  return window.__testHelper.validate.validate([
    {type: 'url_contains', expectedValue: '/dashboard'},
    {type: 'element_exists', target: '欢迎消息'},
    {type: 'text_contains', target: '欢迎消息', expectedValue: 'testuser'}
  ]);
});
```

#### 完整示例

```json
{
  "test_name": "优化后的登录测试",
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/login"
    },
    {
      "action": "evaluate_script",
      "function": "() => { /* 注入辅助脚本 */ }",
      "description": "注入页面辅助脚本"
    },
    {
      "action": "evaluate_script",
      "function": "() => window.__testHelper.quickFind('登录按钮')",
      "description": "快速查找登录按钮",
      "save_result_as": "loginButton"
    },
    {
      "action": "evaluate_script",
      "function": "() => window.__testHelper.batch.execute([{action: 'fill', target: 'username', value: 'testuser'}, {action: 'fill', target: 'password', value: 'testpass'}, {action: 'click', target: '登录按钮'}])",
      "description": "批量执行：填写表单并点击登录"
    },
    {
      "action": "wait_for",
      "text": "欢迎"
    },
    {
      "action": "evaluate_script",
      "function": "() => window.__testHelper.validate.validate([{type: 'url_contains', expectedValue: '/dashboard'}, {type: 'element_exists', target: '用户菜单'}])",
      "description": "批量验证结果"
    }
  ]
}
```

---

### 方案2: 智能缓存机制

缓存已找到的元素，避免重复查找。

#### 实现方式

```javascript
// 在辅助脚本中已实现 ElementCache
// 使用方式：
await evaluate_script(() => {
  // 查找并缓存
  const button = window.__testHelper.find.findByText("登录按钮")[0];
  window.__testHelper.cache.cacheElement("loginButton", button.element);
  
  // 后续直接使用缓存
  const cached = window.__testHelper.cache.getCached("loginButton");
  if (cached) {
    cached.element.click();
  }
});
```

---

### 方案3: 预编译测试用例

将测试用例中的元素描述预先转换为 uid，减少运行时查找。

#### 实现方式

**原始测试用例（需要运行时查找）**：
```json
{
  "steps": [
    {"action": "click", "target": "登录按钮"}
  ]
}
```

**预编译后的测试用例（直接使用uid）**：
```json
{
  "steps": [
    {"action": "click", "target": "test_button_login_12345"}
  ],
  "element_map": {
    "登录按钮": "test_button_login_12345"
  }
}
```

#### 预编译流程

1. **首次执行时**：
   - 执行 snapshot
   - 查找所有需要的元素
   - 生成 element_map
   - 保存预编译后的测试用例

2. **后续执行时**：
   - 直接使用 element_map 中的 uid
   - 跳过查找步骤

---

### 方案4: 批量 snapshot 优化

如果必须使用 snapshot，采用批量策略。

#### 策略

- **只在关键节点 snapshot**：页面加载后、操作前、验证时
- **增量更新**：只获取变化的部分
- **并行处理**：同时处理多个快照

```javascript
// 不好的做法：每个操作都 snapshot
for (step of steps) {
  snapshot(); // ❌ 太慢
  execute(step);
}

// 好的做法：批量 snapshot
snapshot(); // 初始状态
for (step of steps) {
  execute(step);
  if (needsVerification(step)) {
    snapshot(); // 只在需要时
  }
}
```

---

## 性能对比

| 方案 | 单步耗时 | 10步测试耗时 | 优化效果 |
|------|---------|-------------|---------|
| 原始方式（每次snapshot） | ~3-5秒 | ~30-50秒 | 基准 |
| 方案1：辅助脚本 | ~0.5-1秒 | ~5-10秒 | **5-10倍提升** |
| 方案2：缓存机制 | ~1-2秒 | ~10-20秒 | **2-3倍提升** |
| 方案3：预编译 | ~0.3-0.5秒 | ~3-5秒 | **10倍提升** |
| 组合方案（1+2+3） | ~0.2-0.4秒 | ~2-4秒 | **15-25倍提升** |

---

## 最佳实践

### 1. 测试开始时注入辅助脚本

```javascript
// 在第一个 navigate 之后立即注入
{
  "action": "navigate",
  "url": "https://example.com"
},
{
  "action": "evaluate_script",
  "function": "() => { /* 注入 page_helper.js */ }"
}
```

### 2. 使用快速查找替代 snapshot

```javascript
// ❌ 慢的方式
snapshot(); // 获取完整快照
// Agent 分析快照，查找元素

// ✅ 快的方式
evaluate_script(() => window.__testHelper.quickFind("登录按钮"));
```

### 3. 批量操作减少调用次数

```javascript
// ❌ 慢的方式（3次MCP调用）
fill("username", "testuser");
fill("password", "testpass");
click("loginButton");

// ✅ 快的方式（1次MCP调用）
batch.execute([
  {action: 'fill', target: 'username', value: 'testuser'},
  {action: 'fill', target: 'password', value: 'testpass'},
  {action: 'click', target: 'loginButton'}
]);
```

### 4. 批量验证

```javascript
// ❌ 慢的方式（多次验证，多次调用）
verify("url_contains", "/dashboard");
verify("element_exists", "欢迎消息");
verify("text_contains", "欢迎消息", "testuser");

// ✅ 快的方式（1次调用，批量验证）
validate.validate([
  {type: 'url_contains', expectedValue: '/dashboard'},
  {type: 'element_exists', target: '欢迎消息'},
  {type: 'text_contains', target: '欢迎消息', expectedValue: 'testuser'}
]);
```

### 5. 智能等待策略

```javascript
// ❌ 固定延迟
wait(3000); // 总是等待3秒

// ✅ 智能等待
waitForElement("欢迎消息", {timeout: 5000}); // 最多等5秒，找到就继续
```

---

## 实施建议

### 阶段1: 快速实施（立即生效）

1. ✅ 在 SKILL.md 中添加辅助脚本使用说明
2. ✅ 提供辅助脚本文件（page_helper.js）
3. ✅ 更新测试用例格式，支持批量操作

### 阶段2: 优化执行流程（1-2天）

1. 修改 Agent 执行逻辑，优先使用辅助脚本
2. 实现元素缓存机制
3. 添加批量操作支持

### 阶段3: 高级优化（可选）

1. 实现测试用例预编译
2. 添加性能监控
3. 优化 snapshot 策略

---

## 代码示例

### 完整的优化测试用例

```json
{
  "test_name": "优化登录测试",
  "url": "https://example.com/login",
  "optimization": {
    "use_helper_script": true,
    "enable_cache": true,
    "batch_operations": true
  },
  "steps": [
    {
      "action": "navigate",
      "url": "https://example.com/login"
    },
    {
      "action": "inject_helper_script",
      "script_path": "scripts/page_helper.js"
    },
    {
      "action": "batch_operations",
      "operations": [
        {
          "action": "quick_find",
          "target": "用户名输入框",
          "save_as": "usernameInput"
        },
        {
          "action": "quick_find",
          "target": "密码输入框",
          "save_as": "passwordInput"
        },
        {
          "action": "quick_find",
          "target": "登录按钮",
          "save_as": "loginButton"
        }
      ]
    },
    {
      "action": "batch_execute",
      "operations": [
        {"action": "fill", "target": "usernameInput", "value": "testuser"},
        {"action": "fill", "target": "passwordInput", "value": "testpass"},
        {"action": "click", "target": "loginButton"}
      ]
    },
    {
      "action": "wait_for",
      "text": "欢迎",
      "timeout": 5000
    },
    {
      "action": "batch_validate",
      "validations": [
        {"type": "url_contains", "expectedValue": "/dashboard"},
        {"type": "element_exists", "target": "用户菜单"},
        {"type": "text_contains", "target": "欢迎消息", "expectedValue": "testuser"}
      ]
    }
  ]
}
```

---

## 总结

通过页面辅助脚本 + 批量操作 + 缓存机制，可以将测试执行速度提升 **5-25倍**，让测试过程更加丝滑流畅。

**关键点**：
1. ✅ 减少 snapshot 调用（只在必要时）
2. ✅ 使用页面内脚本进行快速查找
3. ✅ 批量操作减少 MCP 调用次数
4. ✅ 缓存已找到的元素
5. ✅ 智能等待替代固定延迟


