---
name: prd-to-tapd
description: 根据PRD需求文档自动创建TAPD单据。支持两层结构：先创建父级需求单据，再按功能模块拆分创建子需求单据，同时将文档归档到iWiki。当用户提到"根据PRD创建TAPD"、"需求文档转单据"、"把需求拆成TAPD story"时触发。
---

# PRD → TAPD 单据

将 PRD 需求文档自动拆解为 TAPD 两层需求单据（父需求 + 子需求），同时将相关文档上传到 iWiki 归档。

## 参考文档

- [描述模板](./references/description-templates.md) - 父需求、子需求、评论的内容模板
- [MCP 工具参考](./references/mcp-tools.md) - iWiki 和 TAPD 的 MCP 调用格式
- [检查点模板](./references/checkpoint-templates.md) - 各阶段检查点清单

---

## 前置条件

1. `bk-vibe-config.json` 包含 `tapd.workspace_id` 和 `iwiki.space_id`
2. TAPD MCP 和 iWiki MCP 服务可用
3. 已有 PRD 文档：`docs/<功能名>_需求文档_v1.0.md`

---

## 执行流程

### 第一步：读取配置与文件

1. 读取 `bk-vibe-config.json` 获取配置
2. 检查文件是否存在：
   - PRD 文档：`docs/<功能名>_需求文档_v1.0.md`（必须）
   - HTML 原型：`prototypes/<功能名>.html`（可选）
   - 审核报告：`docs/<功能名>_需求文档_v1.0_审核报告.md`（可选）

### 第二步：解析 PRD 结构

从 PRD 文档中提取：

| 信息类型 | 提取来源 |
|---------|---------|
| 需求名称 | 文档标题 |
| 需求背景 | 「1.1 背景说明」 |
| 目标用户 | 「1.2 目标用户」 |
| 核心价值 | 「1.3 核心价值」 |
| 功能模块 | 「三、功能详细设计」中每个 `### 3.x` 章节 |

### 第三步：上传 iWiki 文档

创建目录结构并上传文档：

```
[iwiki.parent_doc_id]
└── <功能名称>/           ← FOLDER
    ├── 需求文档          ← PRD Markdown
    ├── 交互原型          ← HTML 代码块
    └── 审核报告          ← 审核报告 Markdown
```

> 详细 MCP 调用格式见 [MCP 工具参考](./references/mcp-tools.md#iwiki-mcp-工具)

### 第四步：创建 TAPD 父需求

调用 `stories_create` 创建父需求：
- **关键**：记录返回的 **19 位长 ID**，用于创建子需求
- 描述内容使用 [父需求描述模板](./references/description-templates.md#父需求描述模板)

### 第五步：批量创建子需求

对 PRD「三、功能详细设计」中每个 `### 3.x` 章节：
- 必须指定 `parent_id` 为父需求的 19 位长 ID
- 优先级映射：P0 → High / P1 → Middle / P2 → Low
- 描述内容使用 [子需求描述模板](./references/description-templates.md#子需求描述模板)

### 第六步：父需求添加评论

调用 `comments_create` 在父需求上添加评论：
- 包含 iWiki 文档链接
- 包含子需求清单
- 内容使用 [评论模板](./references/description-templates.md#评论模板)

### 第七步：输出检查点清单

输出完整的检查点清单，等待用户确认。

> 清单格式见 [检查点模板](./references/checkpoint-templates.md#最终完成检查点)

---

## 优先级映射

| PRD 标签 | TAPD priority_label |
|---------|---------------------|
| P0 | High |
| P1 | Middle |
| P2 | Low |

父需求优先级 = 所有子模块中最高的优先级。

---

## 异常处理

| 场景 | 处理方式 |
|------|---------|
| 配置缺失 | 提示用户在 `bk-vibe-config.json` 中补充 |
| TAPD MCP 不可用 | 阻断执行，提示检查 MCP 配置 |
| iWiki MCP 不可用 | 降级：跳过 iWiki 上传，使用本地路径引用 |
| 原型/报告不存在 | 跳过对应上传，继续执行 |
| 父需求创建失败 | 阻断执行，输出错误信息 |
| 子需求创建失败 | 记录失败项，继续创建其余子需求 |

---

## 配置示例

```json
{
  "tapd": {
    "workspace_id": "10158081",
    "default_iteration_id": "1010158081002227089"
  },
  "iwiki": {
    "space_id": "<your_space_id>",
    "parent_doc_id": "<your_parent_doc_id>"
  }
}
```

---

## 协作关系

```
product-design → [prd-to-tapd] → bk-vibe-coding
   PRD + 原型       TAPD 单据 + iWiki      研发闭环
```
