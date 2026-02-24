# 表格组件使用说明

## 概述

这是一个基于 Figma 设计生成的 React 表格组件，包含完整的交互功能和四个状态列。

## 功能特性

### 1. 基础功能
- ✅ 复选框多选功能
- ✅ 开关切换功能
- ✅ 分页功能
- ✅ 响应式设计

### 2. 状态列
组件包含**四个状态列**（状态1、状态2、状态3、状态4），每个状态列支持四种状态类型：

| 状态类型 | 颜色 | 说明 |
|---------|------|------|
| `success` | 绿色 (#2CAF5E) | 成功状态 |
| `warning` | 橙色 (#FF9C01) | 警告状态 |
| `error` | 红色 (#EA3636) | 错误状态 |
| `info` | 蓝色 (#3A84FF) | 信息状态 |

## 文件结构

```
components/Table/
├── Table.tsx          # 主表格组件
├── Table.css          # 样式文件
├── TableExample.tsx   # 使用示例
├── index.ts           # 导出文件
└── README.md          # 说明文档
```

## 使用方法

### 基础使用

```tsx
import React from 'react';
import Table from './components/Table';

function App() {
  return <Table />;
}
```

### 自定义数据

修改 `components/Table/Table.tsx` 中的 `rows` 状态来使用你自己的数据：

```tsx
const [rows, setRows] = useState<TableRow[]>([
  {
    id: '1',
    title: '你的标题',
    enabled: true,
    description: '描述信息',
    status1: 'success',  // success | warning | error | info
    status2: 'warning',
    status3: 'error',
    status4: 'info',
  },
  // ... 更多数据
]);
```

## 组件结构

### TableRow 接口

```typescript
interface TableRow {
  id: string;              // 唯一标识
  title: string;            // 标题
  enabled: boolean;        // 开关状态
  description: string;     // 描述
  status1: StatusType;     // 状态1
  status2: StatusType;     // 状态2
  status3: StatusType;     // 状态3
  status4: StatusType;      // 状态4
}
```

### 状态类型

```typescript
type StatusType = 'success' | 'warning' | 'error' | 'info';
```

## 样式定制

所有样式定义在 `components/Table/Table.css` 中，你可以根据需要修改：

- **颜色变量**：在 CSS 中直接修改颜色值
- **间距**：调整 padding 和 margin
- **字体**：修改 font-family 和 font-size

## 交互功能

### 1. 复选框选择
- 点击表头的复选框可以全选/取消全选
- 点击每行的复选框可以单独选择

### 2. 开关切换
- 点击开关可以切换每行的启用/禁用状态

### 3. 分页
- 支持切换页码
- 支持调整每页显示数量（10/20/50）

## 浏览器兼容性

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)

## 注意事项

1. 确保已安装 React 和相关依赖
2. 需要引入 CSS 文件才能正常显示样式
3. 状态标签会根据状态类型自动显示对应的中文（成功/警告/错误/信息）

## 后续优化建议

1. 添加排序功能
2. 添加筛选功能
3. 添加列宽调整功能
4. 添加数据导出功能
5. 添加空状态提示

