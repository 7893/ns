# NS - NASA Data System

极简化的 NASA 数据收集系统，基于 Cloudflare Workers。

## 特性

- 🚀 单个 Worker 处理所有 NASA API
- 📦 R2 存储统一数据管理
- ⏰ Cron 自动调度（每日/每小时/每周）
- 🌍 12 个 NASA 数据源
- 🎨 现代化前端界面

## 快速开始

```bash
cd worker
npm install
wrangler login
./deploy.sh
```

详见 [worker/README.md](worker/README.md)

## 项目结构

```
ns/
├── worker/          # Cloudflare Workers 主应用
├── frontend/        # 前端界面
├── docs/            # 文档
├── legacy/          # 旧版本（GCP）
└── .github/         # CI/CD
```

## 数据源

APOD, 小行星, DONKI, EONET, EPIC, 火星照片, 图像库, 系外行星, 基因实验室, 技术组合, 技术转移, 地球图像

## 许可

MIT
