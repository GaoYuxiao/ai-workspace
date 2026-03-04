# Changelog

## v1.3.0 `2026-02-28`

- ✨ 新增“指定迭代”规则：支持通过 `iteration_id` 或 TAPD 迭代链接解析并绑定迭代
- ✨ 强制最终输出同时展示 `story_link` 与 `review_link`
- 📝 更新 `SKILL.md`、`agent.md`、`delivery-checklist.md`

## v1.2.0 `2026-02-28`

- 🔒 移除 no-TAPD 应急降级路径，统一改为 TAPD 不可用即强制阻断
- 🔒 删除输出模板中的降级字段，避免误导为“可跳过 TAPD”
- 📝 更新 `SKILL.md`、`agent.md`、`delivery-checklist.md`、`planning.md`、`workflow.md`

## v1.1.0 `2026-02-28`

- ✨ 强化为默认强制流程：交付任务必须创建/关联 TAPD story 并完成状态流转
- ✨ 新增执行前门禁与阻断规则：未通过 TAPD 检查不得进入实现/提交
- ✨ 新增应急降级规范：仅允许用户明确授权，并要求 `no_tapd_reason` 与补录计划
- 📝 更新 `delivery-checklist.md` 与 `planning.md`，补齐可追溯输出字段

## v1.0.0 `2026-02-28`

- 🎉 首次发布 `bk-vibe-coding` 基础流程文档
