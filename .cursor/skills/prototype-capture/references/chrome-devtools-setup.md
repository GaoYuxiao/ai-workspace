# Chrome DevTools MCP 设置指南

## 启动 Chrome

必须带 `--remote-debugging-port=9222` 启动：

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Windows
chrome.exe --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222
```

## MCP 配置

在全局 `~/.cursor/mcp.json` 或工作区 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Agent 检查项

连接前按顺序验证：

1. 调用 `list_pages` — 如果失败，提示用户检查 Chrome 是否以调试端口启动
2. 确认返回的页面列表中包含目标原型页面
3. 如未找到，提示用户手动在 Chrome 中打开原型 URL 并完成登录

## 常见问题

| 问题 | 解决方式 |
|------|---------|
| `list_pages` 失败 | Chrome 未开启调试端口，需重新启动 |
| Figma 跳转到登录页 | 用户需在 Chrome 中手动登录 Figma |
| 元素 uid 操作报错 | 交互后 DOM 变化导致 uid 失效，重新 `take_snapshot` |
| 弹窗关不掉 | `take_snapshot` 找关闭/取消按钮 uid 后 `click` |
| 截图包含外部 UI | 对 iframe 元素 `take_screenshot(uid=<iframe_uid>)` |
| 页面太长截不全 | 分段截图：点击内部元素滚动后再截 |
