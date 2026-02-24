# BKLog 前端页面 Selector 映射表

本文档提供 BKLog 日志平台前端页面的元素定位映射表，用于页面自动化测试。根据 `page-automation-tester` skill 的要求，优先使用快照定位（snapshot），同时提供多种定位策略作为备选。

## 使用说明

### 定位优先级

1. **快照定位（推荐）**：使用 `take_snapshot` 获取页面快照，通过文本、角色等属性查找元素的 `uid`
2. **文本定位**：通过元素的可见文本内容定位
3. **角色定位**：通过 ARIA role 属性定位
4. **选择器定位**：作为最后备选，使用 CSS 选择器或 XPath

### 在测试用例中的使用

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

---

## 一、页面导航与业务选择

### 1.1 业务选择器

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 业务选择器 | 文本定位 | "业务"、"选择业务" | `role="button"` | `.bk-select`, `[data-test-id="business-selector"]` | 页面顶部业务下拉选择器 |
| demo业务选项 | 文本定位 | "demo" | - | `.bk-option:contains("demo")` | 业务列表中的demo选项 |

### 1.2 索引集选择

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 索引集选择器 | 文本定位 | "索引集" | - | `[data-test-id="retrieve_div_dataQueryBox"] .select-index-set` | 检索条件区域的索引集选择器 |
| 容器日志索引集 | 文本定位 | "容器日志"、"容器日志采集示例" | - | `.bk-option:contains("容器日志")` | 索引集列表中的容器日志选项 |

---

## 二、检索功能区域

### 2.1 检索模式切换

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| UI模式按钮 | 文本定位 | "UI模式"、"表单模式" | `role="tab"` | `.king-tab .tab-item:contains("UI")` | 切换到UI检索模式 |
| 语句模式按钮 | 文本定位 | "语句模式"、"查询语句" | `role="tab"` | `.king-tab .tab-item:contains("语句")` | 切换到语句检索模式 |

### 2.2 UI模式检索

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段选择下拉框 | 文本定位 | "添加条件"、"选择字段" | `role="combobox"` | `.condition-comp .bk-select` | 添加检索条件的字段选择器 |
| 操作符选择器 | 文本定位 | "包含"、"等于"、"大于" | `role="combobox"` | `.condition-comp .operator-select` | 字段操作符选择器 |
| 值输入框 | 文本定位 | - | `role="textbox"` | `.condition-comp input[type="text"]` | 条件值输入框 |
| level筛选输入框 | 文本定位 | "level"、"日志级别" | `role="textbox"` | `input[placeholder*="level"], input[name*="level"]` | 日志级别筛选输入框 |
| 检索按钮 | 文本定位 | "检索"、"查询"、"搜索" | `role="button"` | `.search-comp .retrieve-btn, button:contains("检索")` | 执行检索操作的按钮 |

### 2.3 语句模式检索

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 查询语句输入框 | 文本定位 | "查询语句"、"可输入DSL语句" | `role="textbox"` | `.query-statement textarea, .query-statement input` | 语句模式的多行输入框 |
| 查询历史按钮 | 文本定位 | "查询历史" | `role="button"` | `.query-statement .history-btn` | 查看查询历史记录 |

### 2.4 时间范围选择

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 时间选择器 | 文本定位 | "时间范围"、"选择时间" | `role="button"` | `.time-range-picker, .bk-date-picker` | 时间范围选择器 |
| 快捷时间选项 | 文本定位 | "最近1小时"、"今天"、"昨天" | - | `.time-range-option` | 快捷时间选择选项 |

---

## 三、检索结果区域

### 3.1 结果列表

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 日志列表容器 | 文本定位 | - | `role="table"` | `.result-table-panel, .original-log-list` | 日志结果列表容器 |
| 第一条日志行 | 文本定位 | - | `role="row"` | `.log-row:first-child, .table-row:first-child` | 结果列表的第一条日志 |
| 日志内容单元格 | 文本定位 | - | `role="cell"` | `.log-content-cell, .log-message` | 日志内容显示区域 |
| 结果统计信息 | 文本定位 | "条结果"、"共" | - | `.result-header .total-count` | 显示检索结果总数 |

### 3.2 日志操作按钮

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 上下文按钮 | 文本定位 | "上下文" | `role="button"` | `.context-btn, .operator-tools .context-button` | 查看日志上下文的按钮 |
| 第一条日志的上下文按钮 | 文本定位 | "上下文" | `role="button"` | `.log-row:first-child .context-btn` | 第一条日志行的上下文按钮 |
| 复制按钮 | 文本定位 | "复制" | `role="button"` | `.copy-btn, .operator-tools .copy-button` | 复制日志内容按钮 |
| 导出按钮 | 文本定位 | "导出" | `role="button"` | `.export-btn, .result-header .export-button` | 导出日志按钮 |

---

## 四、上下文功能区域

### 4.1 上下文面板

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 上下文面板容器 | 文本定位 | "上下文" | `role="dialog"` | `.context-log-wrapper, .log-full-dialog-wrapper` | 上下文日志面板主容器 |
| 上下文标题 | 文本定位 | "上下文"、"IP"、"日志路径" | - | `.context-log-wrapper .dialog-title` | 上下文面板标题区域 |
| 上下文日志内容 | 文本定位 | - | `role="log"` | `.context-log-wrapper .log-view, .dialog-log-markdown` | 上下文日志内容显示区域 |
| 参考日志区域 | 文本定位 | "参考日志" | - | `.context-log-wrapper .reference-log` | 参考日志对比区域 |

### 4.2 上下文控制功能

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 高亮输入框 | 文本定位 | "高亮"、"关键字" | `role="textbox"` | `.context-log-wrapper input[placeholder*="高亮"], .log-view-control input` | 上下文高亮关键字输入框 |
| 高亮应用按钮 | 文本定位 | "应用"、"搜索" | `role="button"` | `.log-view-control .apply-highlight-btn` | 应用高亮设置的按钮 |
| 全屏按钮 | 文本定位 | "全屏" | `role="button"` | `.context-log-wrapper .bklog-full-screen-log` | 上下文面板全屏按钮 |
| 字段配置按钮 | 文本定位 | - | `role="button"` | `.context-log-wrapper .bklog-set-icon` | 字段显示配置按钮 |
| 关闭按钮 | 文本定位 | "关闭"、"×" | `role="button"` | `.context-log-wrapper .close-btn, [aria-label="关闭"]` | 关闭上下文面板按钮 |

### 4.3 上下文过滤功能

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 数据过滤组件 | 文本定位 | "过滤" | - | `.context-log-wrapper .data-filter` | 上下文数据过滤组件 |
| 固定当前行按钮 | 文本定位 | "固定" | `role="button"` | `.data-filter .fix-current-row-btn` | 固定当前查看的日志行 |

---

## 五、字段过滤与统计

### 5.1 字段过滤区域

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 查询结果统计标题 | 文本定位 | "查询结果统计" | - | `[data-test-id="retrieve_div_fieldFilterBox"] .tab-item-title` | 字段过滤区域标题 |
| 字段过滤组件 | 文本定位 | - | - | `.field-filter-comp` | 字段过滤主组件 |
| 字段项 | 文本定位 | 字段名称 | - | `.field-filter-item` | 单个字段过滤项 |

---

## 六、通用元素

### 6.1 加载状态

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 加载指示器 | 文本定位 | - | `role="progressbar"` | `.page-loading-wrap, .bk-loading` | 页面加载中的指示器 |
| 加载完成 | 文本定位 | - | - | - | 等待加载指示器消失 |

### 6.2 错误提示

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 错误提示 | 文本定位 | "错误"、"失败" | `role="alert"` | `.bk-message-error, .error-message` | 错误提示消息 |
| 无数据提示 | 文本定位 | "检索无数据"、"无结果" | - | `.empty-status, .no-data` | 无检索结果提示 |

### 6.3 确认对话框

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 确认按钮 | 文本定位 | "确认"、"确定" | `role="button"` | `.bk-dialog .confirm-btn, button:contains("确认")` | 对话框确认按钮 |
| 取消按钮 | 文本定位 | "取消" | `role="button"` | `.bk-dialog .cancel-btn, button:contains("取消")` | 对话框取消按钮 |

---

## 七、定位策略示例

### 示例1：定位业务选择器

**方式1：通过快照定位（推荐）**
```json
{
  "action": "snapshot",
  "description": "获取页面快照"
}
// 在快照中查找包含"业务"文本的元素，获取其uid
{
  "action": "click",
  "target": "业务选择器",  // Agent会在快照中查找包含此文本的元素
  "description": "点击业务选择器"
}
```

**方式2：使用辅助脚本快速定位**
```javascript
// 注入辅助脚本后
evaluate_script(() => {
  const helper = window.__testHelper;
  const results = helper.find.findByText("业务");
  return results.length > 0 ? results[0].uid : null;
})
```

### 示例2：定位检索输入框

**UI模式下的level筛选**
```json
{
  "action": "snapshot",
  "description": "获取检索区域快照"
}
{
  "action": "fill",
  "target": "level筛选输入框",  // 查找包含"level"的输入框
  "value": "WARN",
  "description": "输入WARN级别筛选"
}
```

**语句模式下的查询语句输入**
```json
{
  "action": "click",
  "target": "语句模式按钮",
  "description": "切换到语句模式"
}
{
  "action": "fill",
  "target": "查询语句输入框",
  "value": "log:ERROR",
  "description": "输入查询语句"
}
```

### 示例3：定位上下文按钮

```json
{
  "action": "snapshot",
  "description": "获取日志列表快照"
}
{
  "action": "click",
  "target": "第一条日志的上下文按钮",  // 查找第一条日志行中的上下文按钮
  "description": "点击第一条日志的上下文按钮"
}
```

---

## 八、特殊场景定位

### 8.1 动态生成的元素

对于动态生成的元素（如日志列表项），建议：

1. **使用相对定位**：先定位父容器，再定位子元素
2. **使用索引定位**：如"第一条日志"、"第二条日志"
3. **使用内容定位**：通过日志内容中的特定文本定位

### 8.2 模态框和抽屉

模态框和抽屉通常有遮罩层，定位时：

1. **等待元素出现**：使用 `wait_for` 等待模态框标题出现
2. **通过遮罩定位**：查找遮罩层下的内容区域
3. **使用role属性**：模态框通常有 `role="dialog"`

### 8.3 下拉菜单和选择器

下拉菜单的定位策略：

1. **点击触发器**：先点击触发下拉的元素
2. **等待选项出现**：使用 `wait_for` 等待选项列表出现
3. **选择选项**：通过文本定位选项并点击

---

## 九、测试用例示例

### 完整测试用例：检索WARN日志并查看上下文

```json
{
  "test_name": "BKLog检索与上下文功能测试",
  "description": "测试业务选择、WARN日志检索、上下文查看和高亮功能",
  "url": "https://bklog.woa.com",
  "steps": [
    {
      "action": "navigate",
      "url": "https://bklog.woa.com",
      "description": "导航到日志平台"
    },
    {
      "action": "snapshot",
      "description": "获取页面快照，定位业务选择器"
    },
    {
      "action": "click",
      "target": "业务选择器",
      "description": "点击业务选择器"
    },
    {
      "action": "click",
      "target": "demo业务选项",
      "description": "选择demo业务"
    },
    {
      "action": "snapshot",
      "description": "获取检索页面快照"
    },
    {
      "action": "click",
      "target": "索引集选择器",
      "description": "点击索引集选择器"
    },
    {
      "action": "click",
      "target": "容器日志索引集",
      "description": "选择容器日志索引集"
    },
    {
      "action": "fill",
      "target": "level筛选输入框",
      "value": "WARN",
      "description": "在level筛选中输入WARN"
    },
    {
      "action": "press_key",
      "key": "Enter",
      "description": "按Enter执行检索"
    },
    {
      "action": "wait_for",
      "text": "条结果",
      "timeout": 10000,
      "description": "等待检索结果加载"
    },
    {
      "action": "snapshot",
      "description": "获取结果列表快照"
    },
    {
      "action": "click",
      "target": "第一条日志的上下文按钮",
      "description": "点击第一条日志的上下文按钮"
    },
    {
      "action": "wait_for",
      "text": "上下文",
      "timeout": 5000,
      "description": "等待上下文面板打开"
    },
    {
      "action": "snapshot",
      "description": "获取上下文面板快照"
    },
    {
      "action": "fill",
      "target": "高亮输入框",
      "value": "123",
      "description": "在高亮输入框中输入123"
    },
    {
      "action": "press_key",
      "key": "Enter",
      "description": "应用高亮"
    }
  ],
  "expected_results": [
    {
      "type": "element_exists",
      "target": "上下文面板容器",
      "description": "验证上下文面板已打开"
    },
    {
      "type": "element_exists",
      "target": "上下文日志内容",
      "description": "验证上下文日志内容已显示"
    }
  ]
}
```

---

## 十、注意事项

1. **元素定位的稳定性**：
   - 优先使用文本定位，因为文本内容相对稳定
   - 避免使用过于具体的选择器，页面结构变化时容易失效
   - 使用 `data-test-id` 等测试属性时，需要确认代码中已添加

2. **等待策略**：
   - 关键操作后使用 `wait_for` 等待页面状态稳定
   - 异步加载的内容需要等待加载完成

3. **元素可见性**：
   - 确保元素在视口中可见
   - 某些元素可能需要滚动才能看到

4. **多实例元素**：
   - 当页面存在多个相同类型的元素时，使用更具体的定位策略
   - 可以通过父容器或上下文来区分

5. **国际化支持**：
   - 文本定位需要考虑多语言情况
   - 建议使用英文或通用的标识符作为备选

---

## 更新日志

- **2025-01-XX**：初始版本，基于 bk-monitor 代码库分析创建
- 后续根据页面变化和测试需求持续更新

---

## 参考资源

- [page-automation-tester SKILL.md](../skill/page-automation-tester/SKILL.md)
- [测试用例格式说明](../skill/page-automation-tester/references/test_case_format.md)
- [页面辅助脚本](../skill/page-automation-tester/scripts/page_helper.js)


