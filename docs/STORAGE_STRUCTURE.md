# R2 存储结构

## 📁 目录结构

```
ns-data/
├── apod/
│   └── 2025/10/03/
│       ├── 20251003T000000.json          ← JSON 元数据
│       ├── 20251003T000000_0.jpg         ← 图片 (url)
│       └── 20251003T000000_1.jpg         ← 图片 (hdurl)
│
├── epic/
│   └── 2025/10/03/
│       ├── 20251003T000000.json          ← JSON 元数据
│       ├── 20251003T000000_0.png         ← 图片 1
│       ├── 20251003T000000_1.png         ← 图片 2
│       ├── 20251003T000000_2.png         ← 图片 3
│       ├── 20251003T000000_3.png         ← 图片 4
│       └── 20251003T000000_4.png         ← 图片 5
│
├── mars-rover-photos/
│   └── 2025/10/03/
│       ├── 20251003T000000.json          ← JSON 元数据
│       ├── 20251003T000000_0.jpg         ← 照片 1
│       ├── 20251003T000000_1.jpg         ← 照片 2
│       └── ...                           ← 最多 10 张
│
├── nasa-ivl/
│   └── 2025/10/03/
│       ├── 20251003T080000.json          ← JSON 元数据
│       ├── 20251003T080000_0.jpg         ← 图片 1
│       └── ...                           ← 最多 5 张
│
├── earth/
│   └── 2025/10/05/
│       └── 20251005T000000.png           ← 直接返回的图片
│
└── eonet/
    └── 2025/10/03/
        └── 20251003T080000.json          ← 纯 JSON 数据
```

## 📊 数据源分类

### 1. JSON + 图片下载

| 数据源 | JSON | 图片数量 | 图片来源 |
|--------|------|---------|---------|
| **apod** | ✅ | 1-2 | `url`, `hdurl` |
| **epic** | ✅ | 5 | 构建 URL |
| **mars-rover-photos** | ✅ | 10 | `photos[].img_src` |
| **nasa-ivl** | ✅ | 5 | `items[].links[].href` |

### 2. 直接图片

| 数据源 | 类型 | 说明 |
|--------|------|------|
| **earth** | PNG | API 直接返回图片 |

### 3. 纯 JSON

| 数据源 | 说明 |
|--------|------|
| **asteroids-neows** | 小行星数据 |
| **donki** | 空间天气通知 |
| **eonet** | 地球观测事件 |
| **exoplanet** | 系外行星数据 |
| **genelab** | 基因实验室数据 |
| **techport** | 技术组合 |
| **techtransfer** | 技术转移 |

## 📏 文件命名规则

### JSON 文件
```
{source}/{year}/{month}/{day}/{timestamp}.json
```

### 图片文件
```
{source}/{year}/{month}/{day}/{timestamp}_{index}.{ext}
```

### 错误文件
```
{source}/{year}/{month}/{day}/{timestamp}_error.json
```

## 💾 存储空间估算

### 每日数据量

| 类型 | 数据源 | 次数/天 | 单次大小 | 每日总计 |
|------|--------|---------|---------|---------|
| JSON | 所有 | 58 | 30KB | 1.7MB |
| 图片 | APOD | 1 | 2MB | 2MB |
| 图片 | EPIC | 1 | 2.5MB (5×500KB) | 2.5MB |
| 图片 | Mars | 1 | 5MB (10×500KB) | 5MB |
| 图片 | NASA IVL | 24 | 2.5MB (5×500KB) | 60MB |
| 图片 | Earth | 0.14 | 1MB | 0.14MB |
| **总计** | - | - | - | **~71MB/天** |

### 月度/年度估算

| 周期 | 存储量 | 说明 |
|------|--------|------|
| 每月 | ~2.1GB | 71MB × 30 天 |
| 每年 | ~25GB | 2.1GB × 12 月 |
| **超出免费额度** | ⚠️ | 免费 10GB |

## ⚠️ 存储优化建议

### 方案 1：限制图片数量（推荐）
```javascript
// 减少下载数量
case "nasa-ivl":
  data.collection.items.slice(0, 2)  // 5 → 2
  
case "mars-rover-photos":
  data.photos.slice(0, 5)  // 10 → 5
```
**节省**: ~40MB/天 → ~1.2GB/月 ✅

### 方案 2：降低图片质量
```javascript
// 使用缩略图而非原图
if (data.url) urls.push(data.url);  // 不下载 hdurl
```
**节省**: ~1MB/天

### 方案 3：定期清理旧数据
```bash
# 保留最近 3 个月数据
wrangler r2 object delete ns-data --prefix="apod/2024/"
```

### 方案 4：选择性下载
```javascript
// 只下载特定数据源的图片
const IMAGE_SOURCES = ["apod", "epic"];  // 不下载 Mars 和 NASA IVL
```
**节省**: ~65MB/天 → ~2GB/月 ✅

## 🎯 推荐配置

**当前配置（全量下载）：**
- 月存储：~2.1GB
- 年存储：~25GB
- **超出免费额度** ⚠️

**优化配置（推荐）：**
```javascript
// 减少图片数量
epic: 5 → 3 张
mars: 10 → 3 张
nasa-ivl: 5 → 1 张
```
- 月存储：~900MB
- 年存储：~10.8GB
- **接近免费额度** ⚠️

**最小配置（仅关键图片）：**
```javascript
// 只下载 APOD 和 Earth
const IMAGE_SOURCES = ["apod", "earth"];
```
- 月存储：~150MB
- 年存储：~1.8GB
- **完全在免费额度内** ✅

## 📝 查看存储使用

```bash
# 查看总文件数
wrangler r2 object list ns-data | wc -l

# 查看特定数据源
wrangler r2 object list ns-data --prefix="apod/"

# 查看今天的文件
wrangler r2 object list ns-data --prefix="apod/2025/10/03/"
```

## 🔗 访问文件

```bash
# 下载 JSON
wrangler r2 object get ns-data apod/2025/10/03/20251003T000000.json

# 下载图片
wrangler r2 object get ns-data apod/2025/10/03/20251003T000000_0.jpg
```
