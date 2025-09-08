# NS 资源清单与 IaC 管理边界（ns-resource-inventory.md）

**文档ID**：ns-resource-inventory
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本文件用于全面列出 NS 项目中使用的 GCP 核心资源，并明确哪些资源由 Terraform 管理，哪些资源为运行时动态创建或手动管理资源。

---

## 🗂️ GCP 资源清单

| 资源类型                   | 资源名称（示例）                               | 管理方式      | 描述                  |
| ---------------------- | -------------------------------------- | --------- | ------------------- |
| 项目                     | `ns-dev`                               | 手动创建      | GCP 项目 ID，不由 IaC 管理 |
| GCS Bucket             | `ns-temp-dev`                          | Terraform | 用于存储抓取中间对象与临时数据     |
| Pub/Sub Topic          | `topic-job-dispatch`                   | Terraform | 抓取任务调度消息队列          |
| Pub/Sub Subscription   | `sub-job-dispatch-worker`              | Terraform | 各函数的订阅通道            |
| Cloud Function         | `func-apod-daily`                      | Terraform | 每个任务类型一个函数          |
| Cloud Run 服务           | `api-config-viewer`                    | Terraform | 提供前端状态/配置接口         |
| Firestore 集合           | `job_config`, `job_status`, `failures` | 手动初始化     | 存储配置、运行状态与失败日志      |
| Cloud Logging Sink（可选） | `error-to-bq`                          | Terraform | 错误日志导出至 BigQuery    |
| BigQuery Dataset（可选）   | `ns_logs`                              | Terraform | 存储结构化日志             |

---

## ⚙️ Terraform 管理边界说明

### ✅ 完全由 Terraform 管理的资源：

* GCS Bucket
* Pub/Sub Topics 与 Subscriptions
* Cloud Functions / Cloud Run
* IAM 绑定（服务账号运行身份）
* 日志 Sink / BigQuery / Storage Logging

### ❌ 手动初始化一次的资源：

* Firestore 集合结构（运行时动态创建）
* GCP 项目本身（不可由 Terraform 创建）
* Cloud Billing 绑定与 API 启用（推荐用脚本辅助）

> 🛠️ 推荐写一个 `scripts/init_firestore_structure.sh` 脚本做初始化填充。

---

## 🔐 权限与角色绑定资源

| 资源              | 角色绑定                       | 管理方式                  |
| --------------- | -------------------------- | --------------------- |
| Service Account | IAM Policies               | Terraform             |
| Pub/Sub         | `publisher` / `subscriber` | Terraform             |
| Firestore       | `viewer` / `user`          | Terraform + GCP 控制台校验 |

---

## 🧠 管理策略与建议

* 所有 Terraform 管理资源统一存放于 `infra/gcp/` 目录
* 各函数模块按 `modules/functions/[job]/main.tf` 拆分
* 所有资源应打上 `labels = { project = "ns" }` 便于成本分析与审计
* 可选配置 `terraform import` 机制，将手动资源逐步纳入管理
* Terraform 状态建议存储在 GCS 中，便于多人协作（尽管目前为单人项目）

---

## ✅ 推荐配套文档

* [`ns-deployment-guide.md`](./ns-deployment-guide.md) – 包含 GCS 后端初始化、环境变量配置等说明
* [`ns-naming-conventions.md`](./ns-naming-conventions.md) – 所有资源命名策略来源统一定义
* [`ns-technical-design.md`](./ns-technical-design.md) – 说明资源用途与架构位置
* [`ns-security-policy.md`](./ns-security-policy.md) – 权限与角色绑定规则
