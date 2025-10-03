# 部署检查清单

## 📋 部署前检查

### 1. 账号准备
- [ ] Cloudflare 账号已创建
- [ ] NASA API Key 已获取（https://api.nasa.gov）
- [ ] GitHub 账号已连接（可选，用于 CI/CD）

### 2. 工具安装
- [ ] Node.js 18+ 已安装
- [ ] npm 已安装
- [ ] Wrangler CLI 已安装 (`npm install -g wrangler`)
- [ ] 已登录 Cloudflare (`wrangler login`)

### 3. 配置文件
- [ ] `worker/wrangler.toml` 已配置
  - [ ] NASA_API_KEY 已设置
  - [ ] D1 database_id 已填写
  - [ ] KV namespace id 已填写
- [ ] `frontend/script.js` 中 API_BASE 已更新
- [ ] `.env` 文件已创建（可选）

## 🚀 部署步骤

### 自动部署（推荐）
- [ ] 运行 `./deploy-all.sh`
- [ ] 等待部署完成
- [ ] 记录 Worker URL
- [ ] 记录 Pages URL

### 手动部署
- [ ] 创建 R2 bucket: `wrangler r2 bucket create ns-data`
- [ ] 创建 D1 数据库: `wrangler d1 create ns-db`
- [ ] 创建 KV 命名空间: `wrangler kv:namespace create CACHE`
- [ ] 更新 `worker/wrangler.toml` 中的 ID
- [ ] 初始化数据库: `wrangler d1 execute ns-db --file=schema.sql`
- [ ] 部署 Worker: `cd worker && wrangler deploy`
- [ ] 部署 Frontend: `cd frontend && npx wrangler pages deploy .`

## ✅ 部署后验证

### 1. Worker 测试
- [ ] 访问 Worker URL，返回状态 OK
- [ ] 测试 `/api/stats` 端点
- [ ] 测试 `/collect?source=apod` 手动触发
- [ ] 测试 `/api/latest?source=apod` 获取数据
- [ ] 测试 `/api/list?source=apod` 列出文件

### 2. Frontend 测试
- [ ] 访问 Pages URL
- [ ] 页面正常加载
- [ ] 数据源列表显示
- [ ] 点击数据源可查看数据

### 3. 存储验证
- [ ] R2 bucket 中有数据文件
- [ ] D1 数据库有日志记录
- [ ] KV 缓存正常工作

### 4. Cron 验证
- [ ] 等待下一个调度时间
- [ ] 检查是否自动收集数据
- [ ] 查看日志确认执行

## 🧪 测试命令

```bash
# 运行测试脚本
./test.sh

# 手动测试
WORKER_URL="https://ns.YOUR_SUBDOMAIN.workers.dev"

# 1. 状态检查
curl "$WORKER_URL/"

# 2. 统计信息
curl "$WORKER_URL/api/stats"

# 3. 手动触发
curl "$WORKER_URL/collect?source=apod"

# 4. 获取数据
curl "$WORKER_URL/api/latest?source=apod"

# 5. 列出文件
curl "$WORKER_URL/api/list?source=apod"
```

## 📊 监控检查

### 实时日志
- [ ] 运行 `wrangler tail` 查看实时日志
- [ ] 确认请求正常处理
- [ ] 确认无错误日志

### Cloudflare Dashboard
- [ ] 登录 Cloudflare Dashboard
- [ ] 查看 Workers 分析
- [ ] 查看 R2 使用量
- [ ] 查看 D1 查询统计
- [ ] 查看 KV 操作统计

## 🔧 故障排查

### Worker 部署失败
- [ ] 检查 `wrangler.toml` 配置
- [ ] 检查 API Token 权限
- [ ] 运行 `wrangler deploy --verbose`
- [ ] 查看错误日志

### R2 访问失败
- [ ] 确认 bucket 已创建
- [ ] 检查 binding 名称
- [ ] 检查权限设置

### D1 连接失败
- [ ] 确认数据库已创建
- [ ] 检查 database_id
- [ ] 运行 schema.sql 初始化

### KV 读写失败
- [ ] 确认命名空间已创建
- [ ] 检查 namespace id
- [ ] 检查 binding 名称

### API 返回错误
- [ ] 检查 NASA API Key
- [ ] 查看 Worker 日志
- [ ] 测试 NASA API 直接访问

## 🔐 安全检查

- [ ] API Key 未硬编码在代码中
- [ ] 使用环境变量存储敏感信息
- [ ] HTTPS 强制启用
- [ ] CORS 正确配置
- [ ] 错误信息不泄露敏感数据

## 📝 文档检查

- [ ] README.md 已更新
- [ ] API 文档已完善
- [ ] 部署文档已验证
- [ ] 示例代码可运行

## 🎯 性能检查

- [ ] API 响应时间 <100ms
- [ ] 缓存命中率 >80%
- [ ] 数据收集成功率 >95%
- [ ] 无内存泄漏

## 🔄 CI/CD 检查（可选）

- [ ] GitHub Actions 已配置
- [ ] CLOUDFLARE_API_TOKEN Secret 已设置
- [ ] 推送代码触发自动部署
- [ ] 部署成功通知

## 📈 使用量检查

### 免费额度
- [ ] Workers: <100k 请求/天
- [ ] R2: <10GB 存储
- [ ] D1: <5GB 数据
- [ ] KV: <1GB 存储

### 监控告警
- [ ] 设置使用量告警（可选）
- [ ] 接近限额时收到通知

## ✨ 完成标志

当以下所有项都完成时，部署成功：

- ✅ Worker 正常响应
- ✅ Frontend 可访问
- ✅ API 返回正确数据
- ✅ Cron 自动执行
- ✅ 数据正常存储
- ✅ 日志正常记录
- ✅ 缓存正常工作
- ✅ 测试全部通过

## 🎉 恭喜！

如果所有检查项都通过，你的 NS 系统已经成功部署到 Cloudflare！

下一步：
1. 监控系统运行
2. 查看收集的数据
3. 根据需要调整配置
4. 享受零成本的 NASA 数据服务！
