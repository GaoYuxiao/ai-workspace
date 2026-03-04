---
name: prototype-capture
description: 通过 Chrome DevTools MCP 连接用户浏览器，对 Figma / HTML / Web 原型进行交互式截图采集，按规范命名并回填 PRD。当用户提到"截图采集"、"原型截图"、"设计稿截图"、"补充页面原型"时触发。
---

# 原型截图采集技能

通过 Chrome DevTools MCP 连接用户浏览器，操作原型页面（点击、输入、展开弹窗等），逐功能模块截图并回填到 PRD 文档。

## 适用场景

所有原型类型统一使用 Chrome DevTools MCP 方案：Figma Make 代码原型、传统 Figma 设计稿、HTML 原型、已部署 Web 应用。

核心优势：交互能力（点击/输入/滚动）+ 继承用户登录态 + iframe 内元素精准截图。

## 前置条件

1. 用户用 `--remote-debugging-port=9222` 启动 Chrome
2. 用户在 Chrome 中打开原型页面并完成登录
3. 工作区或全局已配置 `chrome-devtools-mcp`

> 详细设置步骤见 `./references/chrome-devtools-setup.md`

## 执行流程

```
1. 输入分析
   - 读取 PRD，提取所有截图引用路径 → 生成截图清单
   - 确认截图保存目录（默认 PRD 同级 screenshots/）

2. 连接浏览器
   - list_pages → select_page 选中目标页面
   - Figma Make：点击 "Open full-screen view" → 切换到全屏标签页
   - take_snapshot 获取元素树

3. 交互截图（循环）
   - 执行交互操作触发目标状态（click / fill / type_text / press_key）
   - take_snapshot 确认 UI 已更新（uid 会刷新）
   - take_screenshot(uid=<容器uid>, filePath=<路径>) 保存截图
   - 恢复状态（Escape / 点击取消）

4. 回填 PRD
   - 将截图路径写入 PRD 对应的"页面原型"章节
   - 每张截图附 > 说明：描述内容
   - 补充新增截图、更新修订记录
```

> 交互模式详解和 Figma Make iframe 结构见 `./references/interaction-patterns.md`

## 命名规范

格式：`{序号}-{功能模块}-{区域/状态}.png`

| 部分 | 规则 | 示例 |
|------|------|------|
| 序号 | 两位数字，按 PRD 模块顺序 | `01` `02` `03` |
| 功能模块 | 小写英文，连字符分隔 | `filter-mode` `log-pool` `condition-group` |
| 区域/状态 | 描述截图内容 | `selector` `editor` `management` `settings` `overview` |

## 参考文档

| 文档 | 说明 | 路径 |
|------|------|------|
| Chrome DevTools 设置 | 启动命令、MCP 配置、常见问题 | `./references/chrome-devtools-setup.md` |
| 交互模式参考 | iframe 结构、操作示例表、注意事项 | `./references/interaction-patterns.md` |
