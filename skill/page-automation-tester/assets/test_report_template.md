# 页面自动化测试报告

**测试执行时间**: {execution_time}  
**测试环境**: {environment}  
**浏览器**: Chrome (via DevTools)  
**报告生成时间**: {report_time}

---

## 测试概览

| 指标 | 数值 |
|------|------|
| 总测试用例数 | {total_tests} |
| 通过 | {passed_tests} ✅ |
| 失败 | {failed_tests} ❌ |
| 跳过 | {skipped_tests} ⏭️ |
| 通过率 | {pass_rate}% |
| 总执行时间 | {total_duration} |

---

## 测试用例详情

{test_case_details}

### 测试用例模板

```markdown
### {test_case_name}

**状态**: {status} {icon}  
**描述**: {description}  
**执行时间**: {duration}  
**URL**: {url}

#### 执行步骤

| 步骤 | 操作 | 目标 | 状态 | 耗时 |
|------|------|------|------|------|
| 1 | navigate | {url} | ✅ | 1.2s |
| 2 | snapshot | - | ✅ | 0.5s |
| 3 | fill | username_input | ✅ | 0.3s |
| 4 | click | login_button | ✅ | 0.2s |
| 5 | wait_for | "欢迎" | ✅ | 2.1s |

#### 验证结果

| 验证项 | 类型 | 期望值 | 实际值 | 状态 |
|--------|------|--------|--------|------|
| URL跳转 | url_contains | /dashboard | /dashboard | ✅ 通过 |
| 用户菜单存在 | element_exists | 用户菜单 | 找到 | ✅ 通过 |
| 欢迎消息 | text_contains | testuser | "欢迎 testuser" | ✅ 通过 |

#### 截图

{如果有截图，显示截图路径或嵌入图片}

{screenshot_paths}

---

#### 错误信息（如果失败）

{error_message}

{error_stack_trace}
```

---

## 问题汇总

### 失败用例分析

{failed_cases_summary}

### 常见问题

{common_issues}

---

## 总结与建议

### 测试总结

{test_summary}

### 修复建议

{fix_suggestions}

### 后续行动

{next_actions}

---

## 附录

### 测试环境信息

- Chrome版本: {chrome_version}
- 页面尺寸: {page_size}
- 网络条件: {network_conditions}

### 执行日志

{execution_logs}

---

**报告生成工具**: Page Automation Tester Skill  
**版本**: 1.0


