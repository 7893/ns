# NS 数据结构与存储设计（ns-data-design.md）

**文档ID**：ns-data-design
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本文件定义 NS 项目核心数据结构、状态模型与 GCP 存储选型，确保抓取任务、运行状态与日志具备清晰的数据落点、可演化的数据结构与良好的可查询性。

---

## 🧱 存储选型概览

| 存储类型     | 用途             | GCP 服务                     | 存储格式            |
| -------- | -------------- | -------------------------- | --------------- |
| 配置型数据    | 用户参数配置         | Firestore（Native 模式）       | 文档型 JSON        |
| 状态型数据    | 抓取执行状态         | Firestore                  | 文档型 JSON（分状态集合） |
| 可观测性数据   | Trace 日志 / 告警  | Cloud Logging / PubSub DLQ | 结构化 JSON + 日志标签 |
| 对象型数据    | 临时下载文件 / 函数压缩包 | Cloud Storage              | 任意二进制对象         |
| 元数据/失败信息 | 失败任务摘要         | Firestore `failures` 集合    | 索引化 JSON        |

---

## 🧩 Firestore 数据结构设计

### 1. `job_config` 配置集合

```json
{
  "job_id": "apod-daily",
  "active": true,
  "cron": "0 8 * * *",
  "fetch_url": "https://api.nasa.gov/...",
  "params": {
    "api_key": "..."
  },
  "post_process": true,
  "updated_at": "2025-09-04T00:00:00Z"
}
```

* 用途：前端展示与用户可编辑参数配置
* 使用 Cloud Run 前端调用 Cloud Functions API 实时读取

### 2. `job_status` 状态集合

```json
{
  "trace_id": "abc-123",
  "job_id": "apod-daily",
  "started_at": "2025-09-04T08:00:01Z",
  "status": "success", // "pending" | "running" | "error"
  "message": "Successfully fetched image",
  "duration_ms": 1784,
  "output_url": "gs://..."
}
```

* 用途：任务执行过程追踪与历史归档
* trace\_id 来自事件驱动的 Pub/Sub 消息标识

### 3. `failures` 集合

```json
{
  "trace_id": "def-456",
  "job_id": "neo-daily",
  "error_code": "HTTP_500",
  "message": "Upstream API timeout",
  "attempts": 3,
  "timestamp": "2025-09-04T08:10:22Z"
}
```

* 来源：Pub/Sub 死信队列（DLQ）或函数异常处理器
* 用于后续失败分析、任务看板、自动重试器等

---

## 📦 对象存储结构设计

### Cloud Storage Bucket

* 命名示例：`ns-temp-bucket`
* 结构：

  ```
  gs://ns-temp-bucket/
    apod-daily/
      2025-09-04/
        original.jpg
        meta.json
  ```
* 生命周期策略：7 天过期清除临时对象

---

## 🔍 查询优化建议

| 集合          | 建议索引                       | 查询方式        |
| ----------- | -------------------------- | ----------- |
| job\_status | job\_id + started\_at DESC | 查看某任务最近执行情况 |
| failures    | job\_id + timestamp DESC   | 查看近期失败任务摘要  |
| job\_config | job\_id（唯一索引）              | 快速读取配置      |

✅ Firestore 索引在控制台可自动创建，开发期可使用 CLI 脚本初始化

---

## 🧠 数据设计原则

1. **配置即状态**：配置数据需可热更新、可回滚、可审计
2. **状态即日志**：状态集合承担系统追踪与可视化功能
3. **失败即事件**：失败处理统一化、系统化，避免人为介入
4. **临时即清除**：对象存储采用生命周期策略自动清理
5. **无框架依赖**：避免 Firebase / ORM 等额外依赖，便于最小化部署

---

## ✅ 总结

NS 项目的数据结构基于：事件驱动 + 状态追踪 + 配置热更新 三大原则，确保结构简洁、可控并支持长期演化。

📄 推荐继续阅读：

* [`ns-technical-design.md`](./ns-technical-design.md)
* [`ns-security-policy.md`](./ns-security-policy.md)
* [`ns-architecture-summary.md`](./ns-architecture-summary.md)
