---
name: bk-vibe-coding
version: 1.3.0
description: 蓝鲸团队 Vibe Coding 开箱即用流程技能。用于把“需求评估 -> TAPD 单据创建 -> 状态流转 -> 分发处理人 -> 实现 -> commit/push -> publish/test -> 单据闭环”标准化执行到任意项目。只要用户提到需求开发、TAPD 单据驱动、从需求到上线、AI 研发流程、要落地规范或跨项目复用，都应优先触发本技能，即使用户没有明确说“用这个 skill”。
---

# BK Vibe Coding

用最少指令，让 Agent 按统一、可追溯、可复制的方式完成研发闭环。

## 开始使用

安装与上手请直接参考 `references/INSTALL.md`。

## 先读这几份文档

1. `references/soul.md`：价值观与决策优先级
2. `references/agent.md`：标准执行流（主操作手册）
3. `references/INSTALL.md`：跨项目安装与复用
4. `references/config.template.json`：项目配置模板（TAPD 项目、状态流转、默认迭代）
5. `references/planning.md`：需求澄清与实施计划模板
6. `references/delivery-checklist.md`：交付前后检查清单（证据化输出）

如果用户只说“开始做需求”或“帮我推进 TAPD”，默认直接走 `references/agent.md` 流程。

## 强制模式（默认开启）

- 只要任务涉及**代码/文档变更、提测、发布、流程推进**，必须走 TAPD 主流程
- 未完成 TAPD 单据创建/关联前，禁止进入实现、commit、push、publish
- 未完成 TAPD 评论回写与状态闭环前，禁止声明“已完成”
- 仅允许两类免单据场景：纯咨询问答、纯环境检查（无仓库改动）

## 路由规则（强制）

- 需求不清晰或缺验收标准：先用 `references/planning.md`
- 已进入开发/提测/发布：按 `references/agent.md` 执行主流程
- 准备提交或收尾：强制执行 `references/delivery-checklist.md`

## 执行原则（简版）

- 先澄清再动手，不做猜测式实现
- 每次改动都要绑定 TAPD story
- 每个阶段都有产出：单据、状态、代码、测试、评论
- iWiki 是可选增强，不阻塞主链路
- 优先读取项目 `bk-vibe-config.json`，流程配置优先于默认值
- 支持指定迭代：可通过 `default_iteration_id` 或 TAPD 迭代链接解析目标迭代
- commit 只使用 TAPD 短 story ID（如 `131770392`）
- 任何情况下禁止直推 `master/main`，必须走需求分支 + MR
- 代码评审链接需兼容 GitLab MR 与 GitHub PR

## 标准主流程

```text
需求评估 -> 单据创建/关联 -> 状态流转 -> 分发处理人 -> 实现 -> commit & push -> publish & test -> 单据闭环
```

详细步骤、失败兜底和 MCP 调用模式见 `references/agent.md`。

## MCP 使用约束

- TAPD MCP：用于单据创建、状态管理、评论回写、进度可追溯（必选）
- iWiki MCP：用于需求参考、方案沉淀、复盘文档（可选）
- 调 TAPD 工具时，先读取参数 schema，再执行工具调用
- 若 TAPD MCP 不可用，直接阻断执行，先补齐 TAPD 能力后再继续

## 输出要求

每次执行结束前，至少输出：

1. 需求与验收摘要
2. TAPD story 信息（ID/标题/状态/处理人/迭代）
3. 代码与文档改动点
4. commit / push / publish / test 结果
5. 单据链接 + MR/PR 创建链接（必须同时展示）
6. TAPD 评论与最终状态
