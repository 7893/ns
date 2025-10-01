#!/bin/bash
# 清理现有GCP资源脚本

set -e

echo "🧹 清理现有GCP资源..."

# 设置gcloud环境
export CLOUDSDK_PYTHON=/usr/bin/python3

# 删除Cloud Functions
echo "删除Cloud Functions..."
gcloud functions delete ns-func-unified --region=us-central1 --quiet 2>/dev/null || echo "函数不存在或已删除"

# 删除Cloud Scheduler Jobs
echo "删除Cloud Scheduler Jobs..."
gcloud scheduler jobs delete ns-unified-daily --location=us-central1 --quiet 2>/dev/null || echo "daily job不存在"
gcloud scheduler jobs delete ns-unified-hourly --location=us-central1 --quiet 2>/dev/null || echo "hourly job不存在"
gcloud scheduler jobs delete ns-unified-weekly --location=us-central1 --quiet 2>/dev/null || echo "weekly job不存在"

# 删除Pub/Sub Topics
echo "删除Pub/Sub Topics..."
gcloud pubsub topics delete ns-topic-unified --quiet 2>/dev/null || echo "topic不存在"

# 清理存储桶内容但保留桶（避免数据丢失）
echo "清理存储桶内容..."
gsutil -m rm -r gs://ns-2025/source/ 2>/dev/null || echo "源码目录已清空"

echo "✅ 资源清理完成"
