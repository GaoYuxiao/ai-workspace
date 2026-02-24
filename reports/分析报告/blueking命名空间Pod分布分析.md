# blueking 命名空间 Pod 分布分析

## 分析概览

- **命名空间**: blueking
- **索引集ID**: 2444
- **业务ID**: 2
- **分析时间范围**: 最近24小时
- **总Pod数**: 100个
- **总日志量**: 259,283 条

## Pod 分类统计

### 1. 核心服务 Pod（长期运行 - ReplicaSet）

**统计摘要**:
- Pod数量: 8个
- 日志总量: 256,155条
- 占比: 98.79%

#### 详细分布

| Pod名称 | 日志数量 | 占比 | 服务类型 |
|---------|---------|------|---------|
| bkpaas3-apiserver-web-5bdc57969b-2xlcf | 52,507 | 20.25% | Web服务 |
| bkpaas3-svc-bkrepo-web-558766447d-m5cdb | 62,993 | 24.29% | Web服务 |
| bkpaas3-svc-mysql-web-74fb8f566d-rqqq9 | 59,345 | 22.89% | Web服务 |
| bkpaas3-apiserver-web-5bdc57969b-pnk9j | 32,851 | 12.67% | Web服务 |
| bkpaas3-apiserver-web-5bdc57969b-rmbxt | 14,695 | 5.67% | Web服务 |
| bkpaas3-apiserver-web-5bdc57969b-9xt56 | 14,078 | 5.43% | Web服务 |
| bkpaas3-webfe-web-7488d566-t5zlh | 17,423 | 6.72% | Web服务 |
| **小计** | **253,892** | **97.92%** | |

#### Worker服务 Pod

| Pod名称 | 日志数量 | 占比 | 服务类型 |
|---------|---------|------|---------|
| bkpaas3-apiserver-worker-67d9fbdfb8-nr88r | 661 | 0.25% | Worker服务 |
| bkpaas3-apiserver-worker-67d9fbdfb8-p242d | 647 | 0.25% | Worker服务 |
| bkpaas3-apiserver-worker-67d9fbdfb8-sdx5b | 323 | 0.12% | Worker服务 |
| bkpaas3-apiserver-worker-67d9fbdfb8-xppqr | 632 | 0.24% | Worker服务 |
| **小计** | **2,263** | **0.87%** | |

---

### 2. 定时任务 Pod（Job类型）

**统计摘要**:
- Pod数量: 92个
- 日志总量: 3,128条
- 占比: 1.21%

#### 2.1 清理超时Slug Pod任务

**任务类型**: `bkpaas3-apiserver-clean-timeout-slug-pod`

| 时间戳范围 | Pod数量 | 日志总量 | 平均每个Pod日志数 |
|-----------|---------|---------|------------------|
| 1765972800 ~ 1766055600 | 24个 | 576条 | 24条 |

**特点**:
- 每小时执行一次
- 每个Pod运行时间短，日志量固定（约24条）
- 任务名称格式: `bkpaas3-apiserver-clean-timeout-slug-pod-{timestamp}-{random}`

#### 2.2 删除实例任务

**任务类型**: `bkpaas3-apiserver-deleting-instances`

| 时间戳范围 | Pod数量 | 日志总量 | 平均每个Pod日志数 |
|-----------|---------|---------|------------------|
| 1765972800 ~ 1766057400 | 48个 | 1,248条 | 26条 |

**特点**:
- 每3-5分钟执行一次
- 每个Pod日志量约26条
- 任务名称格式: `bkpaas3-apiserver-deleting-instances-{timestamp}-{random}`

#### 2.3 更新待处理状态任务

**任务类型**: `bkpaas3-apiserver-update-pending-status`

| 时间戳范围 | Pod数量 | 日志总量 | 平均每个Pod日志数 |
|-----------|---------|---------|------------------|
| 1765972800 ~ 1766052000 | 19个 | 437条 | 23条 |

**特点**:
- 每3-5分钟执行一次
- 每个Pod日志量约23条
- 任务名称格式: `bkpaas3-apiserver-update-pending-status-{timestamp}-{random}`

#### 2.4 清理Slug Tar任务

**任务类型**: `bkpaas3-apiserver-clean-slug-tar`

| Pod数量 | 日志总量 | 平均每个Pod日志数 |
|---------|---------|------------------|
| 1个 | 24条 | 24条 |

#### 2.5 MySQL删除实例任务

**任务类型**: `bkpaas3-svc-mysql-deleting-instances`

| Pod数量 | 日志总量 | 平均每个Pod日志数 |
|---------|---------|------------------|
| 1个 | 176条 | 176条 |

---

## Pod 分布可视化

### 按服务类型分组

```
核心服务 Pod (8个)
├── Web服务 (7个) - 253,892条日志 (97.92%)
│   ├── bkpaas3-apiserver-web (4个) - 114,131条 (44.01%)
│   ├── bkpaas3-svc-bkrepo-web (1个) - 62,993条 (24.29%)
│   ├── bkpaas3-svc-mysql-web (1个) - 59,345条 (22.89%)
│   └── bkpaas3-webfe-web (1个) - 17,423条 (6.72%)
└── Worker服务 (4个) - 2,263条日志 (0.87%)
    └── bkpaas3-apiserver-worker (4个) - 2,263条 (0.87%)

定时任务 Pod (92个) - 3,128条日志 (1.21%)
├── clean-timeout-slug-pod (24个) - 576条
├── deleting-instances (48个) - 1,248条
├── update-pending-status (19个) - 437条
├── clean-slug-tar (1个) - 24条
└── mysql-deleting-instances (1个) - 176条
```

### 日志量分布图

```
日志量分布（按Pod类型）:
████████████████████████████████████████████████████████████████████████████████████████████████████ 核心服务 (98.79%)
██ 定时任务 (1.21%)
```

---

## 关键发现

### 1. Pod 数量分布
- **核心服务Pod**: 仅8个，但占98.79%的日志量
- **定时任务Pod**: 92个，但仅占1.21%的日志量
- **Pod总数**: 100个

### 2. 日志量分布
- **高度集中**: 前3个Pod占67.43%的日志量
  - `bkpaas3-svc-bkrepo-web-558766447d-m5cdb`: 62,993条 (24.29%)
  - `bkpaas3-svc-mysql-web-74fb8f566d-rqqq9`: 59,345条 (22.89%)
  - `bkpaas3-apiserver-web-5bdc57969b-2xlcf`: 52,507条 (20.25%)

### 3. 服务架构特征
- **Web服务为主**: 7个Web服务Pod产生97.92%的日志
- **Worker服务**: 4个Worker Pod，日志量较少（0.87%）
- **定时任务**: 大量短期运行的Job Pod，主要用于清理和维护

### 4. 定时任务执行频率
- **clean-timeout-slug-pod**: 每小时执行（24次/天）
- **deleting-instances**: 每3-5分钟执行（约288次/天）
- **update-pending-status**: 每3-5分钟执行（约288次/天）

---

## 建议

### 1. 监控重点
- **重点关注**: 前3个核心服务Pod的日志量和质量
- **告警阈值**: 为高日志量Pod设置告警阈值

### 2. 资源优化
- **负载均衡**: 考虑在4个`bkpaas3-apiserver-web` Pod之间更均匀地分配负载
- **定时任务**: 考虑合并或优化定时任务，减少Pod创建频率

### 3. 日志管理
- **日志分级**: 区分核心服务日志和定时任务日志
- **存储策略**: 对定时任务日志采用更短的保留期

### 4. 运维建议
- **Pod生命周期**: 定时任务Pod生命周期短，需要关注Pod创建和销毁的监控
- **资源使用**: 核心服务Pod是资源消耗的主要来源，需要重点监控

---

**报告生成时间**: 2025-01-19
**分析工具**: 蓝鲸监控日志服务 MCP 工具


