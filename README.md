# AI Workspace

日常使用的 Cursor Agent Skills 集合。

## Skills

| Skill | 说明 |
|-------|------|
| [skill-creator](skills/skill-creator/) | 创建新的 Cursor Agent Skill，包含初始化、打包、校验等工具 |
| [prd-writer](skills/prd-writer/) | 撰写功能描述类产品需求文档 (PRD)，含标准模板与审核报告 |
| [design-to-doc](skills/design-to-doc/) | 将设计稿转换为产品交互文档，含蓝鲸设计规范与文档模板 |

## 使用方式

将 Skill 目录复制到 `~/.cursor/skills/` 下即可在 Cursor 中使用：

```bash
cp -r skills/skill-creator ~/.cursor/skills/
cp -r skills/prd-writer ~/.cursor/skills/
cp -r skills/design-to-doc ~/.cursor/skills/
```

## License

MIT
