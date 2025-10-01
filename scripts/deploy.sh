#!/bin/bash
# NS - 统一部署脚本

set -e

echo "🚀 Deploying NS - NASA Data System"

# 检查环境
if [ -z "$NASA_API_KEY" ]; then
    echo "❌ NASA_API_KEY not set"
    exit 1
fi

# 部署基础设施
cd infra/gcp
terraform init
terraform plan -var="nasa_api_key=$NASA_API_KEY"
terraform apply -var="nasa_api_key=$NASA_API_KEY" -auto-approve

echo "✅ Deployment complete"
echo "📊 Monitor: gcloud functions logs read ns-func-unified --region=us-central1"
