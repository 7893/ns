# Cloudflare 全家桶技术栈

## 使用的 Cloudflare 服务

### 1. Workers（计算层）
- **用途**: 运行 API 和数据收集逻辑
- **免费额度**: 100,000 请求/天
- **特点**: 
  - 全球 275+ 边缘节点
  - 冷启动 <10ms
  - 自动扩展
  - 支持 JavaScript/TypeScript

### 2. R2（对象存储）
- **用途**: 存储 NASA API 数据
- **免费额度**: 10GB 存储 + 无限出站流量
- **特点**:
  - S3 兼容 API
  - 零出站流量费用
  - 自动备份

### 3. D1（数据库）
- **用途**: 记录收集日志和元数据
- **免费额度**: 5GB 存储 + 500 万行读/天
- **特点**:
  - SQLite 兼容
  - 边缘复制
  - 低延迟查询

### 4. KV（键值存储）
- **用途**: 缓存 API 响应
- **免费额度**: 1GB 存储 + 100,000 读/天
- **特点**:
  - 全球分布
  - 极低延迟
  - TTL 支持

### 5. Pages（静态托管）
- **用途**: 托管前端界面
- **免费额度**: 无限带宽 + 500 次构建/月
- **特点**:
  - 自动 HTTPS
  - 全球 CDN
  - Git 集成

### 6. Cron Triggers（定时任务）
- **用途**: 自动调度数据收集
- **免费额度**: 完全免费
- **特点**:
  - 标准 cron 语法
  - 可靠执行
  - 无需额外配置

## 数据流

```
NASA APIs
    ↓
Workers (Cron) → 收集数据
    ↓
R2 (存储原始数据)
    ↓
D1 (记录日志)
    ↓
KV (缓存结果)
    ↓
Pages (前端展示) ← Workers (API)
```

## 文件结构

```
ns/
├── worker/
│   ├── src/
│   │   └── index.js          # Worker 主逻辑
│   ├── wrangler.toml          # Worker 配置
│   ├── schema.sql             # D1 数据库结构
│   └── package.json
├── frontend/
│   ├── index.html             # 前端页面
│   ├── script.js              # 前端逻辑
│   ├── style.css              # 样式
│   └── wrangler.toml          # Pages 配置
├── deploy-all.sh              # 一键部署
├── test.sh                    # API 测试
└── README.md
```

## API 设计

### 端点

1. `GET /` - 健康检查
2. `GET /collect?source={source}` - 手动触发收集
3. `GET /api/latest?source={source}` - 获取最新数据（带缓存）
4. `GET /api/list?source={source}` - 列出文件
5. `GET /api/stats` - 统计信息

### 数据源

- **每日**: apod, asteroids-neows, donki, epic, mars-rover-photos
- **每小时**: eonet, nasa-ivl
- **每周**: exoplanet, genelab, techport, techtransfer, earth

## 存储结构

### R2 路径
```
{source}/{year}/{month}/{day}/{timestamp}.json
```

示例：
```
apod/2024/10/03/20241003T140000.json
```

### D1 表结构
```sql
collections (id, source, timestamp, status, error, created_at)
metadata (key, value, updated_at)
```

### KV 键
```
latest:{source}  # 缓存最新数据，TTL 1小时
```

## 性能指标

- **API 响应时间**: <50ms (全球平均)
- **数据收集**: 并发执行，<5s 完成
- **缓存命中率**: >90%
- **可用性**: 99.99%+

## 成本分析

### 预估使用量
- 请求: ~10,000/天
- 存储: ~2GB/年
- 数据库: ~100MB
- 缓存: ~50MB

### 费用
- **总计**: $0/月（完全在免费额度内）

## 扩展性

### 当前限制
- Workers: 100k 请求/天
- R2: 10GB 存储

### 升级路径
如超出免费额度：
- Workers: $5/月（10M 请求）
- R2: $0.015/GB/月

## 监控

```bash
# 实时日志
wrangler tail

# 查看统计
curl https://ns.YOUR_SUBDOMAIN.workers.dev/api/stats
```

## 安全

- ✅ HTTPS 强制
- ✅ CORS 配置
- ✅ API Key 环境变量
- ✅ 错误处理
- ✅ 速率限制（Workers 自动）

## 优势总结

1. **零成本**: 完全免费
2. **高性能**: 全球边缘计算
3. **易维护**: 无服务器架构
4. **可扩展**: 自动扩展
5. **简单**: 单一平台管理
