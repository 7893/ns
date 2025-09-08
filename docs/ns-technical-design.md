# NS 技术架构设计文档（ns-technical-design.md）

**文档ID**：ns-technical-design
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协同支持

---

## 🎯 技术设计目标

本项目采用纯 GCP Serverless 架构，目标是构建一套具备事件驱动、幂等执行、全链路可观测性、最小维护成本的现代云端处理平台。

本设计文档聚焦技术细节，补充架构总览中的实现原则，涵盖以下方面：

1. 事件机制（Pub/Sub）
2. Trace 与 Execution 流程
3. 幂等性策略
4. 配置驱动与冷启动
5. 前端与后端交互逻辑
6. 日志结构与追踪
7. 错误处理与失败任务设计

---

## 1️⃣ 事件驱动机制设计

* **核心驱动通道**：所有异步任务由 `ns-topic-job` Pub/Sub 主题触发
* **消息格式**（标准化 JSON Schema）：

```json
{
  "job_id": "apod-20250904",
  "trigger": "scheduler" | "manual",
  "trace_id": "ns-20250904-001",
  "timestamp": "2025-09-04T16:00:00Z"
}
```

* **发布者**：

  * `scheduler-entry` 函数（来自 Cloud Scheduler）
  * `manual-trigger` 函数（来自前端页面）
* **订阅者**：各抓取函数订阅该主题，根据 job\_id 路由处理

✅ 所有抓取函数仅通过 Pub/Sub 接收触发，确保无直接耦合。

---

## 2️⃣ Trace 流程与执行上下文

* **trace\_id** 为每次执行的唯一标识符

  * 由触发端（scheduler/manual）生成
  * 格式统一：`ns-<date>-<序号>` 形式，具备时间可读性
* **上下文传递**：trace\_id 写入日志、FireStore 状态表、返回值
* **生命周期流转**：

  * 启动：trace\_id 写入 Firestore 中 status 表，标记 `status=pending`
  * 成功：更新为 `status=success` 并记录元信息
  * 失败：记录 `status=failed`，含错误原因

✅ trace\_id 是全链路诊断、去重、重试的核心。

---

## 3️⃣ 幂等性策略

* **契约约定**：所有 Cloud Function 默认视为幂等任务
* **实现方式**：

  * 接收到消息时，先查询 Firestore 中是否已存在 `trace_id` 执行记录（状态为 `success`）
  * 若存在则直接忽略（或打出日志 `already_processed`）
* **可选优化**：将执行记录写入一个 `idempotency` 集合，避免状态表混杂
* **文档约定**：Terraform 中可在 description 字段标注 `"idempotent: true"`

✅ 幂等性是系统稳定性基石，尤其在 Pub/Sub 重投递情形下。

---

## 4️⃣ 配置加载与缓存机制

* 所有任务参数配置（如起止日期、抓取模式、目标源）保存在 Firestore 的 `job_config` 集合中
* Cloud Function 启动时读取配置，但不缓存到内存
* **热更新机制建议**（预留）：

  * 配置更新时发布 `config_updated` 事件到 Pub/Sub
  * 函数监听该事件并刷新本地缓存（如后期使用 long-running Job）

✅ 保留“配置即事件”的设计能力，支持未来演进为“GitOps 式配置系统”

---

## 5️⃣ 前端与后端交互逻辑

* **前端页面部署**：静态 HTML 页面部署于 Cloud Run Service
* **功能职责**：展示任务配置状态，可能包含手动触发按钮
* **交互方式**：

  * 发起 HTTP 请求到 `manual_trigger` Cloud Function
  * 函数根据传参生成 trace\_id 并发布 Pub/Sub 消息
  * 前端不直接接触 Firestore，仅通过函数间接访问

✅ 安全、可审计、权限清晰

---

## 6️⃣ 日志结构与追踪策略

* 所有日志均结构化输出：`textPayload` ➜ `jsonPayload`
* 必含字段：

```json
{
  "severity": "INFO|ERROR",
  "trace_id": "ns-20250904-001",
  "job_id": "apod-20250904",
  "function": "apod-fetcher",
  "status": "success|fail",
  "message": "..."
}
```

* **工具链**：GCP Logging + Log-based Metrics + Alert Policy
* **统一 trace 输出**：日志中携带 trace\_id，方便聚合分析与过滤追踪

✅ 所有执行与异常均可定位、溯源、归因。

---

## 7️⃣ 错误处理与失败路径

* **自动重试**：Cloud Function 默认启用最大重试 3 次（可调）
* **死信队列 DLQ**：Pub/Sub 绑定 DLQ 主题，消息失败后投递至 DLQ
* **失败处理器建议**：

  * 独立失败任务收集函数
  * 周期性扫描 DLQ，归档失败 trace\_id 与原始 payload
  * 写入 Firestore `failures` 集合，供人工干预与统计分析

✅ 失败是正常路径，系统必须能自愈而非依赖“喊人”

---

## ✅ 总结：技术设计十大原则

1. 所有流程均事件驱动（Pub/Sub）
2. trace\_id 为全链路核心 ID
3. 所有函数幂等，重试安全
4. 配置集中管理，支持热更新
5. 前端不可直接读/写数据库，权限隔离
6. 日志结构统一，可聚合分析
7. 错误路径有归宿（DLQ + 失败处理器）
8. 所有资源由 Terraform 管理
9. 函数独立部署，职责单一
10. 文档与架构由 AI 协作生成，保持一致性

---

📄 下一步建议查看：

* [`ns-deployment-guide.md`](./ns-deployment-guide.md)：部署命令、环境变量与版本切换方案
* [`ns-observability-guidelines.md`](./ns-observability-guidelines.md)：日志、告警与指标设计说明

*本项目强调以设计为先、结构清晰、自动化优先，结合 AI 提升工程质量与维护效率。*
