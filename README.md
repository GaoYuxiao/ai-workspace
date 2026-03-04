# TAPD Product 产品工具集

面向蓝鲸产品团队的 AI 技能工具集，覆盖从需求输入到 TAPD 单据闭环的完整产品工作流。

## 工作流概览

```
需求沟通与确认 → HTML 原型生成 → PRD 撰写（含截图采集） → 需求拆分 → 研发闭环
```

> 完整的任务流定义、阶段约束和串行规则见 `AGENTS.md`。

## 技能清单

| 技能 | 说明 | 触发指令示例 |
|------|------|-------------|
| `product-design` | 需求沟通输出大纲 → 生成 HTML 原型 → 撰写 PRD + 审核报告 | "帮我梳理一下这个需求"、"根据这张截图生成原型"、"根据原型写一份 PRD" |
| `prototype-capture` | PRD 撰写时自动调用，对原型交互式截图并回填文档 | "帮我补充 PRD 的原型截图" |
| `prd-to-tapd` | 将 PRD 按父需求 + 子需求两层结构创建 TAPD 单据 | "根据这个 PRD 创建 TAPD 单据" |
| `bk-vibe-coding` | TAPD 单据驱动研发闭环：开发 → 提测 → 发布 | "帮我推进这个需求" |

## 快速开始

### 1. 配置 TAPD Token

编辑 `.cursor/mcp.json`，将 `<YOUR_TAPD_TOKEN>` 替换为真实 Token。

Token 申请：https://tapd.woa.com/platform/myhome?not_direct=1&from=mcp#tab=tab-mytoken

### 2. 配置项目信息

编辑 `bk-vibe-config.json`：

- `tapd.workspace_id`：TAPD 项目 ID
- `tapd.default_iteration_id`：默认迭代 ID

### 3. 用 Cursor 打开本目录

```bash
cursor TAPD_product/
```

## 复用到其他项目

```bash
# 安装 bk-vibe-coding
npx @tencent/bkai install bk-vibe-coding --client cursor

# 手动复制其他技能
cp -r .cursor/skills/product-design <目标项目>/.cursor/skills/
cp -r .cursor/skills/prototype-capture <目标项目>/.cursor/skills/
cp -r .cursor/skills/prd-to-tapd <目标项目>/.cursor/skills/
```

## License

MIT
