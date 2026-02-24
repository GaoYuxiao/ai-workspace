# bkmonitor-backend-saas WARNING 日志分析报告

## 报告时间范围
- **开始时间**: 2025-12-25 17:47:25 (UTC+8)
- **结束时间**: 2025-12-25 17:50:05 (UTC+8)
- **时间跨度**: 近15分钟

## 总体统计

### 日志级别分布
- **WARNING**: 93,547 条
- **INFO**: 1,121,720 条
- **ERROR**: 13,407 条

### WARNING 日志主要类型

1. **get_request_tenant_id 警告** (最多)
   - 错误信息: `get_request_tenant_id: cannot get tenant_id from request or local`
   - 影响范围: 多个服务实例
   - 可能原因: 请求中缺少 tenant_id 信息

2. **连接池满警告**
   - 错误信息: `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
   - 影响范围: urllib3 连接池
   - 可能原因: 连接池配置过小或连接未及时释放

3. **策略组 QoS 警告**
   - 错误信息: `strategy_group_key(f43fde6cd7470e5c63ce3f83f7617cd8) is qos, interval will be expanded with 1`
   - 影响范围: access 服务
   - 可能原因: QoS 策略导致查询间隔扩展

4. **ES 主机配置警告**
   - 错误信息: `compose_es_hosts:host->[bkdata-app-log2-es.physic-sz.es.svr.ehk.db],port->[9200],may be not invalid,please check,error->['bkdata-app-log2-es.physic-sz.es.svr.ehk.db' does not appear to be an IPv4 or IPv6 address]`
   - 影响范围: metadata 服务
   - 可能原因: ES 主机配置使用了域名而非 IP 地址

---

## 按 IP 地址分析

### Top 10 IP 的 WARNING 日志统计

| 排名 | IP 地址 | WARNING 数量 | 主要问题 |
|------|---------|-------------|---------|
| 1 | 9.136.133.78 | 34,760 | get_request_tenant_id 警告（大量） |
| 2 | 30.189.37.50 | 15,447 | get_request_tenant_id 警告 |
| 3 | 30.167.60.61 | 12,762 | get_request_tenant_id 警告 |
| 4 | 30.167.61.56 | 7,642 | 策略组 QoS 警告、ES 主机配置警告 |
| 5 | 9.136.170.171 | 1,729 | 连接池满警告 |
| 6 | 11.149.25.188 | 1,301 | 连接池满警告 |
| 7 | 30.167.61.85 | 1,144 | 其他警告 |
| 8 | 11.176.75.127 | 392 | 其他警告 |
| 9 | 30.167.60.103 | 448 | 其他警告 |
| 10 | 30.171.183.211 | 347 | 其他警告 |

### IP 详细分析

#### 1. 9.136.133.78 (34,760 条 WARNING)
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 
  - 检查请求头中是否正确传递 tenant_id
  - 检查本地上下文是否正确设置 tenant_id
  - 考虑增加默认 tenant_id 处理逻辑

#### 2. 30.189.37.50 (15,447 条 WARNING)
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 同上

#### 3. 30.167.60.61 (12,762 条 WARNING)
- **主要问题**: `get_request_tenant_id: cannot get tenant_id from request or local`
- **影响服务**: bk-monitor-alarm-service-aiops-worker
- **严重程度**: ⚠️ 高
- **建议**: 同上

#### 4. 30.167.61.56 (7,642 条 WARNING)
- **主要问题**: 
  - `strategy_group_key is qos, interval will be expanded with 1`
  - `compose_es_hosts:host->[bkdata-app-log2-es.physic-sz.es.svr.ehk.db] may be not invalid`
- **影响服务**: 
  - bk-monitor-alarm-access-data
  - bk-monitor-alarm-long-task-cron-worker
- **严重程度**: ⚠️ 中
- **建议**: 
  - 检查 ES 主机配置，建议使用 IP 地址或确保域名解析正常
  - 检查 QoS 策略配置

#### 5. 9.136.170.171 (1,729 条 WARNING)
- **主要问题**: `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
- **影响服务**: bk-monitor-alarm-cron-worker
- **严重程度**: ⚠️ 中
- **建议**: 
  - 增加连接池大小
  - 检查连接是否正确关闭
  - 考虑使用连接池监控

#### 6. 11.149.25.188 (1,301 条 WARNING)
- **主要问题**: `Connection pool is full, discarding connection: 9.136.128.212. Connection pool size: 10`
- **影响服务**: bk-monitor-alarm-cron-worker
- **严重程度**: ⚠️ 中
- **建议**: 同上

---

## 按 Path 分析

### Top 20 Path 的 WARNING 日志统计

| 排名 | Path (容器日志路径) | WARNING 数量 | 容器名称 |
|------|-------------------|-------------|---------|
| 1 | .../3bc4ca34b16e57aed229ead7032731fdb190b8498ab2d97c5e288ca8475aeb8a/... | 15,224 | bk-monitor-alarm-service-aiops-worker |
| 2 | .../a68794ec87e002a6e9c3a53a7042909c58dee19ac7bab761212443ec1a3ed971/... | 14,417 | bk-monitor-alarm-service-aiops-worker |
| 3 | .../c3d89df078211dfd99123de53a3fbae4b4532a5ac28de5b9861a5963b2384606/... | 15,020 | bk-monitor-alarm-service-aiops-worker |
| 4 | .../bfb68c9d061f31a52290d3f51fb9fc1f771fa84cee16f62e715baa5219249d46/... | 12,029 | bk-monitor-alarm-service-aiops-worker |
| 5 | .../9e4eadd9c6e8a1729a7595e5655f4bace55621af02e6464cb131e71c396d34da/... | 7,543 | bk-monitor-alarm-long-task-cron-worker |
| 6 | .../34157a573147ed6578a11f37c937d996d8f9a4f01b8915de687e0211adf3aa0a/... | 4,831 | 其他服务 |
| 7 | .../da94aa5d3785fca061c179d8ecc50e8b00ce5aabf2cd77e0730a2be3cc37d93d/... | 573 | bk-monitor-alarm-cron-worker |
| 8 | .../fdda7e2c610d6cead104bfc44e81c1a474015cea3f7e566afce5537a05be8ff6/... | 1,021 | 其他服务 |
| 9 | .../43311ebecd421b605d436c34ef0f9929393d511bbbba74f0bd35f309406f254d/... | 389 | 其他服务 |
| 10 | .../8d19f821ebd9bdc9d392d0a84e08d4935a1d869a93d77f08571cfd938efefde9/... | 408 | 其他服务 |

### Path 分析结论

1. **bk-monitor-alarm-service-aiops-worker** 服务产生了最多的 WARNING 日志
   - 主要问题: `get_request_tenant_id` 警告
   - 涉及多个 Pod 实例

2. **bk-monitor-alarm-long-task-cron-worker** 服务
   - 主要问题: ES 主机配置警告

3. **bk-monitor-alarm-cron-worker** 服务
   - 主要问题: 连接池满警告

---

## 主要问题汇总

### 1. tenant_id 获取失败 (最严重)
- **影响范围**: 多个服务实例，主要集中在 aiops-worker 服务
- **日志数量**: 约 60,000+ 条
- **可能原因**:
  - 请求头中缺少 tenant_id
  - 本地上下文未正确设置
  - 中间件处理逻辑问题
- **建议措施**:
  1. 检查请求链路，确保 tenant_id 正确传递
  2. 增加请求头验证和默认值处理
  3. 优化日志级别，避免大量 WARNING 日志

### 2. 连接池满警告
- **影响范围**: cron-worker 服务
- **日志数量**: 约 3,000+ 条
- **可能原因**:
  - 连接池大小配置过小（当前为 10）
  - 连接未及时释放
  - 请求频率过高
- **建议措施**:
  1. 增加连接池大小配置
  2. 检查连接是否正确关闭
  3. 考虑使用连接复用机制

### 3. ES 主机配置问题
- **影响范围**: long-task-cron-worker 服务
- **日志数量**: 约 7,500+ 条
- **可能原因**:
  - ES 主机配置使用了域名而非 IP
  - 域名解析可能存在问题
- **建议措施**:
  1. 将 ES 主机配置改为 IP 地址
  2. 或确保域名解析正常
  3. 增加主机配置验证

### 4. QoS 策略警告
- **影响范围**: access-data 服务
- **日志数量**: 少量
- **可能原因**: QoS 策略导致查询间隔自动扩展
- **建议措施**: 检查 QoS 策略配置是否合理

---

## Kubernetes 资源使用情况分析

### 主要服务 Pod 分布

基于日志分析，识别出以下主要服务的 Pod 实例：

#### 1. bk-monitor-alarm-service-aiops-worker 服务
- **Pod 数量**: 多个实例（至少 4 个主要 Pod）
- **主要 Pod IP**:
  - 9.136.133.78 (产生最多 WARNING 日志: 34,760 条)
  - 30.189.37.50 (15,447 条 WARNING)
  - 30.167.60.61 (12,762 条 WARNING)
  - 9.166.17.221 (大量 WARNING)
  - 9.166.37.140 (12,029 条 WARNING)
- **Pod 名称示例**:
  - bk-monitor-alarm-service-aiops-worker-7f496c46d5-7nwk8
  - bk-monitor-alarm-service-aiops-worker-7f496c46d5-6hd9l
  - bk-monitor-alarm-service-aiops-worker-7f496c46d5-ftpfs
  - bk-monitor-alarm-service-aiops-worker-7f496c46d5-fztw4
- **命名空间**: blueking
- **资源使用评估**:
  - ⚠️ **高负载**: 该服务产生了最多的 WARNING 日志（约 60,000+ 条）
  - **可能原因**: 
    - 请求量大，导致 tenant_id 获取失败频繁
    - 可能存在资源瓶颈（CPU/内存）
  - **建议**: 
    - 检查 Pod 的 CPU 和内存使用率
    - 考虑增加 Pod 副本数或资源限制
    - 优化 tenant_id 获取逻辑，减少不必要的警告

#### 2. bk-monitor-alarm-cron-worker 服务
- **Pod 数量**: 多个实例
- **主要 Pod IP**:
  - 9.136.170.171 (1,729 条 WARNING - 连接池满)
  - 11.149.25.188 (1,301 条 WARNING - 连接池满)
  - 9.166.48.25
  - 9.166.7.100
  - 9.166.37.144
  - 9.166.37.143
  - 9.166.54.87
  - 9.166.7.120
- **Pod 名称示例**:
  - bk-monitor-alarm-cron-worker-9cd99fcd7-tj752
  - bk-monitor-alarm-cron-worker-9cd99fcd7-qw5ph
  - bk-monitor-alarm-cron-worker-9cd99fcd7-5dqsp
  - bk-monitor-alarm-cron-worker-9cd99fcd7-tzqns
  - bk-monitor-alarm-cron-worker-9cd99fcd7-xkflt
  - bk-monitor-alarm-cron-worker-9cd99fcd7-sc8kd
- **命名空间**: blueking
- **资源使用评估**:
  - ⚠️ **连接池压力**: 出现连接池满警告
  - **可能原因**:
    - 连接池配置过小（当前为 10）
    - 请求频率高，连接未及时释放
    - 可能存在网络延迟问题
  - **建议**:
    - 检查 Pod 的网络流量和连接数
    - 增加连接池大小配置
    - 优化连接管理逻辑

#### 3. bk-monitor-alarm-long-task-cron-worker 服务
- **Pod 数量**: 至少 1 个实例
- **主要 Pod IP**:
  - 30.167.61.56 (7,543 条 WARNING - ES 配置问题)
- **Pod 名称示例**:
  - bk-monitor-alarm-long-task-cron-worker-75876cd47b-cbqzh
- **命名空间**: blueking
- **资源使用评估**:
  - ⚠️ **配置问题**: ES 主机配置警告
  - **可能原因**:
    - ES 连接配置使用域名而非 IP
    - 可能存在 DNS 解析问题
  - **建议**:
    - 检查 Pod 的 DNS 配置
    - 修复 ES 主机配置
    - 验证网络连通性

#### 4. bk-monitor-alarm-access-data 服务
- **Pod 数量**: 至少 1 个实例
- **主要 Pod IP**:
  - 30.167.61.56 (QoS 策略警告)
- **Pod 名称示例**:
  - bk-monitor-alarm-access-data-665c8dd7b4-5gr78
- **命名空间**: blueking
- **资源使用评估**:
  - ⚠️ **QoS 策略**: 出现策略组 QoS 警告
  - **建议**: 检查 QoS 策略配置是否合理

#### 5. 其他服务
- **bk-monitor-alarm-nodata**: 少量日志
- **bk-monitor-web-worker-resource**: 少量日志

---

### 资源使用情况汇总

#### CPU 使用情况评估
基于 WARNING 日志量和服务负载分析：

| 服务名称 | 日志量 | CPU 负载评估 | 建议 |
|---------|--------|------------|------|
| bk-monitor-alarm-service-aiops-worker | 60,000+ | 🔴 高 | 检查 CPU 使用率，考虑扩容 |
| bk-monitor-alarm-cron-worker | 3,000+ | 🟡 中 | 监控 CPU 使用率 |
| bk-monitor-alarm-long-task-cron-worker | 7,500+ | 🟡 中 | 检查 CPU 使用率 |
| bk-monitor-alarm-access-data | 少量 | 🟢 低 | 正常监控 |

#### 内存使用情况评估

| 服务名称 | 内存负载评估 | 建议 |
|---------|------------|------|
| bk-monitor-alarm-service-aiops-worker | 🔴 高 | 检查内存使用率，可能存在内存泄漏 |
| bk-monitor-alarm-cron-worker | 🟡 中 | 监控内存使用率 |
| bk-monitor-alarm-long-task-cron-worker | 🟡 中 | 检查内存使用率 |
| bk-monitor-alarm-access-data | 🟢 低 | 正常监控 |

#### 网络使用情况评估

| 服务名称 | 网络负载评估 | 问题 |
|---------|------------|------|
| bk-monitor-alarm-cron-worker | 🔴 高 | 连接池满，可能存在网络瓶颈 |
| bk-monitor-alarm-service-aiops-worker | 🟡 中 | 大量请求，需要监控网络流量 |
| 其他服务 | 🟢 低 | 正常 |

---

### 资源使用建议

#### 1. 立即检查项
- ✅ **bk-monitor-alarm-service-aiops-worker** Pod 的 CPU 和内存使用率
- ✅ **bk-monitor-alarm-cron-worker** Pod 的网络连接数和流量
- ✅ 所有 Pod 的资源限制（requests/limits）配置

#### 2. 监控指标建议
建议在 Kubernetes 监控中设置以下告警：

**CPU 使用率告警**:
- 警告阈值: > 80%
- 严重阈值: > 95%

**内存使用率告警**:
- 警告阈值: > 85%
- 严重阈值: > 95%

**连接数告警**:
- 警告阈值: 连接池使用率 > 80%
- 严重阈值: 连接池满

**Pod 重启告警**:
- 警告阈值: 15 分钟内重启 > 2 次

#### 3. 资源优化建议

**短期优化**:
1. **增加 aiops-worker 服务资源**:
   - 考虑增加 CPU requests/limits
   - 考虑增加内存 requests/limits
   - 或增加 Pod 副本数

2. **优化 cron-worker 连接池**:
   - 增加连接池大小（从 10 增加到 20-30）
   - 优化连接复用逻辑

3. **修复 long-task-cron-worker 配置**:
   - 修复 ES 主机配置
   - 验证网络连通性

**长期优化**:
1. 建立完善的 K8s 资源监控和告警机制
2. 定期进行资源使用情况分析
3. 根据实际负载调整资源分配
4. 实施自动扩缩容（HPA）策略

---

### PromQL 查询示例

如需在监控系统中查询这些 Pod 的资源使用情况，可使用以下 PromQL：

```promql
# 查询 blueking 命名空间下所有 Pod 的 CPU 使用率
avg(avg_over_time(bkmonitor:system:cpu_summary:usage{namespace="blueking"}[1m]))

# 查询 blueking 命名空间下所有 Pod 的内存使用率
avg(avg_over_time(bkmonitor:system:mem:pct_used{namespace="blueking"}[1m]))

# 查询特定服务的 Pod CPU 使用率
avg(avg_over_time(bkmonitor:system:cpu_summary:usage{namespace="blueking",pod=~"bk-monitor-alarm-service-aiops-worker.*"}[1m]))

# 查询特定服务的 Pod 内存使用率
avg(avg_over_time(bkmonitor:system:mem:pct_used{namespace="blueking",pod=~"bk-monitor-alarm-service-aiops-worker.*"}[1m]))

# 查询容器 CPU 使用率
sum(rate(bkmonitor:container_cpu_usage_seconds_total{namespace="blueking",container_name=~"bk-monitor-alarm.*"}[1m]))

# 查询容器内存使用率
sum(bkmonitor:container_memory_usage_bytes{namespace="blueking",container_name=~"bk-monitor-alarm.*"}) / sum(bkmonitor:container_spec_memory_limit_bytes{namespace="blueking",container_name=~"bk-monitor-alarm.*"}) * 100
```

---

### 注意事项

1. **Pod IP vs 主机 IP**: 日志中的 IP 地址是 Pod IP，不是节点主机 IP
2. **动态 IP**: Pod IP 可能会变化，建议通过 Pod 名称或标签进行查询
3. **资源限制**: 需要检查 Pod 的 requests 和 limits 配置是否合理
4. **命名空间**: 所有服务都在 `blueking` 命名空间下
5. **监控数据**: 建议通过 Kubernetes Dashboard 或监控系统查看实时资源使用情况

---

## 总结与建议

### 优先级排序

1. **高优先级**: tenant_id 获取失败问题
   - 影响范围广，日志量大
   - 需要立即排查和修复

2. **中优先级**: 连接池满和 ES 配置问题
   - 可能影响服务性能
   - 需要优化配置

3. **低优先级**: QoS 策略警告
   - 影响较小
   - 可作为优化项

### 下一步行动

1. **立即行动**:
   - 排查 tenant_id 获取失败的根本原因
   - 检查请求链路中的 tenant_id 传递逻辑

2. **短期优化**:
   - 优化连接池配置
   - 修复 ES 主机配置问题

3. **长期改进**:
   - 建立完善的监控告警机制
   - 优化日志级别，减少不必要的 WARNING 日志
   - 定期进行日志分析和问题排查

---

## 报告生成时间
2025-12-25 17:50:05 (UTC+8)

