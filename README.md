# NS - NASA数据聚合系统

基于Google Cloud Platform的NASA数据聚合系统，使用事件驱动架构自动收集和处理NASA API数据。

## 架构概览

- **Cloud Functions**: 14个函数 (1个调度器 + 13个数据收集器)
- **Pub/Sub**: 事件驱动消息传递
- **Cloud Scheduler**: 定时任务调度
- **Cloud Storage**: 代码和数据存储

## 部署方式

### 方法1: GitHub Actions (推荐)
1. 配置GitHub Secrets:
   - `GCP_SA_KEY`: GCP服务账号密钥JSON
   - `NASA_API_KEY`: NASA API密钥
2. 推送代码到main分支自动部署

### 方法2: 本地部署
```bash
# 使用部署脚本
./scripts/deploy_one.sh

# 或手动执行
cd infra/gcp
terraform init
terraform plan
terraform apply
```

## 环境要求

- Python 3.13+
- Terraform 1.13.3
- gcloud CLI

## 快速开始

```bash
# 激活虚拟环境
./activate.sh

# 安装依赖
pip install -e packages/

# 本地测试
cd apps/apod && python main.py
```

## 调度时间

- **每日**: 香港时间 08:00
- **每小时**: 香港时间每小时整点  
- **每周**: 香港时间周一 00:00

## 监控

查看函数日志:
```bash
gcloud functions logs read ns-func-apod --region=us-central1
```
