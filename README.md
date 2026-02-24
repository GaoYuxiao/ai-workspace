# AI Workspace

蓝鲸监控相关的 AI Skills、产品需求文档(PRD)与工具集。

## 项目结构

```
├── skill/                     # Cursor Agent Skills
│   ├── log-multi-dimensional-analyzer/   # 日志多维分析 Skill
│   ├── mcp-data-fetcher/                 # MCP 数据拉取 Skill
│   ├── page-automation-tester/           # 页面自动化测试 Skill
│   └── skill-creator/                    # Skill 创建器
├── docs/                      # 产品文档与设计
│   ├── 日志检索/              # 日志检索相关 PRD 与方案
│   ├── mcp/                   # MCP 工具文档
│   ├── grok/                  # Grok 规则说明
│   └── 测试/                  # 测试相关文档
├── rum-app-management/        # RUM 应用管理（PRD、原型）
├── testcase/                  # 自动化测试用例与报告
├── metrics_charts/            # 监控指标图表
├── log-viewer-bkmonitor/      # 日志查看器
├── bkmonitor-files/           # 监控平台相关文件
├── reports/                   # 分析报告
├── scripts/                   # 工具脚本
├── components/                # 前端组件
├── mcp_log_server.py          # 日志检索 MCP Server
└── mcp_config.json            # MCP 配置
```

## Skills

| Skill | 说明 |
|-------|------|
| log-multi-dimensional-analyzer | 日志多维度分析，支持聚合、趋势、异常检测 |
| mcp-data-fetcher | 通过 MCP 协议拉取监控数据 |
| page-automation-tester | Web 页面自动化测试 |
| skill-creator | 辅助创建新的 Cursor Agent Skill |

## 产品文档

- **日志检索** — 客户端日志检索、统一日志检索平台、日志池统一检索 PRD
- **RUM 应用管理** — RUM 应用接入 PRD 与原型
- **登录页** — 登录页需求文档

## MCP 日志服务

内置的日志检索 MCP Server，支持分页、过滤、流式传输，详见 `mcp_log_server.py`。

```bash
pip install -r requirements.txt
```

## License

MIT
