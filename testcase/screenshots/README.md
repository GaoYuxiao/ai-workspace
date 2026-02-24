# 测试截图目录说明

## 目录结构

```
screenshots/
├── README.md
├── test_case_1_highlight.png          # 测试用例1：高亮功能测试截图
├── test_case_1_results.png            # 测试用例1：查询结果展示截图
├── test_case_2_tooltip.png            # 测试用例2：分词工具提示菜单截图
├── test_case_2_added.png              # 测试用例2：分词添加到检索条件后截图
├── test_case_3_sort_button.png        # 测试用例3：排序按钮位置截图
├── test_case_3_sorted.png             # 测试用例3：排序后的日志列表截图
├── test_case_4_context_panel.png      # 测试用例4：上下文面板打开截图
├── test_case_4_context_list.png      # 测试用例4：上下文日志列表截图
├── test_case_5_new_context.png        # 测试用例5：新版上下文功能特性截图
├── test_case_6_download_button.png   # 测试用例6：下载按钮定位截图
├── test_case_7_graph_analysis.png     # 测试用例7：图表分析页面截图
└── test_case_7_results.png            # 测试用例7：字段分析结果截图
```

## 截图命名规范

- 格式：`test_case_{用例编号}_{功能描述}.png`
- 示例：
  - `test_case_1_highlight.png` - 测试用例1的高亮功能截图
  - `test_case_2_tooltip.png` - 测试用例2的工具提示截图

## 如何添加截图

1. **使用浏览器截图工具**：
   - Chrome DevTools: 使用 `mcp_chrome-devtools_take_screenshot` 工具
   - 浏览器扩展: 使用截图扩展工具
   - 系统截图: 使用系统自带的截图工具

2. **截图要求**：
   - 格式：PNG（推荐）或 JPG
   - 分辨率：建议宽度至少 1200px
   - 文件大小：建议每个截图不超过 2MB

3. **截图内容建议**：
   - 包含关键操作界面
   - 显示测试结果
   - 突出显示测试要点
   - 保持界面清晰可见

4. **保存截图**：
   - 将截图保存到 `screenshots/` 目录
   - 使用规范的文件名
   - 确保文件名与HTML中的路径一致

## 在HTML中查看截图

1. 打开 `test_report_visualization.html` 文件
2. 确保截图文件已放置在 `screenshots/` 目录中
3. 截图会自动显示在对应的测试用例部分

## 注意事项

- 如果截图文件不存在，HTML页面会显示占位符
- 截图路径是相对于HTML文件的相对路径
- 建议使用PNG格式以获得更好的质量
- 截图应该清晰展示测试的关键步骤和结果

