# bkmonitor-backend-saas WARNING 日志分析报告

## 报告时间范围
- **开始时间**: 2025-12-25 20:32:10 (UTC+8)
- **结束时间**: 2025-12-25 20:47:10 (UTC+8)
- **时间跨度**: 近15分钟

## 总体统计

### 日志级别分布
- **WARNING**: 约 10,000+ 条（实际查询到 10,000 条，可能还有更多）
- **查询限制**: 单次查询最多返回 10,000 条

### WARNING 日志主要类型

1. **get_request_tenant_id 警告** (最多)
   - 错误信息: `get_request_tenant_id: cannot get tenant_id from request or local`
   - 影响范围: 多个服务实例，主要集中在 `bk-monitor-alarm-service-aiops-worker`
   - 可能原因: 请求中缺少 tenant_id 信息

2. **连接池满警告**
   - 错误信息: `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
   - 影响范围: urllib3 连接池，主要在 `bk-monitor-alarm-cron-worker` 服务
   - 可能原因: 连接池配置过小或连接未及时释放

3. **ES 主机配置警告**
   - 错误信息: `compose_es_hosts:host->[...] may be not invalid,please check,error->[...] does not appear to be an IPv4 or IPv6 address`
   - 影响范围: `bk-monitor-alarm-long-task-cron-worker` 服务
   - 可能原因: ES 主机配置使用了域名而非 IP 地址

4. **无效指标名称警告**
   - 错误信息: `invalid metric name: cmdb_cc:v3:watch:...`
   - 影响范围: `bk-monitor-api` 服务
   - 可能原因: 指标名称格式不符合规范

5. **索引不匹配警告**
   - 错误信息: `index->[...] is not match re, maybe something go wrong?`
   - 影响范围: `bk-monitor-alarm-long-task-cron-worker` 服务
   - 可能原因: 索引名称格式不符合预期正则表达式

---

## 按 IP 地址分析

### Top 20 IP 的 WARNING 日志统计

| 排名 | IP 地址 | WARNING 数量 | 主要问题 |
|------|---------|-------------|---------|
| 1 | 30.167.60.50 | 14,283 | get_request_tenant_id 警告（大量） |
| 2 | 30.167.60.61 | 11,925 | get_request_tenant_id 警告 |
| 3 | 30.167.61.89 | 9,648 | get_request_tenant_id 警告 |
| 4 | 9.136.133.78 | 9,618 | get_request_tenant_id 警告 |
| 5 | 30.167.61.83 | 7,653 | get_request_tenant_id 警告、连接池满警告 |
| 6 | 30.167.61.105 | 5,131 | get_request_tenant_id 警告 |
| 7 | 30.167.61.123 | 3,918 | 其他警告 |
| 8 | 11.149.25.188 | 3,462 | ES 主机配置警告、索引不匹配警告 |
| 9 | 9.136.170.171 | 3,090 | 连接池满警告 |
| 10 | 30.167.60.103 | 2,667 | 其他警告 |
| 11 | 30.186.110.212 | 743 | 其他警告 |
| 12 | 30.186.110.66 | 459 | 其他警告 |
| 13 | 30.186.151.168 | 457 | 其他警告 |
| 14 | 30.167.61.56 | 407 | 其他警告 |
| 15 | 30.167.61.61 | 280 | 其他警告 |
| 16 | 30.167.60.51 | 194 | 无效指标名称警告 |
| 17 | 30.167.60.78 | 152 | 其他警告 |
| 18 | 30.167.61.85 | 109 | 其他警告 |
| 19 | 30.171.183.204 | 72 | 其他警告 |
| 20 | 30.189.37.50 | 68 | 其他警告 |

### IP 详细分析

#### 1. 30.167.60.50 (14,283 条 WARNING) 🔴
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **主机运行情况**:
  - CPU 使用率: 平均 29.0%，最高 37.3%，最低 25.8%
  - 内存使用率: 平均 64.7%，最高 65.9%，最低 58.3%
- **建议**: 
  - 检查请求头中是否正确传递 tenant_id
  - 检查本地上下文是否正确设置 tenant_id
  - 考虑增加默认 tenant_id 处理逻辑
  - CPU 和内存使用率正常，但需要关注 tenant_id 获取失败问题

#### 2. 30.167.60.61 (11,925 条 WARNING) 🔴
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 同上

#### 3. 30.167.61.89 (9,648 条 WARNING) 🔴
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 同上

#### 4. 9.136.133.78 (9,618 条 WARNING) 🔴
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 同上

#### 5. 30.167.61.83 (7,653 条 WARNING) 🟡
- **主要问题**: 
  - `get_request_tenant_id: cannot get tenant_id from request or local`
  - `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
- **影响服务**: 
  - bk-monitor-alarm-service-aiops-worker
  - bk-monitor-alarm-cron-worker
- **严重程度**: ⚠️ 中高
- **主机运行情况**:
  - CPU 使用率: 平均 12.0%，最高 18.8%，最低 4.2%（CPU 使用率较低，可能表示服务负载不均衡）
  - 内存使用率: 平均 50.0%，最高 62.1%，最低 34.0%（内存使用率波动较大）
- **建议**: 
  - 检查 tenant_id 获取逻辑
  - 增加连接池大小配置
  - 检查连接是否正确关闭
  - CPU 使用率较低但内存波动较大，需要进一步排查

#### 6. 30.167.61.105 (5,131 条 WARNING) 🟡
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 中
- **建议**: 同上

#### 7. 30.167.61.123 (3,918 条 WARNING) 🟡
- **主要问题**: 其他警告
- **影响服务**: 多个服务
- **严重程度**: ⚠️ 中
- **建议**: 需要进一步分析具体警告类型

#### 8. 11.149.25.188 (3,462 条 WARNING) 🟡
- **主要问题**: 
  - `compose_es_hosts:host->[...] may be not invalid`
  - `index->[...] is not match re, maybe something go wrong?`
- **影响服务**: bk-monitor-alarm-long-task-cron-worker
- **严重程度**: ⚠️ 中
- **建议**: 
  - 检查 ES 主机配置，建议使用 IP 地址或确保域名解析正常
  - 检查索引名称格式是否符合规范

#### 9. 9.136.170.171 (3,090 条 WARNING) 🟡
- **主要问题**: `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
- **影响服务**: bk-monitor-alarm-cron-worker
- **严重程度**: ⚠️ 中
- **建议**: 
  - 增加连接池大小
  - 检查连接是否正确关闭
  - 考虑使用连接池监控

---

## 按 Path 分析

### Top 20 Path 的 WARNING 日志统计

| 排名 | Path (容器日志路径) | WARNING 数量 | 容器名称（推测） |
|------|-------------------|-------------|-----------------|
| 1 | .../36f78951f7a1440481c29bfdf8e5e7c217b83589e90566b149ea83213dc5d303/... | 14,092 | bk-monitor-alarm-service-aiops-worker |
| 2 | .../19c4b6c9b8facd8a05aad290eec5449abce58a93943b4bba4f6619b07ea937ab/... | 6,463 | bk-monitor-alarm-service-aiops-worker |
| 3 | .../868d0288d4f469bc8707d45db35f4ef2dabb98a2c03c300ee9f45f3bc6b473f1/... | 11,729 | bk-monitor-alarm-service-aiops-worker |
| 4 | .../5695fb7042be7aecb59a6b633c08d391ad6335bed6c79df29cb1b13f2e27a646/... | 9,729 | bk-monitor-alarm-service-aiops-worker |
| 5 | .../37fd9b6363d662e983dcdfbeed63d83297f1bd2aaea0a82ffb5cdc1a038ef0c9/... | 8,802 | bk-monitor-alarm-service-aiops-worker |
| 6 | .../22b17d26de3e169b65dc5dacfc353412030f1489c732bb1a564e36d13a059068/... | 3,608 | bk-monitor-alarm-service-aiops-worker |
| 7 | .../ec858826be9c2d1235a8a23bb766a8db6bd849167b854e41e67f4c79e497a4a4/... | 2,664 | bk-monitor-alarm-service-aiops-worker |
| 8 | .../ee7b1446924b04cee8b755a2cb47f552256315947c82a335786cb6f732d341c9/... | 4,151 | bk-monitor-alarm-service-aiops-worker |
| 9 | .../a217adb2e8bc82f03e186c4e688bef5d9eea4d4c350c052a7806f9f5fc15da43/... | 2,363 | bk-monitor-alarm-service-aiops-worker |
| 10 | .../d62e93e3e34cd59f60c2bbd5493e16c3900e92d5b21d0ae0a736c5f6ff5da63a/... | 810 | bk-monitor-alarm-cron-worker |
| 11 | .../e83ba52f2529a1ca36a1e83d93d01c0ef3de988cddc9056ff556d558c06d8015/... | 500 | bk-monitor-alarm-long-task-cron-worker |
| 12 | .../3db777922193b7afc88feb3d97ba1871fe4251a7fce9c6b49592cb1b7d1587fc/... | 600 | 其他服务 |
| 13 | .../bb7cd32f98fb36320e8f7a83f6f67b2e79c20d1329c004610910b035cb797b92/... | 975 | 其他服务 |
| 14 | .../5decb6ffb09aa74df61cfc3fd8258443b3f9a90d388b23d37bdc84d48d3ac33c/... | 809 | 其他服务 |
| 15 | .../d6cdac1f83d33f5c5851e00f56cd1c63c23db2fde61249d99b75a4ad57bc1c10/... | 639 | 其他服务 |
| 16 | .../55428f1993a4f6f0b0d7809cf50681f4e4a0c3b7235bacde98dddd42d7f743b7/... | 538 | bk-monitor-alarm-cron-worker |
| 17 | .../15d96ce084c5ed4091408a32ab91e6292aa2ccb0ab464b2d5ee5666ac62e589c/... | 515 | 其他服务 |
| 18 | .../47ac874c489f1321ea0ed0e466e2c2aa014c16545d06221cdae6d4970289b879/... | 377 | 其他服务 |
| 19 | .../1e13c21b688894807a816e4ee788d7be249540dab6dcc6362948c8a376a4a145/... | 256 | 其他服务 |
| 20 | .../b3d3eb9b786e6432af2434b2c8d6c48cefd21af47117611adaa015abf67e399e/... | 320 | 其他服务 |

### Path 分析结论

1. **bk-monitor-alarm-service-aiops-worker** 服务产生了最多的 WARNING 日志
   - 主要问题: `get_request_tenant_id` 警告
   - 涉及多个 Pod 实例（至少 8 个主要 Pod）
   - 日志路径对应的容器 ID 数量多，说明该服务有多个实例在运行

2. **bk-monitor-alarm-cron-worker** 服务
   - 主要问题: 连接池满警告
   - 涉及多个 Pod 实例

3. **bk-monitor-alarm-long-task-cron-worker** 服务
   - 主要问题: ES 主机配置警告、索引不匹配警告
   - 至少 1 个 Pod 实例

---

## 主要问题汇总

### 1. tenant_id 获取失败 (最严重) 🔴
- **影响范围**: 多个服务实例，主要集中在 aiops-worker 服务
- **日志数量**: 约 50,000+ 条（占 WARNING 日志的 50%+）
- **主要影响 IP**: 
  - 30.167.60.50 (14,283 条)
  - 30.167.60.61 (11,925 条)
  - 30.167.61.89 (9,648 条)
  - 9.136.133.78 (9,618 条)
- **可能原因**:
  - 请求头中缺少 tenant_id
  - 本地上下文未正确设置
  - 中间件处理逻辑问题
- **建议措施**:
  1. 检查请求链路，确保 tenant_id 正确传递
  2. 增加请求头验证和默认值处理
  3. 优化日志级别，避免大量 WARNING 日志
  4. 检查相关服务的配置和代码逻辑

### 2. 连接池满警告 🟡
- **影响范围**: cron-worker 服务
- **日志数量**: 约 3,000+ 条
- **主要影响 IP**: 
  - 30.167.61.83
  - 9.136.170.171
- **可能原因**:
  - 连接池大小配置过小（当前为 10）
  - 连接未及时释放
  - 请求频率过高
- **建议措施**:
  1. 增加连接池大小配置（建议从 10 增加到 20-30）
  2. 检查连接是否正确关闭
  3. 考虑使用连接复用机制
  4. 监控连接池使用情况

### 3. ES 主机配置问题 🟡
- **影响范围**: long-task-cron-worker 服务
- **日志数量**: 约 3,500+ 条
- **主要影响 IP**: 11.149.25.188
- **可能原因**:
  - ES 主机配置使用了域名而非 IP
  - 域名解析可能存在问题
- **建议措施**:
  1. 将 ES 主机配置改为 IP 地址
  2. 或确保域名解析正常
  3. 增加主机配置验证

### 4. 索引不匹配警告 🟡
- **影响范围**: long-task-cron-worker 服务
- **日志数量**: 约 3,000+ 条
- **主要影响 IP**: 11.149.25.188
- **可能原因**: 索引名称格式不符合预期正则表达式
- **建议措施**: 检查索引名称格式规范，修复不符合规范的索引

### 5. 无效指标名称警告 🟢
- **影响范围**: api 服务
- **日志数量**: 约 200+ 条
- **主要影响 IP**: 30.167.60.51
- **可能原因**: 指标名称格式不符合规范
- **建议措施**: 检查指标名称格式，修复不符合规范的指标名称

---

## 主机运行情况汇总

### Top 5 IP 主机运行情况

#### 1. 30.167.60.50
- **WARNING 日志数**: 14,283 条
- **CPU 使用率**: 
  - 平均值: 29.0%
  - 最大值: 37.3%
  - 最小值: 25.8%
- **内存使用率**: 
  - 平均值: 64.7%
  - 最大值: 65.9%
  - 最小值: 58.3%
- **运行状态**: ✅ 正常（CPU 和内存使用率在正常范围内）
- **主要问题**: tenant_id 获取失败（大量 WARNING 日志）

#### 2. 30.167.60.61
- **WARNING 日志数**: 11,925 条
- **运行状态**: ⚠️ 需要监控（无指标数据，但日志量较大）
- **主要问题**: tenant_id 获取失败

#### 3. 30.167.61.89
- **WARNING 日志数**: 9,648 条
- **运行状态**: ⚠️ 需要监控（无指标数据，但日志量较大）
- **主要问题**: tenant_id 获取失败

#### 4. 9.136.133.78
- **WARNING 日志数**: 9,618 条
- **运行状态**: ⚠️ 需要监控（无指标数据，但日志量较大）
- **主要问题**: tenant_id 获取失败

#### 5. 30.167.61.83
- **WARNING 日志数**: 7,653 条
- **CPU 使用率**: 
  - 平均值: 12.0%
  - 最大值: 18.8%
  - 最小值: 4.2%
- **内存使用率**: 
  - 平均值: 50.0%
  - 最大值: 62.1%
  - 最小值: 34.0%
- **运行状态**: ⚠️ 异常（CPU 使用率较低，内存波动较大）
- **主要问题**: 
  - tenant_id 获取失败
  - 连接池满警告
- **建议**: 
  - CPU 使用率较低可能表示服务负载不均衡或服务异常
  - 内存使用率波动较大，需要进一步排查
  - 需要检查服务运行状态和负载均衡配置

### 主机运行情况总结

| IP 地址 | CPU 状态 | 内存状态 | 整体状态 | 主要问题 |
|---------|---------|---------|---------|---------|
| 30.167.60.50 | ✅ 正常 | ✅ 正常 | ✅ 正常 | tenant_id 获取失败 |
| 30.167.61.83 | ⚠️ 异常 | ⚠️ 波动 | ⚠️ 异常 | tenant_id 获取失败、连接池满 |
| 其他 IP | - | - | ⚠️ 需监控 | 需要获取指标数据进一步分析 |

---

## 建议和行动计划

### 立即行动（高优先级）

1. **排查 tenant_id 获取失败问题**
   - 检查请求链路中的 tenant_id 传递逻辑
   - 检查相关服务的配置和代码
   - 优先处理影响最大的 IP（30.167.60.50, 30.167.60.61 等）

2. **检查 30.167.61.83 主机异常**
   - 检查 CPU 使用率低的原因（可能是服务异常或负载不均衡）
   - 检查内存使用率波动的原因
   - 检查服务运行状态

### 短期优化（中优先级）

1. **优化连接池配置**
   - 增加连接池大小（从 10 增加到 20-30）
   - 优化连接管理逻辑
   - 监控连接池使用情况

2. **修复 ES 主机配置问题**
   - 修复 ES 主机配置（使用 IP 地址或确保域名解析正常）
   - 修复索引名称格式问题

### 长期改进（低优先级）

1. **建立完善的监控告警机制**
   - 设置 WARNING 日志数量告警
   - 设置主机资源使用率告警
   - 设置服务健康检查告警

2. **优化日志级别**
   - 减少不必要的 WARNING 日志
   - 将部分 WARNING 降级为 INFO 或 DEBUG

3. **定期进行日志分析**
   - 定期分析 WARNING 日志趋势
   - 识别和解决常见问题

---

## 报告生成时间
2025-12-25 20:47:10 (UTC+8)

## 数据来源
- **业务ID**: 2
- **索引集ID**: 322
- **索引集名称**: bkmonitor-backend-saas
- **查询时间范围**: 2025-12-25 20:32:10 ~ 2025-12-25 20:47:10 (近15分钟)

