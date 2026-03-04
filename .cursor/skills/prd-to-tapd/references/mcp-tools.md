# MCP 工具调用参考

本文档定义了 `prd-to-tapd` 技能使用的 MCP 工具及其参数格式。

---

## iWiki MCP 工具

### 创建目录

```yaml
工具: iWiki.createDocument
参数:
  spaceid: <iwiki.space_id>
  parentid: <iwiki.parent_doc_id>
  title: "<功能名称>"
  contenttype: "FOLDER"
返回:
  docid: <新创建的目录 ID>
```

### 创建 Markdown 文档

```yaml
工具: iWiki.createDocument
参数:
  spaceid: <space_id>
  parentid: <目录 ID>
  title: "<文档标题>"
  body: "<Markdown 内容>"
  contenttype: "MD"
返回:
  docid: <新创建的文档 ID>
```

### iWiki 链接格式

- 文档链接：`https://iwiki.woa.com/pages/viewpage.action?pageId={docid}`
- 锚点链接：`https://iwiki.woa.com/pages/viewpage.action?pageId={docid}#章节标题`

---

## TAPD MCP 工具

### 创建需求

```yaml
工具: stories_create
参数:
  workspace_id: <tapd.workspace_id>       # 必填，项目 ID
  name: "<需求标题>"                       # 必填，需求名称
  description: "<Markdown 描述>"          # 需求详细描述
  priority_label: "High|Middle|Low"       # 优先级
  iteration_id: "<迭代 ID>"               # 所属迭代
  parent_id: "<父需求 19 位 ID>"          # 子需求必填
  label: "<标签>"                         # 多个标签用 | 分隔
返回:
  id: <需求 19 位长 ID>
```

**关键注意事项**：
- `parent_id` 必须是 19 位长 ID 格式，如 `1010158081002227089`
- `stories_create` 返回的 ID 即为 19 位格式
- `description` 支持 Markdown 格式

### 创建评论

```yaml
工具: comments_create
参数:
  workspace_id: <workspace_id>
  entry_id: <父需求 ID>
  entry_type: "stories"
  description: "<Markdown 评论内容>"
```

---

## 优先级映射

| PRD 标签 | TAPD priority_label | 说明 |
|---------|---------------------|------|
| P0 | High | 核心必备，MVP 必须实现 |
| P1 | Middle | 重要功能，第二阶段 |
| P2 | Low | 增强功能，后续迭代 |

父需求的优先级 = 所有子模块中最高的优先级。

---

## 调用顺序

```
1. iWiki.createDocument (FOLDER)  → 创建需求目录
2. iWiki.createDocument (MD)      → 上传 PRD 文档
3. iWiki.createDocument (MD)      → 上传 HTML 原型（如有）
4. iWiki.createDocument (MD)      → 上传审核报告（如有）
5. stories_create                 → 创建父需求，获取 19 位 ID
6. stories_create × N             → 逐个创建子需求
7. comments_create                → 在父需求上添加评论
```
