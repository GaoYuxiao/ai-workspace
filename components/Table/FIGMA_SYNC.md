# Figma 代码同步说明

## 当前状态

表格组件代码已更新到项目中的 `components/Table/` 目录，包含以下更新：

### ✅ 已完成的更新

1. **四个状态列** - 已添加状态1、状态2、状态3、状态4列
2. **完整功能** - 复选框、开关、分页等功能
3. **代码组织** - 已整理到 `components/Table/` 目录

### 📁 文件位置

```
components/Table/
├── Table.tsx          # 主表格组件（包含四个状态列）
├── Table.css          # 样式文件
├── TableExample.tsx   # 使用示例
├── index.ts           # 导出文件
└── README.md          # 组件文档
```

## Figma Code Connect 设置

Code Connect 显示 "not publish" 的原因：**组件需要先发布到团队库才能使用 Code Connect**。

### ⚠️ 重要：发布组件到团队库

在使用 Code Connect 之前，必须先发布组件：

#### 步骤 1: 将表格转换为组件

1. 在 Figma 中选择表格节点（node-id: 3:2172）
2. 右键点击 → 选择 "Create Component" 或按 `⌘/Ctrl + Alt + K`
3. 将表格转换为组件

#### 步骤 2: 发布组件到团队库

1. 选择已创建的组件
2. 在右侧面板找到 "Publish" 或 "发布" 按钮
3. 点击 "Publish" 发布到团队库
4. 填写发布说明（可选）
5. 确认发布

#### 步骤 3: 设置 Code Connect

发布后，设置 Code Connect：

1. 在 Figma 中选择已发布的组件
2. 在右侧面板找到 "Code" 或 "Code Connect" 选项
3. 点击 "Connect to code"
4. 输入代码路径：`components/Table/Table.tsx`
5. 选择框架：React
6. 点击 "Save" 保存连接

### 方法 2: 使用 Figma Code Connect 配置文件

**注意**：配置文件方式也需要组件已发布。

在项目根目录创建 `.figma/code-connect.json` 文件：

```json
{
  "mappings": [
    {
      "figmaNodeId": "3:2172",
      "source": "components/Table/Table.tsx",
      "componentName": "Table",
      "framework": "React"
    }
  ]
}
```

### 方法 3: 使用 Figma 插件

1. 安装 Figma Code Connect 插件
2. 确保组件已发布到团队库
3. 在 Figma 中选择已发布的表格组件
4. 使用插件连接到代码库
5. 指定代码路径：`components/Table/Table.tsx`

## 常见问题

### Q: 为什么显示 "not publish"？

**A:** 因为组件还没有发布到团队库。Code Connect 只支持已发布的组件。

### Q: 如何检查组件是否已发布？

**A:** 
- 查看组件右侧面板，如果有 "Publish" 按钮，说明未发布
- 已发布的组件会显示版本号和发布信息
- 在团队库中可以搜索到该组件

### Q: 发布后还是显示 "not publish"？

**A:** 
1. 确保选择的是组件本身，而不是组件实例
2. 刷新 Figma 页面
3. 检查是否有发布权限
4. 确认组件已成功发布到团队库

### Q: 个人文件可以发布吗？

**A:** 可以，但需要：
- 将文件移动到团队项目，或
- 创建团队库并发布到该库

## 代码更新说明

### 主要变更

1. **新增三个状态列**
   - 原设计：1个状态列
   - 更新后：4个状态列（状态1、状态2、状态3、状态4）

2. **状态类型支持**
   - `success` - 成功（绿色）
   - `warning` - 警告（橙色）
   - `error` - 错误（红色）
   - `info` - 信息（蓝色）

3. **完整功能实现**
   - ✅ 复选框多选
   - ✅ 开关切换
   - ✅ 分页功能
   - ✅ 响应式设计

## ⚠️ Figma MCP 限制说明

**重要**：Figma MCP 工具主要用于从设计生成代码，**不支持直接更新 Figma 画布**。

### 为什么无法同步？

1. **Figma MCP 是只读工具** - 只能读取设计，不能修改设计
2. **节点不是组件** - 当前表格节点（3:2172）不是组件实例，无法建立 Code Connect
3. **需要手动更新** - 设计更新需要在 Figma 中手动完成

### 解决方案

#### 方案 1: 在 Figma 中手动更新设计（推荐）

1. 打开 Figma 设计文件
2. 选择现有的状态列（状态1）
3. 复制该列三次，创建状态2、状态3、状态4
4. 将新列放置在状态1之后
5. 更新列标题为"状态1"、"状态2"、"状态3"、"状态4"

#### 方案 2: 建立 Code Connect 连接（查看代码）

如果需要在 Figma 中查看代码实现：

1. **将表格转换为组件**
   - 在 Figma 中选择表格节点
   - 右键 → "Create Component" 或按 `⌘/Ctrl + Alt + K`

2. **发布组件到团队库**
   - 选择组件 → 点击 "Publish" 按钮
   - 发布到团队库

3. **建立 Code Connect**
   - 选择已发布的组件
   - 在右侧面板找到 "Code" → "Connect to code"
   - 输入代码路径：`components/Table/Table.tsx`
   - 选择框架：React

这样可以在 Figma 中查看代码，但**不会改变设计本身**。

## 设计建议

如果需要在 Figma 中更新设计以匹配代码：

1. 复制现有的状态列（状态1）
2. 创建三个新的状态列（状态2、状态3、状态4）
3. 放置在状态1列之后
4. 使用相同的状态徽标组件
5. 更新列标题为"状态1"、"状态2"、"状态3"、"状态4"

## 相关链接

- Figma 设计链接：https://www.figma.com/design/XY9zQrr9e2eca5OFX9tggE/Untitled?node-id=3-2172
- 代码位置：`components/Table/Table.tsx`
- 组件文档：`components/Table/README.md`

