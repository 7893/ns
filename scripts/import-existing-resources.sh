#!/bin/bash

# 导入现有GCP资源到Terraform状态
# 这个脚本只在需要时运行，用于同步Terraform状态与实际资源

set -e

cd "$(dirname "$0")/../infra/gcp"

echo "🔄 导入现有GCP资源到Terraform状态..."

# 检查是否有NASA_API_KEY
if [ -z "$NASA_API_KEY" ]; then
    echo "❌ 请设置NASA_API_KEY环境变量"
    exit 1
fi

# 导入存储桶
echo "📦 导入存储桶..."
terraform import -var="nasa_api_key=$NASA_API_KEY" google_storage_bucket.nasa_data_storage ns-2025-data || echo "存储桶已导入或不存在"
terraform import -var="nasa_api_key=$NASA_API_KEY" google_storage_bucket.function_source_code ns-2025 || echo "源码桶已导入或不存在"

# 导入Pub/Sub主题
echo "📡 导入Pub/Sub主题..."
topics=("scheduler-triggers" "apod" "asteroids-neows" "donki" "earth" "eonet" "epic" "exoplanet" "genelab" "mars-rover-photos" "nasa-ivl" "techport" "techtransfer")

for topic in "${topics[@]}"; do
    if [ "$topic" = "scheduler-triggers" ]; then
        terraform import -var="nasa_api_key=$NASA_API_KEY" google_pubsub_topic.scheduler_triggers_topic "projects/sigma-outcome/topics/ns-topic-$topic" || echo "主题 $topic 已导入或不存在"
    else
        terraform import -var="nasa_api_key=$NASA_API_KEY" "google_pubsub_topic.worker_topics[\"$(echo $topic | sed 's/scheduler-triggers//')\"" "projects/sigma-outcome/topics/ns-topic-$topic" || echo "主题 $topic 已导入或不存在"
    fi
done

echo "✅ 资源导入完成！"
echo "💡 现在可以运行 terraform plan 检查状态同步"
