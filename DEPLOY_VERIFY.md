# 部署验证指南

## ✅ 代码已推送

提交：`05b75e5`
分支：`main`

## 🔍 验证步骤

### 1. 检查 GitHub Actions

访问：https://github.com/7893/ns/actions

**预期结果：**
- ✅ Workflow "Deploy" 自动触发
- ✅ 状态显示为运行中或成功
- ❌ 如果失败，查看日志

### 2. 查看部署日志

点击最新的 workflow run → 查看 "Deploy Worker" 步骤

**成功标志：**
```
✨ Success! Uploaded to https://ns.YOUR_SUBDOMAIN.workers.dev
```

### 3. 验证 Worker 部署

```bash
# 替换为你的实际 URL
curl https://ns.YOUR_SUBDOMAIN.workers.dev/

# 预期返回：前端 HTML
```

### 4. 测试 API

```bash
# 统计信息
curl https://ns.YOUR_SUBDOMAIN.workers.dev/api/stats

# 手动触发收集
curl https://ns.YOUR_SUBDOMAIN.workers.dev/collect?source=apod

# 获取最新数据
curl https://ns.YOUR_SUBDOMAIN.workers.dev/api/latest?source=apod
```

## 🚨 常见问题

### Workflow 失败

**检查：**
1. GitHub Secrets 是否正确配置
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`（可选）

2. wrangler.toml 配置
   - `YOUR_D1_DATABASE_ID` 是否替换
   - `YOUR_KV_NAMESPACE_ID` 是否替换

**解决：**
```bash
# 本地测试部署
cd worker
wrangler deploy
```

### Worker 404

**原因：**
- Worker 未部署成功
- URL 错误

**解决：**
```bash
# 查看已部署的 Workers
wrangler deployments list

# 查看 Worker 详情
wrangler whoami
```

### API 返回错误

**检查：**
1. R2 bucket 是否创建
2. D1 数据库是否创建
3. KV 命名空间是否创建

**解决：**
```bash
# 手动创建资源
./deploy-all.sh
```

## 📊 部署成功标志

- ✅ GitHub Actions 显示绿色勾
- ✅ Worker URL 可访问
- ✅ 前端界面正常显示
- ✅ API 返回正确数据
- ✅ Cron 自动执行（等待下一个调度时间）

## 🎉 下一步

1. 访问 Worker URL 查看前端
2. 运行 `./test.sh` 测试所有 API
3. 查看 Cloudflare Dashboard 监控数据
4. 等待 Cron 自动收集数据

## 📝 监控

```bash
# 实时日志
wrangler tail

# 查看最近的请求
wrangler tail --format pretty
```

## 🔗 相关链接

- GitHub Actions: https://github.com/7893/ns/actions
- Cloudflare Dashboard: https://dash.cloudflare.com
- Worker URL: https://ns.YOUR_SUBDOMAIN.workers.dev
