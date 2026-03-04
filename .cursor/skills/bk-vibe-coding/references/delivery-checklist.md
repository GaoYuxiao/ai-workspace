# delivery-checklist.md

用于提交前后的固定检查，确保每次交付有证据。

## 执行前门禁（必须）

- 已判定任务类型（交付任务 / 非交付任务）
- 交付任务已创建或关联 TAPD story
- TAPD 状态已流转到开发态（按项目配置）
- TAPD MCP 不可用时停止执行，不进入实现/提交流程

## 提交前（必须）

- 使用 TAPD 短 story ID（`--story=<shortId>`）
- 不直推 `master/main`，只推需求分支
- 已运行测试/校验命令（按配置）

## 推送后（必须）

- 输出单据链接与 MR/PR 创建链接（必须同时展示）
- 回写 TAPD 评论（commit、分支、MR/PR、测试/发布结果）
- 更新 TAPD 状态到项目定义完成态（如 done/resolved）

## 最终输出模板

1. story：`<shortId>`
2. story_link：`<tapd_story_url>`
3. branch：`<feature-branch>`
4. commit：`<sha>`
5. review_link：`<mr_or_pr_url>`
6. test_result：`<pass_or_fail + evidence>`
7. publish_result：`<if_any>`
