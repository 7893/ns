# NS 安全与权限策略（ns-security-policy.md）

**文档ID**：ns-security-policy
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本文件用于明确 NS 项目的安全控制原则，包括服务账号权限、Secrets 管理、访问控制、日志策略、Terraform 状态保护及未来增强措施。

---

## 🔐 服务账号策略

| 类型                  | 描述                                                                  | 权限绑定方式                                                              |
| ------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Cloud Function 运行账号 | 每个函数使用独立或统一服务账号（例如 `8172...-compute@developer.gserviceaccount.com`） | Terraform 绑定 `roles/pubsub.subscriber`、`roles/datastore.user` 等最小权限 |
| Cloud Run 前端账号      | 用于读取配置 / 写入状态的账号                                                    | Terraform 绑定 `roles/datastore.viewer`、`roles/datastore.user`        |
| Terraform 操作账号      | 手动执行部署时使用本地 `gcloud auth` 凭证                                        | 使用 impersonation 模式执行 Terraform                                     |

---

## 🔑 Secrets 管理

* **原则**：不在代码中写明 API 密钥、服务账号等机密信息
* **实践方式**：

  * 所有机密变量写入 Terraform `terraform.tfvars`（本地忽略提交）
  * GCP Secret Manager 暂未启用（可作为后续增强）
  * 本地脚本使用环境变量注入，如：`export NASA_API_KEY=xxx`

---

## 🚫 权限最小化实践

| 模块            | 措施                                           |
| ------------- | -------------------------------------------- |
| Pub/Sub       | 仅允许函数订阅各自的 topic，不允许跨 topic 操作               |
| Firestore     | job\_config 集合设为只读，job\_status 集合为只写（函数视图隔离） |
| Cloud Logging | 只授予函数日志写入权限，不授予查看权限（调试时手动打开）                 |
| Terraform 状态  | GCS Bucket 设置为私有 + versioning 开启，避免状态损坏      |

---

## 🛡️ 日志安全策略

* 所有日志必须结构化输出，字段中不得包含明文密钥或用户私密数据
* 日志中 `trace_id` 与 `job_id` 用于追踪，但避免写入参数详情
* Cloud Logging Sink 如启用导出，应确保目标表具有访问控制

---

## 🧰 安全辅助机制

| 机制           | 说明                                           |
| ------------ | -------------------------------------------- |
| trace\_id 链路 | 所有函数通过 Pub/Sub 自动传递 trace\_id 用于日志关联         |
| 死信队列保护       | 所有 Pub/Sub topic 配置 Dead Letter Topic 避免无限重试 |
| 文档标注         | 每个文档明确最后更新时间与责任人，避免过期内容误导操作                  |

---

## 🧭 安全策略未来增强方向

| 项目                      | 描述                            |
| ----------------------- | ----------------------------- |
| GCP Secret Manager      | 引入机密统一管理机制，减少本地配置泄露风险         |
| IAM 条件策略                | 引入基于时间/来源的 IAM 条件以限制函数访问窗口    |
| Cloud Logging Viewer 限权 | 日志查看权限仅绑定维护账号，便于审计与合规         |
| Terraform State 加密      | GCS 后端加密配置 + 自动备份机制（适合团队协作阶段） |

---

## ✅ 推荐配套文档

* [`ns-resource-inventory.md`](./ns-resource-inventory.md) – 所有资源与权限绑定清单
* [`ns-deployment-guide.md`](./ns-deployment-guide.md) – Terraform 执行身份与部署建议
* [`ns-observability-guidelines.md`](./ns-observability-guidelines.md) – 日志输出与审计实践
