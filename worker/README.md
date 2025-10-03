# NS - Cloudflare Workers 版本

极简化的NASA数据收集系统，运行在 Cloudflare Workers。

## 架构

- **1个 Worker**: 处理所有NASA API
- **1个 R2 Bucket**: 统一数据存储
- **3个 Cron Triggers**: 每日/每小时/每周自动收集
- **12个数据源**: APOD, 小行星, DONKI, EONET, EPIC, 火星照片, 图像库, 系外行星, 基因实验室, 技术组合, 技术转移, 地球图像

## 快速开始

### 前置要求

1. 安装 Node.js (v18+)
2. 安装 Wrangler CLI: `npm install -g wrangler`
3. 登录 Cloudflare: `wrangler login`

### 部署

```bash
cd worker
./deploy.sh
```

### 手动触发

```bash
# 触发单个数据源
curl "https://ns.<your-subdomain>.workers.dev/collect?source=apod"
```

### 本地开发

```bash
npm run dev
```

### 查看日志

```bash
npm run tail
```

## 数据存储

所有数据保存在 R2 bucket `ns-data` 按以下结构组织：
```
{source}/{year}/{month}/{day}/{timestamp}.json
```

## 调度配置

- **每日 (00:00 UTC)**: apod, asteroids-neows, donki, epic, mars-rover-photos
- **每小时**: eonet, nasa-ivl
- **每周 (周日 00:00 UTC)**: exoplanet, genelab, techport, techtransfer, earth

## 配置

编辑 `wrangler.toml` 修改：
- NASA API Key
- Cron 调度时间
- R2 bucket 名称
