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
| 下载按钮 | 文本定位/属性定位 | "下载"、"bklog-download" | `data-test-id="fieldForm_div_exportData"` | `[data-test-id="fieldForm_div_exportData"], .operation-icon .bklog-download` | 日志下载主按钮，鼠标悬停显示下拉菜单 |
| 下载日志选项 | 文本定位 | "下载日志" | - | `.download-box span:contains("下载日志")` | 下载下拉菜单中的"下载日志"选项 |
| 下载历史选项 | 文本定位 | "下载历史" | - | `.download-box span:contains("下载历史")` | 下载下拉菜单中的"下载历史"选项 |
| 实时日志按钮 | 文本定位 | "实时日志"、"实时查看" | `role="button"` | `.real-time-log-btn, .realtime-btn` | 打开实时日志查看的按钮 |

### 3.3 表格操作

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段设置按钮 | 文本定位/图标定位 | "字段设置"、"设置" | `role="button"` | `.fields-setting-btn, .bklog-set-icon` | 打开字段显示设置面板的按钮 |
| 排序按钮 | 文本定位 | - | - | `.bk-table .sort-column, th.sortable` | 表格列头的排序按钮（点击列头可排序） |
| 分页组件 | 文本定位 | "条/页"、"上一页"、"下一页" | - | `.bk-pagination, .pagination` | 结果列表的分页组件 |
| 每页条数选择 | 文本定位 | "条/页" | `role="combobox"` | `.bk-pagination .page-size-select` | 选择每页显示条数的下拉框 |

---

## 四、下载功能区域

### 4.1 下载对话框

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 下载对话框 | 文本定位 | "日志下载" | `role="dialog"` | `.async-export-dialog, .bk-dialog:contains("日志下载")` | 下载配置对话框主容器 |
| 下载对话框标题 | 文本定位 | "日志下载" | - | `.async-export-dialog .bk-dialog-header` | 下载对话框标题 |
| 下载按钮（对话框确认） | 文本定位 | "下载" | `role="button"` | `.async-export-dialog .bk-dialog-footer .bk-button-primary` | 下载对话框的确认下载按钮 |
| 数据量显示 | 文本定位 | "条结果"、"当前数据量级" | - | `.log-num-container .log-num` | 显示当前检索结果数据量 |
| 预计下载时长 | 文本定位 | "预计下载时长" | - | `.log-num-container .log-unit` | 显示预计下载时长 |

### 4.2 下载模式选择

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 下载模式标题 | 文本定位 | "下载模式" | - | `.filed-select-box .middle-title:contains("下载模式")` | 下载模式选择区域标题 |
| 全文下载选项 | 文本定位 | "全文下载" | `role="radio"` | `.filed-radio-box input[value="all"]` | 全文下载模式单选项 |
| 快速下载选项 | 文本定位 | "快速下载" | `role="radio"` | `.filed-radio-box input[value="quick"]` | 快速下载模式单选项（提速100%+） |
| 取样下载选项 | 文本定位 | "取样下载" | `role="radio"` | `.filed-radio-box input[value="sampling"]` | 取样下载模式单选项（前1万条） |

### 4.3 下载范围选择

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 下载范围标题 | 文本定位 | "下载范围" | - | `.filed-select-box .middle-title:contains("下载范围")` | 下载范围选择区域标题 |
| 全部字段选项 | 文本定位 | "全部字段" | `role="radio"` | `.filed-radio-box input[value="all"]` | 下载全部字段单选项 |
| 当前显示字段选项 | 文本定位 | "当前显示字段" | `role="radio"` | `.filed-radio-box input[value="show"]` | 下载当前显示字段单选项 |
| 指定字段选项 | 文本定位 | "指定字段" | `role="radio"` | `.filed-radio-box input[value="specify"]` | 下载指定字段单选项 |
| 字段选择下拉框 | 文本定位 | "未选择则默认为全部字段" | `role="combobox"` | `.filed-select-box .bk-select` | 指定字段模式下的字段多选下拉框 |

### 4.4 下载历史

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 下载历史对话框 | 文本定位 | "下载历史" | `role="dialog"` | `.bk-dialog:contains("下载历史")` | 下载历史记录对话框 |
| 查看所有按钮 | 文本定位 | "查看所有" | `role="button"` | `.search-history .bk-button-primary` | 查看所有索引集的下载历史 |
| 下载历史表格 | 文本定位 | - | `role="table"` | `.export-table` | 下载历史记录表格 |
| 下载链接按钮 | 文本定位 | "下载" | `role="button"` | `.export-table .download-link-btn` | 下载历史中已完成任务的下载链接 |

### 4.5 图表数据下载

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 图表下载按钮 | 文本定位/图标定位 | "下载"、"icon-download" | `role="button"` | `.chart-toolbar .download-btn, .icon-download` | 图表分析中的数据下载按钮 |

### 4.6 聚类下载

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 聚类下载按钮 | 文本定位/图标定位 | "聚类下载"、"download" | `role="button"` | `.download-main .download, .clustering-nav .download` | 日志聚类结果下载按钮 |
| 聚类下载图标 | 图标定位 | - | - | `.log-icon[type="download"]` | 聚类下载图标按钮 |

### 4.7 规则导出

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 导出规则按钮 | 文本定位 | "导出"、"导出规则" | `role="button"` | `.operate-btn:contains("导出"), button:contains("导出规则")` | 聚类规则导出按钮（在规则管理或聚类配置中） |

---

## 五、上下文功能区域

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

## 六、字段过滤与统计

### 6.1 字段过滤区域容器

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 查询结果统计标题 | 文本定位 | "查询结果统计" | - | `[data-test-id="retrieve_div_fieldFilterBox"] .tab-item-title` | 字段过滤区域标题 |
| 字段过滤组件容器 | 文本定位/属性定位 | - | `data-test-id="retrieve_div_fieldFilterBox"` | `[data-test-id="retrieve_div_fieldFilterBox"], .field-filter-container` | 字段过滤主组件容器 |

### 6.2 字段搜索和过滤

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段搜索输入框 | 文本定位/属性定位 | "搜索字段名" | `data-test-id="fieldFilter_input_searchFieldName"` | `[data-test-id="fieldFilter_input_searchFieldName"], .field-filter-container input[placeholder*="搜索"]` | 搜索字段名称的输入框 |
| 字段类型过滤按钮 | 文本定位 | "字段类型" | `role="button"` | `[data-test-id="fieldFilter_div_phrasesSearch"], .field-filter-popover-trigger` | 打开字段类型过滤弹窗的按钮 |
| 字段类型过滤弹窗 | 文本定位 | "是否可聚合"、"字段类型" | - | `.filter-popover-content` | 字段类型和聚合过滤弹窗 |
| 是否可聚合选项 | 文本定位 | "不限"、"是"、"否" | `role="radio"` | `.filter-popover-content .king-radio-group input[value="0/1/2"]` | 是否可聚合的单选项 |
| 字段类型选项 | 文本定位 | "不限"、"数字"、"字符串"、"文本"、"时间"、"虚拟字段" | `role="button"` | `.filter-popover-content .bk-button-group .bk-button` | 字段类型选择按钮组 |
| 过滤确认按钮 | 文本定位 | "确定" | `role="button"` | `.filter-popover-content .king-button.primary` | 确认字段过滤条件 |
| 过滤取消按钮 | 文本定位 | "取消" | `role="button"` | `.filter-popover-content .king-button:not(.primary)` | 取消字段过滤 |

### 6.3 显示字段列表

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 显示字段区域 | 文本定位 | "显示字段" | - | `.fields-container.selected` | 当前显示的字段列表区域 |
| 显示字段列表 | 文本定位 | - | - | `.fields-container.selected .filed-list` | 显示字段的列表容器 |
| 显示字段项 | 文本定位 | 字段名称 | - | `.fields-container.selected .filed-item-old` | 单个显示字段项 |
| 字段拖拽图标 | 图标定位 | - | - | `.bklog-drag-dots` | 字段拖拽排序的拖拽点图标 |

### 6.4 索引字段列表

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 索引字段区域 | 文本定位 | "索引字段" | - | `.fields-container.not-selected:contains("索引字段")` | 索引字段列表区域 |
| 索引字段列表 | 文本定位 | - | - | `.fields-container .filed-list` | 索引字段列表容器 |
| 索引字段项 | 文本定位 | 字段名称 | - | `.fields-container .filed-item-old` | 单个索引字段项 |
| 展开全部按钮 | 文本定位 | "展开全部"、"收起" | `role="button"` | `.expand-all` | 展开或收起所有索引字段 |

### 6.5 可选字段列表

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 可选字段区域 | 文本定位 | "可选字段" | - | `.fields-container.optional-field` | 可选字段列表区域 |
| 可选字段列表 | 文本定位 | - | - | `.fields-container.optional-field .filed-list` | 可选字段列表容器 |
| 可选字段项 | 文本定位 | 字段名称 | - | `.fields-container.optional-field .filed-item-old` | 单个可选字段项 |

### 6.6 内置字段列表

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 内置字段区域 | 文本定位 | "内置字段" | - | `.fields-container:contains("内置字段")` | 内置字段列表区域 |
| 内置字段列表 | 文本定位 | - | - | `.fields-container .filed-list` | 内置字段列表容器 |
| 内置字段项 | 文本定位 | 字段名称 | - | `.fields-container .filed-item-old` | 单个内置字段项 |
| 展开全部按钮（内置字段） | 文本定位 | "展开全部"、"收起" | `role="button"` | `.fields-container:contains("内置字段") .expand-all` | 展开或收起所有内置字段 |

### 6.7 字段项操作

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段名称 | 文本定位 | 字段名称 | - | `.filed-item-old .field-name` | 字段名称显示区域 |
| 字段类型图标 | 图标定位 | - | - | `.field-type-icon` | 字段类型对应的图标 |
| 字段统计数量 | 文本定位 | 数字（括号内） | - | `.field-count` | 字段统计数量显示 |
| 字段展开图标 | 图标定位 | - | - | `.icon-right-shape, .bk-icon` | 展开字段聚合信息的三角图标 |
| 显示/隐藏字段按钮 | 图标定位 | "点击显示"、"点击隐藏" | `role="button"` | `.operation-icon-box .include-icon, .icon-eye, .icon-eye-slash` | 显示或隐藏字段的眼睛图标按钮 |
| 图表分析按钮 | 图标定位 | "图表分析" | `role="button"` | `.operation-icon-box .bklog-log-trend` | 打开字段图表分析的按钮 |
| 字段聚合图表 | 文本定位 | - | - | `.agg-chart` | 字段展开后显示的聚合统计图表 |

### 6.8 字段拖拽排序

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段拖拽点 | 图标定位 | - | - | `.bklog-drag-dots` | 字段拖拽排序的拖拽点（显示字段区域） |
| 字段列表容器（可拖拽） | 文本定位 | - | - | `.fields-container.selected .filed-list` | 支持拖拽排序的字段列表容器 |

---

## 七、收藏功能区域

### 7.1 收藏操作

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 收藏按钮 | 文本定位 | "收藏"、"保存" | `role="button"` | `.favorite-btn, .save-favorite-btn` | 保存当前检索条件为收藏 |
| 收藏列表 | 文本定位 | "收藏" | - | `.favorite-list, .collect-container` | 收藏列表容器 |
| 收藏项 | 文本定位 | 收藏名称 | - | `.favorite-item, .collect-item` | 单个收藏项 |
| 新建收藏按钮 | 文本定位 | "新建收藏"、"添加收藏" | `role="button"` | `.add-favorite-btn, .create-favorite-btn` | 创建新收藏的按钮 |
| 编辑收藏按钮 | 文本定位 | "编辑" | `role="button"` | `.edit-favorite-btn` | 编辑收藏的按钮 |
| 删除收藏按钮 | 文本定位 | "删除" | `role="button"` | `.delete-favorite-btn` | 删除收藏的按钮 |

---

## 八、实时日志功能区域

### 8.1 实时日志面板

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 实时日志对话框 | 文本定位 | "实时日志" | `role="dialog"` | `.real-time-log-dialog, .realtime-log-wrapper` | 实时日志查看对话框 |
| 实时日志内容区域 | 文本定位 | - | `role="log"` | `.real-time-log-content, .realtime-log-list` | 实时日志内容显示区域 |
| 暂停/继续按钮 | 文本定位 | "暂停"、"继续" | `role="button"` | `.pause-btn, .resume-btn` | 暂停或继续实时日志刷新 |
| 清空日志按钮 | 文本定位 | "清空" | `role="button"` | `.clear-log-btn` | 清空当前显示的实时日志 |
| 自动滚动开关 | 文本定位 | "自动滚动" | `role="checkbox"` | `.auto-scroll-switch` | 自动滚动到底部的开关 |

---

## 九、字段设置功能区域

### 9.1 字段设置面板

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 字段设置面板 | 文本定位 | "字段设置" | - | `.fields-setting-container, .field-setting-panel` | 字段显示配置面板 |
| 显示字段列表 | 文本定位 | "显示字段" | - | `.display-fields-list` | 已选择显示的字段列表 |
| 字段复选框 | 文本定位 | 字段名称 | `role="checkbox"` | `.field-checkbox, input[type="checkbox"]` | 字段的显示/隐藏复选框 |
| 字段宽度输入框 | 文本定位 | - | `role="textbox"` | `.field-width-input` | 设置字段显示宽度的输入框 |
| 确认按钮 | 文本定位 | "确认"、"确定" | `role="button"` | `.fields-setting .confirm-btn` | 确认字段设置 |
| 重置按钮 | 文本定位 | "重置" | `role="button"` | `.fields-setting .reset-btn` | 重置字段设置为默认 |

---

## 十、日志聚类功能区域

### 10.1 聚类开关和模式

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 聚类开关 | 文本定位 | "日志聚类"、"聚类" | `role="switch"` | `.cluster-switch, .clustering-toggle` | 开启/关闭日志聚类功能的开关 |
| 聚类模式切换 | 文本定位 | "数据指纹"、"聚类模式" | `role="tab"` | `.clustering-mode-tab` | 切换聚类显示模式 |
| 聚类结果列表 | 文本定位 | - | `role="table"` | `.cluster-result-list, .finger-list` | 聚类结果（数据指纹）列表 |

### 10.2 聚类操作

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 聚类配置按钮 | 文本定位 | "配置"、"聚类配置" | `role="button"` | `.cluster-config-btn` | 打开聚类配置对话框 |
| 聚类策略按钮 | 文本定位 | "策略"、"聚类策略" | `role="button"` | `.cluster-strategy-btn` | 打开聚类策略配置 |
| 快速过滤按钮 | 文本定位 | "快速过滤" | `role="button"` | `.quick-filter-btn` | 快速过滤聚类结果 |

---

## 十一、图表分析功能区域

### 11.1 图表显示

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 趋势图表容器 | 文本定位/属性定位 | - | `data-test-id="retrieve_div_generalTrendEcharts"` | `[data-test-id="retrieve_div_generalTrendEcharts"], .monitor-echarts-container` | 趋势图表主容器 |
| 图表标题 | 文本定位 | - | - | `.chart-title` | 图表标题区域 |
| 图表工具栏 | 文本定位 | - | - | `.chart-toolbar` | 图表工具栏（包含下载、刷新等） |
| 图表折叠按钮 | 文本定位 | "折叠"、"展开" | `role="button"` | `.chart-fold-btn` | 折叠/展开图表 |

### 11.2 图表操作

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 图表刷新按钮 | 文本定位/图标定位 | "刷新" | `role="button"` | `.chart-refresh-btn, .icon-refresh` | 刷新图表数据 |
| 图表时间选择 | 文本定位 | - | - | `.chart-time-picker` | 图表时间范围选择器 |

---

## 十二、IP选择器功能区域

### 12.1 IP选择器

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| IP选择器按钮 | 文本定位 | "选择服务器"、"选择主机" | `role="button"` | `[data-test-id="addNewExtraction_button_selectTheServer"], .ip-selector-btn` | 打开IP选择器的按钮 |
| IP选择器对话框 | 文本定位 | "选择主机" | `role="dialog"` | `.ip-selector-dialog, .log-ip-selector` | IP选择器主对话框 |
| 静态拓扑面板 | 文本定位 | "静态拓扑" | `role="tab"` | `.ip-selector .static-topo-tab` | 静态拓扑选择面板 |
| 动态拓扑面板 | 文本定位 | "动态拓扑" | `role="tab"` | `.ip-selector .dynamic-topo-tab` | 动态拓扑选择面板 |
| 手动输入面板 | 文本定位 | "手动输入" | `role="tab"` | `.ip-selector .manual-input-tab` | 手动输入IP的面板 |
| IP输入框 | 文本定位 | "请输入IP" | `role="textbox"` | `.ip-selector input[placeholder*="IP"]` | 手动输入IP的文本框 |
| 确认选择按钮 | 文本定位 | "确认"、"确定" | `role="button"` | `.ip-selector .confirm-btn` | 确认IP选择 |
| 已选择节点数 | 文本定位 | "已选择"、"个节点" | - | `.select-text, .selected-count` | 显示已选择的节点数量 |

---

## 十三、通用元素

### 13.1 加载状态

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 加载指示器 | 文本定位 | - | `role="progressbar"` | `.page-loading-wrap, .bk-loading` | 页面加载中的指示器 |
| 加载完成 | 文本定位 | - | - | - | 等待加载指示器消失 |

### 13.2 错误提示

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 错误提示 | 文本定位 | "错误"、"失败" | `role="alert"` | `.bk-message-error, .error-message` | 错误提示消息 |
| 无数据提示 | 文本定位 | "检索无数据"、"无结果" | - | `.empty-status, .no-data` | 无检索结果提示 |

### 13.3 确认对话框

| 元素描述 | 定位方式 | 文本关键词 | 角色/属性 | CSS选择器（备选） | 说明 |
|---------|---------|-----------|----------|-----------------|------|
| 确认按钮 | 文本定位 | "确认"、"确定" | `role="button"` | `.bk-dialog .confirm-btn, button:contains("确认")` | 对话框确认按钮 |
| 取消按钮 | 文本定位 | "取消" | `role="button"` | `.bk-dialog .cancel-btn, button:contains("取消")` | 对话框取消按钮 |

---

## 十四、定位策略示例

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

## 十五、特殊场景定位

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

## 十六、测试用例示例

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

## 十七、注意事项

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
- **2025-01-XX**：补充下载功能相关元素映射
  - 新增下载按钮、下载下拉菜单（下载日志、下载历史）
  - 新增下载对话框相关元素（下载模式、下载范围、字段选择）
  - 新增下载历史对话框相关元素
  - 新增图表数据下载按钮
  - 新增聚类下载按钮
- **2025-01-XX**：补充其他核心功能元素映射
  - 新增实时日志功能相关元素（实时日志面板、暂停/继续、清空等）
  - 新增字段设置功能相关元素（字段设置面板、显示字段列表、字段宽度等）
  - 新增日志聚类功能相关元素（聚类开关、聚类模式、聚类配置等）
  - 新增图表分析功能相关元素（趋势图表、图表工具栏、图表操作等）
  - 新增IP选择器功能相关元素（IP选择器对话框、拓扑面板、手动输入等）
  - 新增表格操作相关元素（排序、分页、每页条数选择等）
- **2025-01-XX**：补充字段列表详细功能映射
  - 新增字段搜索和过滤功能（字段搜索输入框、字段类型过滤、是否可聚合过滤）
  - 新增字段列表分类展示（显示字段、索引字段、可选字段、内置字段）
  - 新增字段项详细操作（字段展开/收起、显示/隐藏、图表分析、字段统计数量）
  - 新增字段拖拽排序功能（拖拽点、可拖拽列表容器）
  - 新增字段类型图标和字段聚合图表
- 后续根据页面变化和测试需求持续更新

---

## 参考资源

- [page-automation-tester SKILL.md](../skill/page-automation-tester/SKILL.md)
- [测试用例格式说明](../skill/page-automation-tester/references/test_case_format.md)
- [页面辅助脚本](../skill/page-automation-tester/scripts/page_helper.js)

