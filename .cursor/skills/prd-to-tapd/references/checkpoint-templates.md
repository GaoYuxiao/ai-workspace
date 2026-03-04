# 检查点清单模板

本文档定义了 `prd-to-tapd` 技能执行过程中的检查点清单模板。

---

## iWiki 上传确认检查点

iWiki 文档上传完成后输出：

```markdown
## 检查点确认 - iWiki 文档归档

### 已上传文档
- [ ] 需求目录：https://iwiki.woa.com/pages/viewpage.action?pageId=<目录ID>
- [ ] 需求文档：https://iwiki.woa.com/pages/viewpage.action?pageId=<PRD文档ID>
- [ ] 交互原型：https://iwiki.woa.com/pages/viewpage.action?pageId=<原型文档ID>
- [ ] 审核报告：https://iwiki.woa.com/pages/viewpage.action?pageId=<报告文档ID>

### 即将创建的 TAPD 单据
📋 父需求：[需求名称]
   优先级：High | 迭代：[迭代名称]

   📌 子需求 1：[模块名] (P0 - High)
   📌 子需求 2：[模块名] (P1 - Middle)
   ...

目标项目：workspace_id = xxx

---
请回复「确认」继续创建 TAPD 单据，或提出需要修改的内容。
```

---

## 最终完成检查点

所有操作完成后输出：

```markdown
## 检查点确认 - 阶段四：需求拆分与 TAPD 单据创建

### 本阶段产出
- [ ] iWiki 文档目录：https://iwiki.woa.com/pages/viewpage.action?pageId={目录ID}
  - [ ] 需求文档：https://iwiki.woa.com/pages/viewpage.action?pageId={PRD文档ID}
  - [ ] 交互原型：https://iwiki.woa.com/pages/viewpage.action?pageId={原型文档ID}
  - [ ] 审核报告：https://iwiki.woa.com/pages/viewpage.action?pageId={报告文档ID}
- [ ] TAPD 父需求：https://tapd.woa.com/tapd_fe/{workspace_id}/story/detail/{story_id}
- [ ] TAPD 子需求（共 N 个）：
  | 序号 | 名称 | 优先级 | Story ID |
  |------|------|--------|----------|
  | 1 | 模块A | P0 (High) | xxx |
  | 2 | 模块B | P1 (Middle) | xxx |
- [ ] 父需求评论已添加 iWiki 链接

### 待确认事项
1. 父需求和子需求的层级关系是否正确？
2. 子需求的优先级是否与 PRD 模块优先级一致？
3. iWiki 文档是否可正常访问？

### 下一步操作
如需继续，可进入 **阶段五：研发闭环**，基于 TAPD 单据进行开发实现。

---
请回复「确认」完成本轮需求流程，或回复「继续」进入阶段五。
```

---

## 执行结果总结

执行完成后输出（可与检查点合并）：

```markdown
## TAPD 单据创建完成

### 父需求
- 标题：xxx
- ID：xxx
- 优先级：High
- 链接：https://tapd.woa.com/tapd_fe/{workspace_id}/story/detail/{story_id}

### 子需求清单
| 序号 | 名称 | 优先级 | ID |
|------|------|--------|-----|
| 1 | 模块A | P0 (High) | xxx |
| 2 | 模块B | P1 (Middle) | xxx |

### iWiki 文档归档
| 文档类型 | 链接 |
|---------|------|
| 📁 需求目录 | https://iwiki.woa.com/pages/viewpage.action?pageId=xxx |
| 📄 需求文档 | https://iwiki.woa.com/pages/viewpage.action?pageId=xxx |
| 🎨 交互原型 | https://iwiki.woa.com/pages/viewpage.action?pageId=xxx |
| ✅ 审核报告 | https://iwiki.woa.com/pages/viewpage.action?pageId=xxx |

### 本地文件
- PRD：docs/<功能名>_需求文档_v1.0.md
- 原型：prototypes/<功能名>.html
- 报告：docs/<功能名>_需求文档_v1.0_审核报告.md
```
