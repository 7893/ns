#!/bin/bash
set -e

echo "Deploying NS Worker to Cloudflare..."

# Install dependencies
npm install

# Create R2 bucket if not exists
wrangler r2 bucket create ns-data 2>/dev/null || echo "Bucket already exists"

# Deploy worker
wrangler deploy

echo "Deployment complete!"
echo ""
echo "Manual trigger: https://ns.<your-subdomain>.workers.dev/collect?source=apod"
