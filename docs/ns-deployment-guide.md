# NS 部署与执行指引 (ns-deployment-guide.md)

**最后更新时间**：2025-09-09
**维护者**：T o（总架构师） + AI 协同支持
---
## 🧱 Terraform 文件结构
本项目的 Terraform 代码位于 `infra/gcp/` 目录，并已按资源类型分解为多个 `.tf` 文件，职责清晰：
- `main.tf`: Provider 配置入口
- `locals.tf`: 项目变量配置
- `pubsub.tf`: Pub/Sub 主题定义
- `gcs.tf`: GCS 存储桶与对象定义
- `functions.tf`: Cloud Functions 定义
- `scheduler.tf`: Cloud Scheduler 定义

---
## 🚀 Terraform 部署流程

### 1. 认证 (一次性)
确保已通过 gcloud 登录并设置好应用默认凭证：
`gcloud auth application-default login`

### 2. 初始化 (首次或变更Provider时)
进入 `infra/gcp` 目录，执行：
`terraform init`

### 3. 部署或更新
`terraform apply`

### 4. 销毁
`terraform destroy`
---
[...文档其余部分可根据需要补充...]