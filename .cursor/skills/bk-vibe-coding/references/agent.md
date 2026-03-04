# agent.md

这是 `bk-vibe-coding` 的执行手册。目标是把研发流程变成可复用的“流水线动作”，而不是一次性对话。

## 强制执行声明（新增）

`bk-vibe-coding` 默认是强制流程，不是建议流程。

- 只要任务产生仓库改动（代码、文档、配置），必须创建或关联 TAPD story
- 未进入 TAPD 开发态前，禁止实现与提交
- 未完成 TAPD 评论与状态闭环前，禁止宣布交付完成
- TAPD MCP 不可用时直接阻断，不提供 no-TAPD 降级路径

## 配置优先（新增）

执行前优先读取项目根目录的 `bk-vibe-config.json`（可由 `references/config.template.json` 复制而来）。

如果该文件存在，以下信息必须以配置为准：

- TAPD 项目（`workspace_id` / `workspace_name`）
- 默认迭代（`default_iteration_id`）
- 单据状态流转（`workflow.story_status_flow`）
- 提交模板、测试命令、发布命令
- 分支策略（是否允许直推主分支）
- story ID 规则（短 ID / 长 ID）

如果配置文件不存在，再使用通用默认流程。

## 0) 准备上下文（必须）

开始前收集最小输入：

- TAPD `workspace_id`
- 需求描述（目标、边界、验收标准）
- 代码仓库与分支策略
- 默认测试命令、发布命令
- 是否需要 iWiki 沉淀文档（可选）

如果任一关键输入缺失，先提问补齐，不直接进入实现。

### 0.3 指定迭代（新增）

若用户明确提供迭代（ID、名称或 TAPD 迭代链接），必须优先使用该迭代，不得回退默认迭代。

推荐优先级：

1. 用户显式指定的 `iteration_id`
2. 用户提供的迭代链接中解析出的 `iteration_id`
3. `bk-vibe-config.json.tapd.default_iteration_id`

迭代链接解析规则（示例）：

```text
https://tapd.woa.com/tapd_fe/10158081/iteration/card/1010158081002227089?q=...
workspace_id = 10158081
iteration_id = 1010158081002227089
```

创建/更新 story 时，若目标迭代明确，需写入 `iteration_id`，并在最终输出中展示迭代信息与迭代链接。

### 0.1 强制门禁（必须先通过）

执行前按顺序做门禁检查：

1. 任务分类：是否有仓库改动（有改动则视为交付任务）
2. TAPD MCP 可用性：是否可用且能读取工具 schema
3. TAPD 上下文：是否有 `workspace_id`，是否能创建/关联 story
4. 状态门禁：是否已流转到开发态（todo/doing 或项目定义开发态）

任一检查失败时，默认阻断，不得进入实现与提交阶段。

### 0.2 TAPD 不可用处理（强制阻断）

如果 TAPD MCP 不可用、无法读取 schema 或无法创建/更新 story，立即停止执行并返回阻断信息。

阻断信息至少包含：

- `blocked_reason`：不可执行的客观原因
- `required_action`：恢复执行前必须完成的动作（如补齐 MCP 配置、workspace_id）
- `resume_condition`：满足哪些条件后才能继续

## 1) 需求评估

执行动作：

1. 复述需求目标与非目标
2. 识别影响面（模块、接口、配置、文档）
3. 拆分交付项（可实现、可测试、可回滚）

阶段产物：

- 一段“需求评估摘要”
- 一组明确验收标准（可验证）

如果需求含糊或缺验收标准，先按 `planning.md` 输出最小计划，再进入实现。

## 2) TAPD 单据创建/关联

优先复用已有 story；没有则创建新 story。

建议顺序：

1. 查重：`stories_get`
2. 创建（必要时）：`stories_create`
3. 根据规则写入 `iteration_id`（若有指定迭代）
4. 记录 story ID、标题、当前状态

阻断规则：

- 如果 story 未创建/未关联，禁止进入“实现（第 5 步）”

## 3) 状态流转（度量必经）

默认执行两次流转：

```text
backlog/planning -> todo(developing) -> doing(status_7)
```

注意：不同项目状态枚举可能不同，首次接入先查 `stories_fields_info_get`。

如果存在 `bk-vibe-config.json`，按配置的 `workflow.story_status_flow` 进行完整流转，不要使用内置默认值。

阻断规则：

- 如果状态未进入开发态，禁止进入“实现（第 5 步）”

## 4) 分发处理人

在 story 上设置或确认处理人（owner/handler），保证责任清晰：

- 单人开发：直接绑定当前执行人
- 多人协作：按子任务拆分处理人并在评论中说明分工

如果没有明确处理人，暂停后续步骤并向用户确认。

## 5) 实现（Vibe Coding 主阶段）

执行策略：

- 小步提交、每步可验证
- 先读后改，避免“猜测式修复”
- 代码改动与文档更新同步进行

最低要求：

- 代码可运行
- 变更有对应测试或验证动作
- 文档与行为一致

## 6) commit & push

强制规范：

- commit message 里的 `--story=` 必须使用 **TAPD 短 ID**（示例：`131770392`），不要使用长 ID
- 任何情况下都不允许直接推送 `master/main`，必须先创建需求分支
- push 到需求分支后，必须生成并返回 MR 创建链接
- 未完成 story 绑定与状态门禁时，禁止 commit

推荐格式：

```text
feat|fix|refactor|docs|chore: <主题> --story=<storyId>
```

如果 `bk-vibe-config.json.delivery.commit_template` 存在，按配置模板执行。

推荐流程：

1. 基于需求创建分支（示例：`feat/<topic>-<storyId>`）
2. `git add .`
3. 运行项目预检（如 pre-commit）
4. 生成 commit（含短 story ID）
5. 推送到需求分支（示例：`git push origin <branch>`）
6. 生成代码评审链接并返回给用户：
   - GitLab：`.../merge_requests/new?merge_request[source_branch]=<branch>`
   - GitHub：`.../compare/<base_branch>...<branch>?expand=1`
7. 发起 MR/PR，等待合并到主分支

如果配置中存在 `delivery.branch_policy` 或 `delivery.story_id_format`，优先按配置校验，不满足则停止执行并提示修正。
如果配置中存在 `delivery.mr.base_branch`，生成链接时使用该目标分支。
如果配置中存在 `delivery.mr.platform`，按配置的平台优先生成链接（`gitlab` / `github` / `auto`）。

提交与推送完成后，必须执行 `delivery-checklist.md` 并输出其中的最终模板。

## 7) publish & test

按项目实际情况执行：

- 本地测试（单测/集成测试/构建）
- CI 检查确认
- 如需发版，先 dry-run 再正式 publish

如果配置中存在 `delivery.test_command` 与 `delivery.publish_command`，优先按配置命令执行。

如果测试或发布失败：

- 在输出中给出失败点与修复建议
- TAPD 评论同步失败信息，不要假装完成

## 8) TAPD 闭环

至少完成两件事：

1. 评论回写（commit、分支、MR/PR 链接、测试/发布结果）
2. 状态更新到项目定义的完成态（如 resolved/done）

展示规范（强制）：

- 最终回复里必须同时给出 `story_link` 与 `review_link`
- 禁止只给评审链接不展示单据链接

阻断规则：

- 评论未回写或状态未闭环时，输出状态只能是“进行中”，不能标记“完成”

## TAPD MCP 调用约定

每次调用 TAPD 工具遵循固定模式：

1. 查询参数 schema（例如 `lookup_tool_param_schema`）
2. 基于 schema 组装参数
3. 执行工具调用（例如 `proxy_execute_tool`）

常用工具：

- `stories_get`
- `stories_create`
- `stories_update`
- `stories_fields_info_get`
- `comments_create`

## iWiki MCP（可选增强）

适用场景：

- 开发前检索历史方案：`aiSearchDocument`
- 开发后沉淀复盘/方案：`createDocument` / `saveDocument`

iWiki 不可用时，不阻塞主流程。
