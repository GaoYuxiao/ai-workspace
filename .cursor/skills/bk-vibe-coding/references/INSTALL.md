# INSTALL.md

把 `bk-vibe-coding` 接入任意项目，按下面 5 步即可。

## 1) 配置 TAPD MCP（必须）

在对应客户端的 `mcp.json` 中添加 TAPD MCP 配置（示例）：

```json
{
  "tapd_mcp_http": {
    "url": "https://mcp-oa.tapd.woa.com/mcp/",
    "timeout": 20000,
    "headers": {
      "X-Tapd-Access-Token": "<YOUR_TAPD_TOKEN>"
    },
    "transportType": "streamable-http"
  }
}
```

说明：

- 将 `<YOUR_TAPD_TOKEN>` 替换为你自己的 Token
- Token 申请地址：`https://tapd.woa.com/platform/myhome?not_direct=1&from=mcp#tab=tab-mytoken`
- 不要把真实 Token 提交到仓库，建议通过本地用户级配置管理

## 2) 安装技能目录

将 `bk-vibe-coding` 放入目标项目：

- Cursor: `.cursor/skills/bk-vibe-coding/`
- Claude Code: `.claude/skills/bk-vibe-coding/`

## 3) 配置项目变量与流程模板（推荐）

在项目根目录新增 `bk-vibe-config.json`，可直接复制：

- `references/config.template.json`

当前项目（蓝鲸监控）建议配置如下：

```json
{
  "project_name": "bk-monitor",
  "tapd": {
    "workspace_id": "10158081",
    "workspace_name": "蓝鲸监控",
    "default_iteration_id": "1010158081002227089",
    "default_iteration_url": "https://tapd.woa.com/tapd_fe/10158081/iteration/card/1010158081002227089?q=882ae02758277407fb432c25d3b59a57"
  },
  "workflow": {
    "story_status_flow": ["backlog", "todo", "doing", "for test", "done"]
  },
  "delivery": {
    "commit_template": "feat|fix|refactor|docs|chore: <subject> --story=<id>",
    "story_id_format": "short",
    "branch_policy": {
      "protected_branches": ["master", "main"],
      "allow_direct_push": false,
      "require_feature_branch": true,
      "branch_naming": "feat|fix|chore/<topic>-<storyId>"
    },
    "mr": {
      "required": true,
      "platform": "auto",
      "base_branch": "master"
    },
    "test_command": "npm test",
    "publish_command": "npm publish"
  }
}
```

关键约束（建议强制）：

- `story_id_format` 使用 `short`：commit 中 `--story=` 只写短 ID（例如 `131770392`）
- `allow_direct_push` 必须为 `false`：禁止直推 `master/main`
- `require_feature_branch` 为 `true`：按需求创建分支并走 MR
- `mr.required` 为 `true`：push 后必须输出 MR 创建链接
- `mr.platform`：支持 `gitlab`、`github`、`auto`（默认自动识别）

然后在项目 `AGENTS.md` 或团队约定文档中定义：

- `TAPD_WORKSPACE_ID`
- `DEFAULT_BRANCH`（如 `main`）
- `TEST_COMMAND`（如 `npm test` / `pytest`）
- `PUBLISH_COMMAND`（如 `npm publish` / `helm upgrade`）
- `COMMIT_TEMPLATE`（默认：`type: <subject> --story=<id>`）

建议模板：

```markdown
## BK Vibe Coding Config
- TAPD_WORKSPACE_ID: <your_workspace_id>
- DEFAULT_BRANCH: main
- TEST_COMMAND: npm test
- PUBLISH_COMMAND: npm publish
- COMMIT_TEMPLATE: feat|fix|refactor|docs|chore: <subject> --story=<id>
```

## 4) 在 AGENTS.md 声明启用

建议在项目 `AGENTS.md` 增加一句：

```markdown
本项目启用 bk-vibe-coding，流程配置以项目根目录 bk-vibe-config.json 为准。
```

## 5) 验证开箱可用

让 Agent 执行以下任一请求进行冒烟测试：

- “帮我基于这个需求创建 TAPD story 并流转到 doing”
- “按 bk-vibe-coding 流程推进这个需求到 commit 阶段”

通过标准：

1. Agent 先做需求评估，不直接写代码
2. 能创建/关联 story 并按配置执行状态流转（说明 TAPD MCP + 流程配置已生效）
3. 输出里包含 story ID、处理人、测试结果、闭环动作

## iWiki（可选）

如果团队有 iWiki 文档，可额外启用：

- 开发前：检索历史文档
- 开发后：沉淀方案、发布记录、复盘

即便 iWiki 不可用，主流程也可正常工作。
