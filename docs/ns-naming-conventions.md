# NS 命名规范文档（ns-naming-conventions.md）

**文档ID**：ns-naming-conventions
**最后更新时间**：2025-09-08
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本规范文档用于统一 NS 项目在 GCP 各类资源、代码目录、配置键名、日志字段等方面的命名规则，确保整体工程具备一致性、可读性与可维护性。

---

## 🌐 GCP 资源命名规范

| 资源类型 | 命名规则 | 示例 |
| :--- | :--- | :--- |
| 项目名称 | `ns-[env]` | `ns-dev`, `ns-prod` |
| Cloud Function | `ns-func-[job]` | `ns-func-apod`, `ns-func-dispatcher` |
| Cloud Run 服务 | `ns-run-[name]` | `ns-run-dashboard` |
| Pub/Sub Topic | `ns-topic-[name]` | `ns-topic-job-dispatch`, `ns-topic-apod` |
| Pub/Sub Subscription| `sub-[topic]-[purpose]` | `sub-ns-topic-apod-worker` |
| Firestore 集合名 | `job_config`, `job_status`| (固定命名，不加前缀) |
| Cloud Storage Bucket| `ns-bucket-[purpose]-[env]`| `ns-bucket-source-dev` |
| Cloud Scheduler | `ns-scheduler-[frequency]`| `ns-scheduler-main-daily`|

> 所有资源命名遵循小写、短横线连接，不使用下划线、驼峰、空格。

---

## 🧩 代码与目录结构命名

### Monorepo 结构

| 类别 | 命名示例 |
| :--- | :--- |
| 项目根目录 | `ns/` |
| GCP 函数目录 | `apps/[job]/` → `apps/apod/` |
| Terraform 配置 | `infra/gcp/` |
| 公共工具函数 | `packages/ns_packages/` |
| 部署脚本 | `scripts/deploy_[target].sh` |
| 文档目录 | `docs/` |

---
[...文档其余部分保持不变...]