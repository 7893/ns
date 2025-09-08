# NS 项目初始化与任务追踪清单（ns-project-checklist.md）

**文档ID**：ns-project-checklist
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本清单文件用于：

1. 指导 NS 项目的初始化过程（GCP 配置、Terraform、服务账号）
2. 跟踪项目各阶段的关键任务完成情况
3. 为未来迭代提供断点续接与可追溯性基础

---

## ✅ 项目初始化任务（一次性）

| 阶段            | 操作项                                      | 是否完成 |
| ------------- | ---------------------------------------- | ---- |
| GCP 项目设置      | 创建 GCP 项目（如 ns-dev）                      | ✅    |
| Billing 设置    | 绑定结算账号并启用预算提醒                            | ✅    |
| API 启用        | 启用 GCS、Pub/Sub、Functions、Firestore 等必要服务 | ✅    |
| Firestore 初始化 | 手动创建 job\_config、job\_status 集合结构        | ✅    |
| Terraform 初始化 | 配置远程 backend，设置 provider                 | ✅    |
| 服务账号          | 创建函数运行身份，绑定 IAM 权限                       | ✅    |
| 本地工具          | 安装 asdf + terraform + gcloud CLI         | ✅    |

---

## 🔁 Terraform 管理资源任务

| 模块             | 子任务                        | 是否完成 |
| -------------- | -------------------------- | ---- |
| GCS            | 创建临时中间对象存储桶                | ✅    |
| Pub/Sub        | 定义 topics / subscriptions  | ✅    |
| Cloud Function | 部署 `func-apod-daily` 等抓取函数 | ✅    |
| Cloud Run      | 部署前端配置与状态接口                | ✅    |
| IAM            | 为函数绑定合适权限                  | ✅    |
| Logging Sink   | （可选）导出日志至 BigQuery / GCS   | ⏳    |
| Firestore IAM  | 绑定函数对 job\_config 的读权限     | ✅    |

---

## 🧠 抓取函数开发任务

| 抓取类型              | 状态    | 说明            |
| ----------------- | ----- | ------------- |
| APOD Daily        | ✅ 已完成 | NASA 天文图像日更接口 |
| Earth Assets      | ✅ 已完成 | 支持用户参数配置      |
| NeoWs Feed        | ✅ 已完成 | 接入任务配置结构体     |
| TechTransfer      | ⏳ 开发中 | 支持分页/重试策略     |
| Exoplanet Archive | ⏳ 开发中 | 长列表处理模式       |

---

## 🌐 前端任务

| 模块     | 状态                     | 说明        |
| ------ | ---------------------- | --------- |
| 前端页面   | ✅ 已部署                  | 显示任务状态与配置 |
| 配置修改能力 | ❌ 暂不实现                 | 当前仅为展示用途  |
| 页面托管   | ✅ 使用 Cloud Run 生成的 URL |           |

---

## 🔒 安全与权限任务

| 模块           | 子任务                           | 是否完成 |
| ------------ | ----------------------------- | ---- |
| 服务账号权限       | 最小权限绑定                        | ✅    |
| 环境变量管理       | 不写死机密信息，使用 Terraform 管理       | ✅    |
| Firestore 限权 | job\_config 只读，job\_status 可写 | ✅    |
| 日志权限         | 限制 Cloud Logging Viewer 范围    | ✅    |

---

## 📦 可观测性部署任务

| 模块           | 子任务                   | 是否完成 |
| ------------ | --------------------- | ---- |
| 日志结构统一       | 全部函数输出结构化 JSON        | ✅    |
| trace\_id 贯通 | Pub/Sub → 函数 → 日志     | ✅    |
| Pub/Sub 死信队列 | 配置 DLQ topic 与订阅      | ✅    |
| 错误告警         | 设置 basic alert policy | ⏳    |
| 日志导出         | 导出到 BigQuery 或 GCS    | ⏳    |

---

## 🧰 工程与维护自动化

| 模块              | 子任务                   | 是否完成 |
| --------------- | --------------------- | ---- |
| GitHub 仓库       | 已私有托管                 | ✅    |
| GitHub Actions  | 自动部署 Terraform 计划（可选） | ❌    |
| Firestore 初始化脚本 | 提供便捷创建配置结构工具          | ✅    |
| 配置热更新支持         | 发布 config\_updated 事件 | ⏳    |
| 文档生成自动化         | Markdown 结构生成机制       | ✅    |

---

## ✅ 进展评估

* 当前系统已具备稳定抓取、配置驱动、状态查看、日志追踪能力
* 尚未实现：自动告警、配置变更事件驱动、CI/CD 自动部署

---

## 🧭 推荐配套文档

* [`ns-technical-design.md`](./ns-technical-design.md) – 各模块技术实现结构
* [`ns-resource-inventory.md`](./ns-resource-inventory.md) – GCP 资源及管理方式
* [`ns-observability-guidelines.md`](./ns-observability-guidelines.md) – 日志与告警机制
* [`ns-security-policy.md`](./ns-security-policy.md) – 最小权限与 Secrets 策略
* [`ns-deployment-guide.md`](./ns-deployment-guide.md) – Terraform 与服务部署指引
