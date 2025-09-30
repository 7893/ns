#!/bin/bash
# NS项目本地部署脚本

set -e

echo "🚀 开始部署NS项目基础设施..."

# 检查必要工具
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform未安装"; exit 1; }
command -v gcloud >/dev/null 2>&1 || { echo "❌ gcloud未安装"; exit 1; }

# 切换到基础设施目录
cd "$(dirname "$0")/../infra/gcp"

echo "📋 验证Terraform配置..."
terraform validate

echo "🔧 初始化Terraform..."
terraform init

echo "📊 生成执行计划..."
terraform plan -out=tfplan

echo "🎯 应用基础设施更改..."
terraform apply tfplan

echo "✅ 部署完成！"
echo "📝 查看资源: gcloud functions list --regions=us-central1"
