# 项目结构

```
ns/
├── worker/              # Cloudflare Workers 主应用
│   ├── src/
│   │   └── index.js    # Worker 入口文件
│   ├── wrangler.toml   # Cloudflare 配置
│   ├── package.json    # NPM 依赖
│   ├── deploy.sh       # 部署脚本
│   └── README.md
│
├── frontend/            # 前端界面
│   ├── index.html      # 主页面（启用硬件加速）
│   ├── style.css       # 样式（启用硬件加速）
│   ├── script.js       # 交互逻辑
│   └── README.md
│
├── docs/                # 文档
│   ├── README.md
│   └── structure.md    # 本文件
│
├── legacy/              # 旧版 GCP 实现
│   ├── apps/           # Cloud Functions
│   ├── infra/          # Terraform
│   ├── scripts/        # 部署脚本
│   └── README.md
│
├── .github/             # CI/CD
│   └── workflows/
│
├── .gitignore           # Git 忽略规则
├── .env.example         # 环境变量示例
└── README.md            # 项目说明
```

## 设计原则

1. **模块化**: 每个目录职责单一
2. **文档化**: 每个模块都有 README
3. **现代化**: 使用最新技术栈
4. **可维护**: 清晰的结构和命名
