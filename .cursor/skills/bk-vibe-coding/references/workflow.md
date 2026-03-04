# workflow.md

历史兼容文档。当前以根目录 `agent.md` 为主执行手册。

## 快速索引

- 标准流程与阶段产物：见 `agent.md`
- 价值观与决策优先级：见 `soul.md`
- 跨项目安装与复用：见 `INSTALL.md`
- 强制门禁与阻断规则：见 `agent.md` 的“0.1/0.2”章节

## TAPD MCP 统一调用模式

```text
1. 查询参数 schema
2. 按 schema 组装参数
3. 执行工具调用
```

## 常用工具

- `stories_get`
- `stories_create`
- `stories_update`
- `stories_fields_info_get`
- `comments_create`

## iWiki MCP（可选）

- 检索：`aiSearchDocument`
- 沉淀：`createDocument` / `saveDocument`
