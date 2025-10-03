# 快速开始 - 5 分钟部署

## 1. 准备（1分钟）

```bash
# 安装 Wrangler
npm install -g wrangler

# 登录 Cloudflare
wrangler login

# 获取 NASA API Key
# 访问: https://api.nasa.gov
```

## 2. 一键部署（3分钟）

```bash
cd /home/ubuntu/ns
./deploy-all.sh
```

脚本会自动：
- ✅ 创建 R2 bucket
- ✅ 创建 D1 数据库
- ✅ 创建 KV 命名空间
- ✅ 部署 Worker（包含前端）

## 3. 访问（1分钟）

访问: `https://ns.YOUR_SUBDOMAIN.workers.dev`

- 前端界面在根路径 `/`
- API 在 `/api/*` 路径

## 4. 测试

```bash
# 修改 test.sh 中的 URL
vim test.sh

# 运行测试
./test.sh
```

## 常用命令

```bash
# 查看实时日志
wrangler tail

# 手动触发收集
curl "https://ns.YOUR_SUBDOMAIN.workers.dev/collect?source=apod"

# 查看统计
curl "https://ns.YOUR_SUBDOMAIN.workers.dev/api/stats"

# 重新部署
cd worker && wrangler deploy
```

## 完成！

访问 Worker URL 即可看到前端界面和使用 API。

