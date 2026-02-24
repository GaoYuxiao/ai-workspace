# 运行表格组件

## 方式 1: 直接在浏览器中打开（推荐）

```bash
# macOS
open components/Table/table-demo.html

# Linux
xdg-open components/Table/table-demo.html

# Windows
start components/Table/table-demo.html
```

或者直接双击 `table-demo.html` 文件。

## 方式 2: 使用本地服务器

如果需要更好的开发体验，可以使用本地服务器：

### Python 3

```bash
cd components/Table
python3 -m http.server 8000
```

然后在浏览器中访问：http://localhost:8000/table-demo.html

### Node.js (npx)

```bash
cd components/Table
npx serve
```

### PHP

```bash
cd components/Table
php -S localhost:8000
```

## 功能演示

打开后你将看到：

- ✅ **复选框多选** - 点击表头复选框全选，点击行复选框单选
- 🔘 **开关切换** - 点击开关可以切换每行的启用状态
- 🟢 **四个状态列** - 状态1、状态2、状态3、状态4
- 🎨 **四种状态类型** - 成功（绿）、警告（橙）、错误（红）、信息（蓝）
- 📄 **分页功能** - 底部显示分页控制
- ⚙️ **设置按钮** - 右上角设置图标

## 文件说明

- `table-demo.html` - 独立的 HTML 演示文件（使用 React CDN）
- `Table.tsx` - React 组件源码
- `Table.css` - 样式文件
- `TableExample.tsx` - React 组件使用示例

## 注意事项

- `table-demo.html` 使用 React CDN，需要网络连接
- 如果网络受限，可以下载 React 文件到本地
- 所有样式已内联在 HTML 中，可以直接运行

