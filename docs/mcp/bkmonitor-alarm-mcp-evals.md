# BKMonitor-Alarm MCP 评估文档 (Evals)

## 1. 概述

### 1.1 评估目标
本文档用于评估 `bkmonitor-alarm` MCP 服务的功能完整性、准确性和可用性。

### 1.2 MCP 工具清单

| 工具名称 | HTTP Method | 功能描述 | 依赖关系 |
|---------|-------------|---------|---------|
| `list_alerts` | POST | 列举告警列表，支持过滤、时间范围、分页、排序 | 无，工作流入口 |
| `get_alert_info` | GET | 获取指定告警详细信息 | 依赖 `list_alerts` 返回的 `id` |

### 1.3 关键注意事项
- **业务ID（bk_biz_id）**：所有工具都需要提供，这是 MCP 鉴权的必需参数
- **告警ID获取**：`get_alert_info` 的 `id` 参数必须从 `list_alerts` 的返回结果中获取
- **时间戳动态计算**：查询告警时的时间戳必须动态计算当前时间，不要使用历史固定值
- **参数转换**：`list_alerts` 接口会自动将 `bk_biz_id` 转换为 `bk_biz_ids` 数组格式

---

## 2. 测试用例汇总表

### 2.1 list_alerts 工具测试用例

| 测试ID | 测试项名称 | 测试场景 | 输入内容 | 预期输出 |
|--------|-----------|---------|---------|---------|
| LA-001 | 基础告警列表查询 | 查询指定业务最近1小时的告警列表 | `{"bk_biz_id": "7", "start_time": 动态计算, "end_time": 动态计算}` | 正确返回告警列表，时间戳动态计算 |
| LA-002 | 按状态筛选-未恢复告警 | 查询所有未恢复状态的告警 | `{"bk_biz_id": "7", "status": ["ABNORMAL"]}` | 返回 status 为 ABNORMAL 的告警 |
| LA-003 | 按状态筛选-已恢复告警 | 查询已恢复状态的告警 | `{"bk_biz_id": "7", "status": ["RECOVERED"]}` | 返回 status 为 RECOVERED 的告警 |
| LA-004 | 按状态筛选-已关闭告警 | 查询已关闭状态的告警 | `{"bk_biz_id": "7", "status": ["CLOSED"]}` | 返回 status 为 CLOSED 的告警 |
| LA-005 | 多状态筛选 | 同时查询多个状态的告警 | `{"bk_biz_id": "7", "status": ["ABNORMAL", "RECOVERED"]}` | 返回多种状态的告警 |
| LA-006 | 全文搜索-关键字查询 | 使用关键字搜索告警 | `{"bk_biz_id": "7", "query_string": "CPU"}` | 返回包含"CPU"的告警 |
| LA-007 | 全文搜索-中文关键字 | 使用中文关键字搜索 | `{"bk_biz_id": "7", "query_string": "内存"}` | 支持中文搜索 |
| LA-008 | conditions-包含匹配 | 使用include进行模糊匹配 | `{"conditions": [{"key": "alert_name", "value": ["CPU高"], "method": "include"}]}` | 返回告警名称包含"CPU高"的告警 |
| LA-009 | conditions-精确匹配 | 使用eq进行精确匹配 | `{"conditions": [{"key": "severity", "value": ["1"], "method": "eq"}]}` | 返回 severity=1 的告警 |
| LA-010 | conditions-不等于 | 使用neq排除某些告警 | `{"conditions": [{"key": "severity", "value": ["1"], "method": "neq"}]}` | 返回 severity≠1 的告警 |
| LA-011 | conditions-不包含 | 使用exclude排除告警 | `{"conditions": [{"key": "alert_name", "value": ["测试"], "method": "exclude"}]}` | 告警名称不含"测试" |
| LA-012 | conditions-AND逻辑 | 使用AND连接多个条件 | `{"conditions": [{"key": "alert_name", "value": ["CPU"], "method": "include", "condition": "and"}, {"key": "severity", "value": ["1"], "method": "eq"}]}` | 同时满足两个条件 |
| LA-013 | conditions-OR逻辑 | 使用OR连接多个条件 | `{"conditions": [..., "condition": "or", ...]}` | 满足任一条件 |
| LA-014 | conditions-多值匹配 | 单个条件匹配多个值 | `{"conditions": [{"key": "alert_name", "value": ["CPU", "内存"], "method": "include"}]}` | 包含任一关键字 |
| LA-015 | 按负责人筛选 | 查询特定负责人的告警 | `{"bk_biz_id": "7", "username": "admin"}` | 返回 admin 负责的告警 |
| LA-016 | 按策略名筛选 | 按策略名过滤 | `{"conditions": [{"key": "strategy_name", "value": ["主机监控"], "method": "include"}]}` | 返回相关策略告警 |
| LA-017 | 按IP地址筛选 | 按IP过滤告警 | `{"conditions": [{"key": "ip", "value": ["10.0.0.1"], "method": "eq"}]}` | 返回指定IP告警 |
| LA-018 | 时间范围-最近24小时 | 查询最近24小时的告警 | `start_time = end_time - 86400` | 时间范围正确 |
| LA-019 | 时间范围-最近7天 | 查询最近7天的告警 | `start_time = end_time - 604800` | 时间范围正确 |
| LA-020 | 排序-按时间倒序 | 获取最新的告警 | `{"ordering": ["-create_time"]}` | 最新告警排在前面 |
| LA-021 | 排序-按时间升序 | 获取最早的告警 | `{"ordering": ["create_time"]}` | 最早告警排在前面 |
| LA-022 | 排序-按级别排序 | 按严重程度排序 | `{"ordering": ["severity"]}` | 按级别排序 |
| LA-023 | 分页查询-第一页 | 获取第一页告警 | `{"page": 1, "page_size": 10}` | 返回最多10条 |
| LA-024 | 分页查询-翻页 | 获取第二页告警 | `{"page": 2, "page_size": 20}` | 返回第21-40条 |
| LA-025 | 统计信息-概览统计 | 获取告警概览统计 | `{"show_overview": true}` | 返回各状态数量 |
| LA-026 | 统计信息-聚合统计 | 获取告警趋势统计 | `{"show_aggs": true}` | 返回趋势分布 |
| LA-027 | 复合查询-多条件组合 | 状态+时间+排序组合 | 多参数组合 | 各条件同时生效 |
| LA-028 | 复合查询-全条件 | 完整条件组合查询 | 所有参数组合 | 满足所有条件 |
| LA-029 | 参数转换验证 | bk_biz_id到bk_biz_ids转换 | MCP: `bk_biz_id: "7"` | 后台: `bk_biz_ids: ["7"]` |
| LA-030 | 时间戳动态计算验证 | 验证时间戳必须动态计算 | Python: `int(time.time())` | 不使用固定历史时间戳 |

### 2.2 get_alert_info 工具测试用例

| 测试ID | 测试项名称 | 测试场景 | 输入内容 | 预期输出 |
|--------|-----------|---------|---------|---------|
| GA-001 | 获取告警详情-基础查询 | 根据告警ID获取详细信息 | `{"bk_biz_id": "7", "id": "123456"}` | 返回完整告警详情 |
| GA-002 | 获取告警详情-完整字段 | 验证返回字段完整性 | 调用 get_alert_info | 包含 id, alert_name, status, severity, description, create_time, extra_info, actions 等 |
| GA-003 | 获取告警详情-策略信息 | 查看关联策略配置 | 调用 get_alert_info | 返回 extra_info.strategy |
| GA-004 | 获取告警详情-处理记录 | 查看处理历史 | 调用 get_alert_info | 返回 actions 数组 |
| GA-005 | 获取告警详情-收敛信息 | 查看收敛情况 | 调用 get_alert_info | 返回 alert_collect |
| GA-006 | 获取告警详情-事件信息 | 查看事件详情 | 调用 get_alert_info | 返回 event 字段 |

### 2.3 工作流测试用例

| 测试ID | 测试项名称 | 测试场景 | 输入内容 | 预期输出 |
|--------|-----------|---------|---------|---------|
| WF-001 | 完整工作流-列表到详情 | 先查列表再查详情 | "查看最近告警，然后查看第一个详情" | 正确遵循 list_alerts → get_alert_info 流程 |
| WF-002 | 故障排查工作流 | 使用告警进行故障排查 | "服务器有问题，查查告警" | 优先关注未恢复、高级别告警 |
| WF-003 | 告警趋势分析 | 分析告警趋势 | "分析最近一周告警趋势" | 返回统计数据，提供分析结论 |

### 2.4 异常处理测试用例

| 测试ID | 测试项名称 | 测试场景 | 输入内容 | 预期输出 |
|--------|-----------|---------|---------|---------|
| ERR-001 | 缺少必需参数-业务ID | 未提供业务ID | "查看最近的告警" | 主动询问业务ID |
| ERR-002 | 无效的告警ID | 使用不存在的告警ID | `{"id": "999999999"}` | 友好提示告警不存在 |
| ERR-003 | 时间范围过大 | 查询时间超出限制 | "查询过去一年的告警" | 建议分批查询 |
| ERR-004 | 直接使用get_alert_info | 未先获取告警ID | "获取告警详情" | 先调用 list_alerts |
| ERR-005 | 空结果处理 | 查询条件无结果 | 严格条件查询 | 友好提示无结果 |
| ERR-006 | 参数格式错误-status | status非数组 | `{"status": "ABNORMAL"}` | 应为 `["ABNORMAL"]` |
| ERR-007 | 参数格式错误-ordering | ordering非数组 | `{"ordering": "-create_time"}` | 应为 `["-create_time"]` |
| ERR-008 | conditions结构错误 | 缺少必需字段 | `{"conditions": [{"key": "x"}]}` | 必须有 key 和 value |

### 2.5 性能与展示测试用例

| 测试ID | 测试项名称 | 测试场景 | 输入内容 | 预期输出 |
|--------|-----------|---------|---------|---------|
| PERF-001 | 响应时间-少量数据 | 查询少量告警 | page_size=10 | 响应时间 < 3秒 |
| PERF-002 | 响应时间-大量数据 | 查询大量告警 | page_size=100 | 响应时间 < 10秒 |
| DISP-001 | 结果可读性-告警列表 | 列表展示格式 | 告警列表 | 格式清晰，关键信息突出 |
| DISP-002 | 结果可读性-告警详情 | 详情展示格式 | 告警详情 | 结构化展示，重要字段优先 |

---

## 3. 参数详细说明

### 3.1 list_alerts 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|-----|------|------|
| bk_biz_id | string | ✅ | 业务ID（MCP鉴权必需） | "7" |
| status | array[string] | ❌ | 告警状态：ABNORMAL/RECOVERED/CLOSED | ["ABNORMAL"] |
| query_string | string | ❌ | 全文搜索 | "CPU" |
| start_time | number | ❌ | 开始时间戳（秒），必须动态计算 | int(time.time())-3600 |
| end_time | number | ❌ | 结束时间戳（秒），必须动态计算 | int(time.time()) |
| username | string | ❌ | 按负责人过滤 | "admin" |
| ordering | array[string] | ❌ | 排序字段，-前缀降序 | ["-create_time"] |
| page | number | ❌ | 页码，从1开始 | 1 |
| page_size | number | ❌ | 每页条数（1-5000） | 10 |
| conditions | array[object] | ❌ | 高级过滤条件 | 见下表 |
| show_overview | boolean | ❌ | 返回概览统计 | true |
| show_aggs | boolean | ❌ | 返回聚合统计 | true |

### 3.2 conditions 参数结构

| 字段 | 类型 | 必填 | 说明 | 可选值 |
|-----|------|-----|------|--------|
| key | string | ✅ | 字段名 | alert_name, severity, strategy_name, ip, status |
| value | array[string] | ✅ | 匹配值数组 | - |
| method | string | ❌ | 匹配方法 | eq, neq, include, exclude, gt, gte, lt, lte |
| condition | string | ❌ | 逻辑运算符 | and, or, "" |

### 3.3 get_alert_info 参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|-----|------|------|
| bk_biz_id | string | ✅ | 业务ID | "7" |
| id | string | ✅ | 告警ID（从list_alerts获取） | "123456" |

---

## 4. 告警状态和级别参考

### 4.1 告警状态
| 状态值 | 含义 |
|-------|------|
| ABNORMAL | 未恢复 |
| RECOVERED | 已恢复 |
| CLOSED | 已关闭 |

### 4.2 告警级别
| 级别值 | 含义 |
|-------|------|
| 1 | 致命 |
| 2 | 预警 |
| 3 | 提醒 |

---

## 5. 时间戳计算参考

```python
import time

# 当前时间戳
end_time = int(time.time())

# 1小时前
start_time_1h = end_time - 3600

# 24小时前
start_time_24h = end_time - 86400

# 7天前
start_time_7d = end_time - 604800
```

```javascript
// 当前时间戳
const end_time = Math.floor(Date.now() / 1000);

// 1小时前
const start_time_1h = end_time - 3600;
```

---

## 6. 评估记录模板

| 测试ID | 执行时间 | 测试人 | 结果 | 备注 |
|-------|---------|-------|------|------|
| LA-001 | | | ⬜ 通过 / ⬜ 失败 | |
| LA-002 | | | ⬜ 通过 / ⬜ 失败 | |
| ... | | | | |

---

**文档版本**: v2.0  
**创建日期**: 2026-01-22  
**参考文档**: 告警 MCP 工具介绍 / Alert MCP Tools Documentation  
**适用MCP**: bkmonitor-alarm
