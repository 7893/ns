# GCP → Cloudflare 迁移对比

## 架构变化

| 组件 | GCP (旧) | Cloudflare (新) | 优势 |
|------|---------|----------------|------|
| 计算 | Cloud Functions | Workers | 更快冷启动，全球边缘 |
| 存储 | Cloud Storage | R2 | 免费出站流量 |
| 数据库 | Firestore | D1 (SQLite) | 更简单，免费额度大 |
| 缓存 | Memorystore | KV | 完全免费 |
| 前端 | Cloud Run | Pages | 无限带宽 |
| 调度 | Cloud Scheduler | Cron Triggers | 内置免费 |

## 成本对比

### GCP（旧方案）
- Cloud Functions: $0.40/百万次请求
- Cloud Storage: $0.026/GB/月 + 出站流量费
- Firestore: $0.18/GB/月
- Cloud Scheduler: $0.10/作业/月
- **预估月成本**: $10-50

### Cloudflare（新方案）
- Workers: 100k 请求/天 **免费**
- R2: 10GB 存储 + 无限出站 **免费**
- D1: 5GB 数据库 **免费**
- KV: 1GB 缓存 **免费**
- Pages: 无限带宽 **免费**
- Cron: 内置 **免费**
- **月成本**: $0

## 功能对比

| 功能 | GCP | Cloudflare | 状态 |
|------|-----|-----------|------|
| 数据收集 | ✅ | ✅ | 完全迁移 |
| 自动调度 | ✅ | ✅ | 完全迁移 |
| API 接口 | ✅ | ✅ | 增强 |
| 数据存储 | ✅ | ✅ | 完全迁移 |
| 缓存层 | ❌ | ✅ | 新增 |
| 日志记录 | ✅ | ✅ | 完全迁移 |
| 前端托管 | ✅ | ✅ | 完全迁移 |

## 性能提升

- **冷启动**: 10-100ms (vs GCP 1-3s)
- **全球延迟**: <50ms (275+ 边缘节点)
- **出站流量**: 免费无限 (vs GCP 收费)
- **并发**: 自动扩展

## 迁移步骤

1. ✅ 创建 Cloudflare 账号
2. ✅ 部署 Worker（替代 Cloud Functions）
3. ✅ 创建 R2 bucket（替代 Cloud Storage）
4. ✅ 配置 Cron Triggers（替代 Cloud Scheduler）
5. ✅ 部署 Pages（替代 Cloud Run）
6. ✅ 配置 D1 数据库（替代 Firestore）
7. ✅ 配置 KV 缓存（新增）
8. ⏳ 数据迁移（如需要）
9. ⏳ DNS 切换
10. ⏳ 关闭 GCP 资源

## 代码变化

### 旧代码（GCP Cloud Functions）
```python
# Python + Flask
from google.cloud import storage
import functions_framework

@functions_framework.http
def collect_data(request):
    # 处理逻辑
    pass
```

### 新代码（Cloudflare Workers）
```javascript
// JavaScript + Workers API
export default {
  async fetch(request, env) {
    // 处理逻辑
  }
}
```

## 数据迁移

如需从 GCP Cloud Storage 迁移数据到 R2：

```bash
# 使用 rclone
rclone sync gcs:old-bucket r2:ns-data
```

## 回滚计划

保留 GCP 资源 30 天，确保 Cloudflare 稳定运行后再删除。

## 总结

- ✅ 100% 免费
- ✅ 性能更好
- ✅ 更简单
- ✅ 全球 CDN
- ✅ 无需信用卡（免费套餐）
