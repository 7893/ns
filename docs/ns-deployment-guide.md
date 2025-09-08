# NS 部署与执行指引（ns-deployment-guide.md）

**文档ID**：ns-deployment-guide
**最后更新时间**：2025-09-04
**维护者**：T o（总架构师） + AI 协作支持

---

## 🎯 文档目的

本指南提供完整的部署流程与执行建议，适用于开发者首次部署、环境重建或后续维护。

---

## 🧱 部署环境要求

| 项目       | 要求                                                         |
| -------- | ---------------------------------------------------------- |
| 操作系统     | Ubuntu Server / macOS / WSL 均可                             |
| 工具链管理    | 使用 `asdf` 管理 CLI 工具版本                                      |
| CLI 工具版本 | Terraform >= 1.13.x、gcloud >= 536.x、Python >= 3.11         |
| 权限要求     | 当前用户已绑定 GCP Billing Viewer / IAM Admin / Project Editor 权限 |

---

## ⚙️ 本地初始化流程

### 1. 克隆项目与安装依赖

```bash
# 克隆项目
git clone git@github.com:yourname/ns-project.git
cd ns-project

# 安装 asdf 工具（如尚未安装）
brew install asdf  # 或手动安装

# 安装工具版本
asdf install
```

### 2. 配置变量

创建 `terraform.tfvars` 文件：

```hcl
gcp_project_id = "ns-dev"
region         = "us-central1"
nasa_api_key   = "..."
deployer_sa_email = "8172...@developer.gserviceaccount.com"
```

建议将 `.tfvars` 添加到 `.gitignore`，避免泄露敏感信息。

---

## 🚀 Terraform 部署流程

### 1. 初始化 Terraform 工作目录

```bash
cd infra/gcp
terraform init
```

### 2. 检查计划（推荐每次先执行）

```bash
terraform plan -var-file=terraform.tfvars
```

### 3. 应用更改（部署资源）

```bash
terraform apply -var-file=terraform.tfvars
```

### 4. 验证状态

确认以下资源已成功创建：

* GCS Bucket（Terraform backend 与中间存储）
* Pub/Sub Topics / Subscriptions
* Firestore Collections：`job_config`, `job_status`
* Cloud Functions（部署成功）
* Cloud Run 页面（访问 URL 成功）

---

## 🔄 函数更新流程

修改函数代码（如 `apps/apod`）后执行：

```bash
cd infra/gcp
terraform apply -target=google_cloudfunctions2_function.func_apod_daily -var-file=terraform.tfvars
```

或使用 `gcloud deploy` 手动部署（若未使用 Terraform 管理函数代码）。

---

## 🌐 前端 Cloud Run 页面部署流程

前端页面为纯 HTML/JS 静态文件，部署方式：

```bash
cd frontend
gcloud run deploy ns-dashboard \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --project=ns-dev
```

部署成功后将获得一个 HTTPS URL（如 `https://ns-dashboard-xxx.a.run.app`）。

---

## 🧰 Firestore 数据初始化指引

首次部署完成后需初始化 `job_config`：

可手动通过 Firebase 控制台创建文档，或使用 Python 脚本：

```bash
python scripts/init_config.py
```

脚本会向 `job_config` 写入初始任务配置（已支持 APOD、NeoWs、Earth 等）

---

## 🧪 本地测试建议

* 所有函数支持本地测试（通过模拟 Pub/Sub 消息触发）
* 推荐使用 `scripts/test_*.py` 进行参数化测试
* trace\_id 支持日志贯通，可通过 Logging 查询追踪

---

## 📦 配套部署脚本清单

| 路径                       | 脚本用途                |
| ------------------------ | ------------------- |
| `scripts/init_config.py` | 初始化 Firestore 配置文档  |
| `scripts/deploy_one.sh`  | 手动部署单个函数            |
| `scripts/test_pubsub.py` | 本地模拟 Pub/Sub 消息触发函数 |

---

## ✅ 配套文档

* [`ns-project-checklist.md`](./ns-project-checklist.md) – 任务追踪与部署进度总览
* [`ns-resource-inventory.md`](./ns-resource-inventory.md) – 所有资源结构与权限说明
* [`ns-technical-design.md`](./ns-technical-design.md) – 各函数与交互设计说明
* [`ns-security-policy.md`](./ns-security-policy.md) – 权限控制与安全措施详解
