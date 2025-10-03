# Cloudflare 部署指南

## 前置要求

1. Cloudflare 账号（免费）
2. NASA API Key（免费）：https://api.nasa.gov
3. Node.js 18+

## 步骤

### 1. 安装 Wrangler CLI

```bash
npm install -g wrangler
wrangler login
```

### 2. 创建 Cloudflare 资源

```bash
# R2 存储桶
wrangler r2 bucket create ns-data

# D1 数据库
wrangler d1 create ns-db
# 记录返回的 database_id

# KV 命名空间
wrangler kv:namespace create CACHE
# 记录返回的 id
```

### 3. 配置 Worker

编辑 `worker/wrangler.toml`，替换：
- `YOUR_D1_DATABASE_ID` → 步骤2的 database_id
- `YOUR_KV_NAMESPACE_ID` → 步骤2的 KV id
- `NASA_API_KEY` → 你的 NASA API Key

### 4. 初始化数据库

```bash
cd worker
wrangler d1 execute ns-db --file=schema.sql
```

### 5. 部署

```bash
cd worker
npm install
wrangler deploy
```

### 6. 验证

访问：`https://ns.YOUR_SUBDOMAIN.workers.dev`

测试 API：
```bash
curl https://ns.YOUR_SUBDOMAIN.workers.dev/api/stats
```

## GitHub Actions（可选）

在 GitHub 仓库设置中添加 Secret：
- `CLOUDFLARE_API_TOKEN`

推送代码后自动部署。

## 免费额度

- Workers: 100,000 请求/天
- R2: 10GB 存储，无限出站流量
- KV: 1GB 存储，100,000 读/天
- D1: 5GB 存储，5,000,000 行读/天

完全够用！
