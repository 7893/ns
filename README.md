# NS - NASA Data System

极简化的 NASA 数据收集系统，基于 Cloudflare 全家桶（100% 免费套餐）。

## ✨ 特性

- 🚀 **零成本**: 完全使用 Cloudflare 免费套餐
- 🌍 **全球 CDN**: 275+ 边缘节点，<50ms 延迟
- ⚡ **高性能**: Workers 冷启动 <10ms
- 📦 **12 数据源**: APOD, 小行星, DONKI, EPIC, 火星照片等
- ⏰ **自动调度**: 每日/每小时/每周自动收集
- 🔄 **实时 API**: RESTful API + 缓存层
- 📊 **数据持久化**: R2 + D1 + KV 三层存储
- 🎨 **单 Worker**: API + 前端统一托管

## 🏗️ 架构

```
┌─────────────┐
│  NASA APIs  │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────┐
│  Cloudflare Worker (边缘计算)            │
│  • API 端点                              │
│  • 前端托管                              │
│  • Cron Triggers (自动调度)              │
│  • 数据收集逻辑                          │
└──┬────────┬────────┬─────────────────────┘
   │        │        │
   ▼        ▼        ▼
┌──────┐ ┌────┐  ┌────────┐
│  R2  │ │ D1 │  │   KV   │
│ 10GB │ │ 5GB│  │  1GB   │
│ 存储 │ │数据│  │ 缓存   │
└──────┘ └────┘  └────────┘
```

## 🚀 快速开始

```bash
# 1. 安装依赖
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 一键部署
./deploy-all.sh
```

访问: `https://ns.YOUR_SUBDOMAIN.workers.dev`

## 📦 Cloudflare 服务

| 服务 | 用途 | 免费额度 |
|------|------|---------|
| Workers | API + 前端 + 数据收集 | 100k 请求/天 |
| R2 | 数据存储 | 10GB + 无限出站 |
| D1 | 日志数据库 | 5GB + 500万行读/天 |
| KV | 缓存层 | 1GB + 100k 读/天 |
| Cron | 定时任务 | 免费 |

## 📡 API 端点

```bash
# 前端界面
GET /

# 手动触发收集
GET /collect?source=apod

# 获取最新数据（带缓存）
GET /api/latest?source=apod

# 列出文件
GET /api/list?source=apod

# 统计信息
GET /api/stats
```

## 🛰️ 数据源

**每日 (00:00 UTC)**
- APOD, Asteroids NeoWs, DONKI, EPIC, Mars Rover Photos

**每小时**
- EONET, NASA Image Library

**每周 (周日 00:00 UTC)**
- Exoplanet, GeneLab, TechPort, Tech Transfer, Earth Imagery

## 📂 项目结构

```
ns/
├── worker/              # Cloudflare Worker
│   ├── src/index.js    # 主逻辑 (API + 前端)
│   ├── wrangler.toml   # 配置
│   └── schema.sql      # D1 数据库结构
├── frontend/            # 前端源码（已内联到 Worker）
├── docs/                # 文档
├── deploy-all.sh        # 一键部署
└── test.sh              # API 测试
```

## 💰 成本

**完全免费！** 所有服务都在 Cloudflare 免费套餐内。

## 📝 许可

MIT



