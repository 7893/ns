# NS - NASA Data System

极简化的NASA数据收集系统，基于单函数统一架构。

## 架构

- **1个函数**: `ns-func-unified` - 处理所有NASA API
- **1个Topic**: `ns-topic-unified` - 统一消息队列  
- **3个调度器**: 每日/每小时/每周自动收集
- **12个数据源**: APOD, 小行星, DONKI, EONET, EPIC, 火星照片, 图像库, 系外行星, 基因实验室, 技术组合, 技术转移, 地球图像

## 快速开始

```bash
# 设置环境
export NASA_API_KEY="your-key"

# 部署
./scripts/deploy.sh

# 监控
gcloud functions logs read ns-func-unified --region=us-central1
```

## 手动触发

```bash
# 触发每日收集
gcloud pubsub topics publish ns-topic-unified --message='{"schedule_type": "daily"}'

# 触发单个数据源
gcloud pubsub topics publish ns-topic-unified --attribute="source=apod"
```

## 数据存储

所有数据保存在 `gs://ns-data-2025/` 按以下结构组织：
```
{source}/{year}/{month}/{day}/{timestamp}.json
```
