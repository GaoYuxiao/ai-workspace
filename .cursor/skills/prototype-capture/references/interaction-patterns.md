# 交互模式参考

## Figma Make 原型结构

Figma Make 原型渲染在 iframe 中，截图时定位 iframe 可获得干净的原型画面（不含 Figma 编辑器 UI）。

```
RootWebArea (Figma Make 编辑器)
  └── Iframe "Preview"          ← 原型的 iframe 容器
        └── RootWebArea          ← 原型根节点
              ├── banner         ← 导航栏
              ├── button/input   ← 交互元素（有 uid）
              └── ...
```

关键操作：

- **截图**：`take_screenshot(uid=<iframe_uid>)` — 只截 iframe 内容
- **交互**：iframe 内元素在 `take_snapshot` 中有 uid，可直接 `click` / `fill`
- **限制**：`evaluate_script` 无法访问 iframe 内容（跨域），用 uid 操作代替

## 全屏预览

Figma Make 页面通常有 "Open full-screen view" 按钮，点击后在新标签页打开全屏预览，操作更便捷。流程：

1. `take_snapshot` → 找到全屏按钮 uid
2. `click(uid)` → 打开新标签页
3. `list_pages` → `select_page` 切到新标签页
4. 后续在全屏预览中操作

## 交互操作对照表

| 目标状态 | 操作序列 |
|---------|---------|
| 默认页面 | 直接截图 |
| 切换 Tab / 模式 | `click(tab_uid)` → 截图 |
| 展开下拉选择器 | `click(selector_uid)` → 截图 → `press_key("Escape")` |
| 打开弹窗 / 对话框 | `click(button_uid)` → 截图 → `click(cancel_uid)` |
| 输入触发浮层 | `click(input_uid)` → `type_text("@")` → 截图 |
| 查询结果 | `click(confirm_uid)` → 等待 → 截图 |
| 悬停 Tooltip | `hover(element_uid)` → 截图 |

## 注意事项

1. **每次交互后刷新 uid**：`take_snapshot` 返回的 uid 在 DOM 变化后可能失效，交互后必须重新获取
2. **截图层级是功能区域**：截图目标是语义功能区域容器，不是单个控件。不确定时主动向用户确认
3. **恢复状态**：截完弹窗/下拉后，用 `press_key("Escape")` 或点击取消按钮关闭，再进行下一个截图
4. **iframe 内滚动**：无法用 JS 直接滚动 iframe，通过点击视口外元素间接实现
