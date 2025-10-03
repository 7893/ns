#!/bin/bash

# 测试 NS Worker API

WORKER_URL="https://ns.YOUR_SUBDOMAIN.workers.dev"

echo "🧪 Testing NS Worker..."

# 1. 状态检查
echo -e "\n1️⃣ Status check:"
curl -s "$WORKER_URL/" | jq

# 2. 统计信息
echo -e "\n2️⃣ Stats:"
curl -s "$WORKER_URL/api/stats" | jq

# 3. 手动触发收集
echo -e "\n3️⃣ Trigger collection (apod):"
curl -s "$WORKER_URL/collect?source=apod" | jq

# 4. 获取最新数据
echo -e "\n4️⃣ Get latest (apod):"
curl -s "$WORKER_URL/api/latest?source=apod" | jq

# 5. 列出文件
echo -e "\n5️⃣ List files (apod):"
curl -s "$WORKER_URL/api/list?source=apod" | jq

echo -e "\n✅ Tests complete!"
