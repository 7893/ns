# NS 架构总览与职责划分（ns-architecture-summary.md）

**文档ID**：ns-architecture-summary
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协同支持

---

## 🎯 项目定位与背景

`ns` 是一个由个人主导、AI 协同完成的现代软件工程实践项目。它基于 Google Cloud Platform（GCP）全家桶，采用 Serverless 架构，聚焦事件驱动流程、可观测性落地、IaC 自动化与安全权限设计。

目标是通过一个实际的云函数抓取与处理平台，全面验证现代架构范式的工程可行性与最小维护成本，强调“Human-led / AI-supported” 的设计与实现模式。

---

## 🧱 架构结构总览

整个系统采用模块化结构，分为五大核心模块，每个模块独立部署、职责清晰：

### 1. 🧭 任务入口模块（调度与触发）

* **定时触发**：通过 Cloud Scheduler 周期性调用启动函数
* **手动触发**：前端页面（部署于 Cloud Run）通过 HTTP API 发布 Pub/Sub 消息
* **配置驱动**：所有任务均读取 Firestore 中的参数配置文档（traceable）

### 2. ⚙️ 抓取与处理模块（Cloud Functions）

* **功能职责**：每个抓取模块封装为独立函数，负责外部 API 抓取与处理
* **触发方式**：通过 Pub/Sub 消息驱动，确保异步解耦
* **幂等机制**：执行 trace\_id 驱动，防止重复执行

### 3. 🗂️ 状态记录模块（Firestore）

* **配置存储**：任务参数配置文档（如 jobId、时间范围、目标源）
* **状态记录**：每次任务执行后，将成功/失败状态写入状态表（traceable）
* **可视化支持**：供前端页面读取展示当前配置与执行状态

### 4. 🔍 可观测性与监控模块

* **日志记录**：结构化日志 + trace\_id 全链路追踪
* **告警机制**：基于日志内容设置告警（失败次数、无响应、异常字段等）
* **死信处理**：Pub/Sub DLQ 收集失败消息，后续统一处理

### 5. 🖥️ 前端页面模块（Cloud Run）

* **功能定位**：用于展示任务配置、状态、可选触发接口
* **部署方式**：静态 HTML + JS 部署于 Cloud Run，HTTPS 自动生成
* **接口交互**：通过调用 Cloud Run 提供的 HTTP API 与 Firestore/函数交互

---

## 🌐 架构图（文字版）

```
[ Cloud Scheduler ] ──▶ [ ns_scheduler_entry (Function) ] ──▶ [ Pub/Sub: ns-topic-job ]
                                                               │
[ 前端页面 (Cloud Run) ] ──▶ [ ns_manual_trigger (Function) ] ┘
                                                                  │
                                                                ▼
                                                  [ 各抓取函数 (Cloud Functions) ]
                                                                  │
                                                                  ▼
                                                        [ Firestore 状态与配置表 ]
                                                                  ▼
                                                        [ 日志 + 告警 + DLQ ]
```

---

## 📌 模块职责清单（结构化）

| 模块        | 子组件                      | 主要职责                   |
| --------- | ------------------------ | ---------------------- |
| 任务入口      | Scheduler / Cloud Run 页面 | 定时或手动触发任务流程            |
| 抓取函数      | 多个 Cloud Functions       | 抓取数据、结构化写入状态           |
| Pub/Sub   | 消息队列与 DLQ                | 异步任务解耦、失败收敛            |
| Firestore | config / state           | 存储任务配置与 traceable 状态记录 |
| 可观测性      | Logging / Monitoring     | 结构化日志、失败告警、trace追踪     |
| 前端展示      | Cloud Run 页面             | 展示当前配置与运行状态，可能添加手动触发入口 |

---

## 📌 架构决策原则

* **GCP-only 架构**：移除 Vercel、Cloudflare 等依赖，统一于 Google Cloud 平台内部部署与托管
* **最小维护负担**：Serverless + 可观测性 + 命名规范 + Terraform 保证高可维护性
* **全事件驱动闭环**：任务执行、配置变更、错误处理均通过事件流触发与追踪
* **清晰职责拆分**：每个 Cloud Function 单一职责、幂等设计、独立部署
* **AI 协作生成标准化文档**：所有架构文档支持 AI 自动生成与更新（通过结构清晰 + 元信息）

---

## ✅ 下一步文档链接

* 📄 [`ns-technical-design.md`](./ns-technical-design.md)：事件机制、trace 流程、幂等逻辑详细说明
* 📄 [`ns-deployment-guide.md`](./ns-deployment-guide.md)：函数部署、环境变量与前端部署说明
* 📄 [`ns-security-policy.md`](./ns-security-policy.md)：服务账号权限、日志脱敏与 IAM 策略

---

*本项目由架构师主导，AI 全程协作生成设计、文档与代码，体现“人主导 / AI 辅助”的现代开发模式。*
