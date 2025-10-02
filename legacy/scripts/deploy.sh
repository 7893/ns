#!/bin/bash
# NS - 完整IaC部署脚本

set -e

echo "🚀 NS - NASA Data System 完整部署"
echo "区域: us-central1 (美国中部)"
echo "时区: Asia/Hong_Kong (香港时区)"

# 检查环境
if [ -z "$NASA_API_KEY" ]; then
    echo "❌ NASA_API_KEY环境变量未设置"
    exit 1
fi

# 进入terraform目录
cd infra/gcp

# 初始化terraform
echo "📦 初始化Terraform..."
terraform init

# 验证配置
echo "🔍 验证Terraform配置..."
terraform validate

# 生成执行计划
echo "📋 生成执行计划..."
terraform plan -var="nasa_api_key=$NASA_API_KEY"

# 应用配置
echo "🚀 部署基础设施..."
terraform apply -var="nasa_api_key=$NASA_API_KEY" -auto-approve

echo "✅ 部署完成！"
echo ""
echo "📊 系统信息:"
echo "- 函数: ns-func-unified"
echo "- Topic: ns-topic-unified" 
echo "- 调度器: 每日/每小时/每周 (香港时区)"
echo "- 区域: us-central1"
echo ""
echo "🔍 监控命令:"
echo "gcloud functions logs read ns-func-unified --region=us-central1"
