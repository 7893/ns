# NS 可观测性与日志规范文档（ns-observability-guidelines.md）

**文档ID**：ns-observability-guidelines
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本指南旨在统一 NS 项目在结构化日志、指标埋点、Trace ID 传递、告警配置等方面的可观测性实践，确保项目具备可审计、可定位、可维护的运行特性。

---

## 📋 结构化日志格式规范

所有 Cloud Function 与 Cloud Run 应输出如下结构化 JSON 日志：

```json
{
  "timestamp": "2025-09-04T15:30:12.123Z",
  "severity": "INFO",
  "trace_id": "abc123-xyz456",
  "execution_id": "exec-20250904-001",
  "job_id": "apod-daily",
  "status": "success",
  "duration_ms": 843,
  "event_type": "job_dispatched",
  "details": { "item_count": 23 }
}
```

> 日志应符合 GCP Logging JSON 结构，便于索引、筛选、告警与导出。

### 字段定义说明

| 字段名            | 类型      | 说明                                       |
| -------------- | ------- | ---------------------------------------- |
| `timestamp`    | ISO 时间戳 | 日志记录时间                                   |
| `severity`     | 字符串     | `INFO` / `ERROR` / `WARNING` 等           |
| `trace_id`     | 字符串     | 贯穿任务流程的唯一标识，来自 Pub/Sub 消息或生成于入口          |
| `execution_id` | 字符串     | 本次函数执行的唯一 ID                             |
| `job_id`       | 字符串     | 当前处理任务类型，如 `apod-daily`                  |
| `status`       | 字符串     | 任务执行状态（success/failed/skipped）           |
| `duration_ms`  | 数值      | 执行时长（毫秒）                                 |
| `event_type`   | 字符串     | 任务事件阶段，如 `job_dispatched` / `job_failed` |
| `details`      | 任意对象    | 附加元信息（可选）                                |

---

## 🔁 Trace ID 传递机制

| 阶段                   | 来源                           | Trace ID 传递方式               |
| -------------------- | ---------------------------- | --------------------------- |
| 用户触发或定时调度            | Cloud Scheduler / Pub/Sub    | 初始生成 UUID，写入消息属性 `trace_id` |
| Cloud Function / Run | 接收消息 → 提取 trace\_id → 持续传入日志 | 使用环境变量或函数上下文传递              |
| 错误告警 / 回调            | 附带 trace\_id                 | 支持用户在前端页面追溯任务流程             |

---

## 📈 指标收集建议

* 可选启用 Cloud Monitoring 自定义指标：

  * 每分钟成功抓取数量（per job）
  * 平均执行时间（按 job 聚合）
  * 每日失败次数（按 severity）

> 如暂不启用，可在日志中输出结构化字段，后续可基于日志导出计算。

---

## 🚨 告警与错误通知

### 推荐告警类型：

| 告警类型           | 条件示例                        |
| -------------- | --------------------------- |
| 函数执行失败率高       | `ERROR` 日志超过 X 次 / 分钟       |
| Pub/Sub 积压消息过多 | Subscription 未消费数量 > 阈值     |
| 死信队列累积         | DLQ 中消息条数持续增长               |
| 配置缺失或非法        | `job_config_not_found` 事件出现 |

### 告警输出渠道

* 初始阶段建议启用 GCP Monitoring 告警 → 邮件通知
* 日志可导出至 BigQuery / GCS，便于人工分析
* 日志可打上 `notify=true` 字段触发日志路由（可选）

---

## 📦 日志 Sink 与导出建议

| 导出目标                 | 用途                    |
| -------------------- | --------------------- |
| BigQuery Dataset     | 用于结构化查询、失败任务分析、任务趋势报告 |
| Cloud Storage Bucket | 保留原始日志归档，支持低频访问或审计    |

---

## 🧠 最佳实践摘要

* 所有函数输出 JSON 日志，确保可解析、可导出
* 日志字段应统一，支持跨函数查询与追踪
* trace\_id 应全程贯穿，支持任务链路回溯
* 日志即指标，指标即告警（logs → metrics → alerts）

---

## ✅ 推荐配套文档

* [`ns-technical-design.md`](./ns-technical-design.md) – 说明日志传递机制
* [`ns-security-policy.md`](./ns-security-policy.md) – 日志脱敏与权限管理建议
* [`ns-resource-inventory.md`](./ns-resource-inventory.md) – Logging Sink 与资源对应关系
