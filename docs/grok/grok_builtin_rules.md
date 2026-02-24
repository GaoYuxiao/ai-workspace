# Grok 内置规则建议清单

| 名称 | 描述 | 典型日志样例（缩写） | 关键字段 |
| --- | --- | --- | --- |
| `NGINX_ACCESSLOG` | Nginx 访问日志（通用组合） | `10.0.0.1 - - [03/Feb/2025:12:00:01 +0800] "GET /api/orders HTTP/1.1" 200 512 "-" "Mozilla/5.0"` | `client_ip`, `timestamp`, `verb`, `request`, `status`, `bytes`, `referrer`, `user_agent` |
| `APACHE_ACCESSLOG` | Apache Combined Log | `192.168.0.2 - - [03/Feb/2025:12:00:02 +0800] "POST /login HTTP/1.1" 302 123 "https://foo" "Chrome/120"` | `client_ip`, `timestamp`, `verb`, `request`, `status`, `bytes`, `referrer`, `agent` |
| `JAVA_STACKTRACE` | Java 异常栈 | `Exception in thread "main" java.lang.NullPointerException` `\tat com.example.Service.doWork(Service.java:42)` | `thread`, `exception`, `message`, `class`, `method`, `line` |
| `SPRING_BOOT_LOG` | Spring/Logback 模式 | `2025-02-03 12:00:03.123  INFO 12345 --- [nio-8080-exec-1] c.e.OrderController : created orderId=88` | `timestamp`, `level`, `pid`, `thread`, `logger`, `message` |
| `MYSQL_GENERAL_LOG` | MySQL 通用查询日志 | `2025-02-03T12:00:04Z    11 Query SELECT * FROM orders WHERE id=88` | `timestamp`, `conn_id`, `command`, `query` |
| `PG_LOG` | PostgreSQL 日志 | `2025-02-03 12:00:05.678 UTC [12345] LOG:  statement: INSERT INTO ...` | `timestamp`, `pid`, `level`, `message`, `statement` |
| `NGINX_ERROR` | Nginx 错误日志 | `2025/02/03 12:00:06 [error] 1234#0: *1 upstream timed out while reading` | `timestamp`, `level`, `pid`, `worker`, `message` |
| `K8S_CONTAINER_LOG` | 标准 JSON 行 | `{"log":"GET /healthz 200","stream":"stdout","time":"2025-02-03T12:00:07Z"}` | `log`, `stream`, `time` |
| `SYSTEMD_JOURNAL` | systemd journalctl | `Feb  3 12:00:08 host1 systemd[1]: Started Foo Service.` | `month`, `day`, `time`, `host`, `unit`, `message` |
| `WAF_ALERT` | Web 防火墙告警 | `2025-02-03T12:00:09Z ALERT waf rule=SQLi src=10.0.0.5 path=/search` | `timestamp`, `severity`, `rule`, `src`, `path` |

> 每条规则均可拆分成基础模式，例如 `IPORHOST`, `HTTPVERB`, `URIPATHPARAM` 等，以便扩展其他场景。

## 示例定义片段

- `NGINX_ACCESSLOG`  
  `%{IPORHOST:client_ip} %{DATA:ident} %{DATA:auth} \\[%{HTTPDATE:timestamp}\\] "%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:http_version}" %{INT:status} %{INT:bytes} "%{DATA:referrer}" "%{GREEDYDATA:user_agent}"`

- `JAVA_STACKTRACE`  
  `Exception in thread "%{DATA:thread}" %{JAVACLASS:exception}: %{GREEDYDATA:message}`  
  `\\s+at %{JAVACLASS:class}\\.%{WORD:method}\\(%{DATA:file}:%{INT:line}\\)`

其余规则可参照以上格式，补齐样例与字段文档后纳入内置库。***


