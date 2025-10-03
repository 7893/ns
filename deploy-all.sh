#!/bin/bash
set -e

echo "🚀 Deploying NS to Cloudflare..."

# 1. Create R2 bucket
echo "📦 Creating R2 bucket..."
wrangler r2 bucket create ns-data 2>/dev/null || echo "Bucket exists"

# 2. Create D1 database
echo "💾 Creating D1 database..."
DB_ID=$(wrangler d1 create ns-db --json 2>/dev/null | jq -r '.database_id' || echo "")
if [ -n "$DB_ID" ]; then
  sed -i "s/YOUR_D1_DATABASE_ID/$DB_ID/" worker/wrangler.toml
fi

# 3. Create KV namespace
echo "🗄️ Creating KV namespace..."
KV_ID=$(wrangler kv:namespace create CACHE --json 2>/dev/null | jq -r '.id' || echo "")
if [ -n "$KV_ID" ]; then
  sed -i "s/YOUR_KV_NAMESPACE_ID/$KV_ID/" worker/wrangler.toml
fi

# 4. Deploy Worker (includes frontend)
echo "⚙️ Deploying Worker..."
cd worker
npm install
wrangler deploy
cd ..

echo "✅ Deployment complete!"
echo "Access: https://ns.YOUR_SUBDOMAIN.workers.dev"

