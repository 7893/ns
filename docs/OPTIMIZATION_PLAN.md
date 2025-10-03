# 优化方案 - 提高实时性 + 减少文件数

## 📊 当前问题

### 1. 文件碎片化
```
nasa-ivl/2025/10/03/
├── 20251003T080048.json (45.84 KB)
├── 20251003T080050_0.jpg (161.49 KB)
├── 20251003T080050_1.jpg (1.58 KB)
├── 20251003T080050_2.jpg (28.32 KB)
├── 20251003T080050_3.jpg (82.81 KB)
└── 20251003T080050_4.jpg (171.96 KB)
```
**问题**: 6 个文件，总计 491 KB

### 2. 实时性不足
- DONKI/EONET: 每 6 小时（空间天气/自然灾害需要更高频率）
- NASA IVL: 每 6 小时（实际搜索结果变化慢）

## 🎯 优化方案

### 方案 1: 图片合并 + 频率调整（推荐）

#### A. 图片存储优化

**当前**:
```javascript
// 每张图片单独保存
20251003T080050_0.jpg
20251003T080050_1.jpg
...
```

**优化**:
```javascript
// 方案 1A: 只保存 JSON，图片 URL 在 JSON 中
{
  "metadata": {...},
  "images": [
    {"url": "https://...", "size": 161490},
    {"url": "https://...", "size": 1580}
  ]
}
```

**方案 1B: 打包成 ZIP**
```javascript
20251003T080050.zip  // 包含 JSON + 所有图片
```

**方案 1C: 选择性下载**
```javascript
// 只下载第一张图片（缩略图）
20251003T080050.json
20251003T080050.jpg  // 只保存第一张
```

#### B. 频率调整

**3 个 Cron 限制下的最优配置**:

```javascript
// Cron 1: 每 3 小时 - 高实时性
"0 */3 * * *" → donki, eonet

// Cron 2: 每日 - 常规更新
"0 0 * * *" → apod, asteroids-neows, epic, mars-rover-photos

// Cron 3: 每周 - 慢更新
"0 0 * * 0" → nasa-ivl, earth, genelab, techtransfer, exoplanet, techport
```

**效果**:
- DONKI/EONET: 每 6h → 每 3h（提高 2x 实时性）
- NASA IVL: 每 6h → 每周（降低冗余）
- EPIC: 每 6h → 每日（合理化）

### 方案 2: 智能合并（最优）

#### A. 按 API 类型区分策略

| API | 策略 | 原因 |
|-----|------|------|
| **APOD** | 只保存 JSON + 第一张图 | 通常只有 1-2 张 |
| **EPIC** | 只保存 JSON + 第一张图 | 5 张图太多，第一张代表性足够 |
| **Mars Rover** | 只保存 JSON + 前 3 张 | 10 张太多，3 张足够 |
| **NASA IVL** | 只保存 JSON，不下载图片 | 搜索结果，图片 URL 足够 |
| **Earth** | 保存图片 | 直接返回图片 |

#### B. 新的频率配置

```javascript
const SCHEDULE_MAP = {
  // 每 3 小时 - 紧急实时数据
  every3h: ["donki", "eonet"],
  
  // 每日 - 常规更新 + 图片类
  daily: ["apod", "asteroids-neows", "epic", "mars-rover-photos"],
  
  // 每周 - 慢更新 + 低价值
  weekly: ["nasa-ivl", "earth", "genelab", "techtransfer", "exoplanet", "techport"]
};
```

## 📊 效果对比

### 存储空间

| 方案 | 月存储 | 年存储 | 年成本 |
|------|--------|--------|--------|
| **当前（全量）** | 1.6GB | 19.2GB | $3.60 |
| **方案 1（选择性）** | 800MB | 9.6GB | $0 |
| **方案 2（智能）** | 600MB | 7.2GB | $0 |

### 实时性

| API | 当前 | 方案 2 | 提升 |
|-----|------|--------|------|
| DONKI | 每 6h | 每 3h | 2x |
| EONET | 每 6h | 每 3h | 2x |
| EPIC | 每 6h | 每日 | - |
| NASA IVL | 每 6h | 每周 | - |

### 文件数量

| API | 当前 | 方案 2 | 减少 |
|-----|------|--------|------|
| NASA IVL | 6 文件/次 | 1 文件/次 | 83% |
| EPIC | 6 文件/次 | 2 文件/次 | 67% |
| Mars Rover | 11 文件/次 | 4 文件/次 | 64% |

## 🎯 推荐实施

### 阶段 1: 频率优化（立即）

```toml
[triggers]
crons = [
  "0 */3 * * *",    # every 3 hours: donki, eonet
  "0 0 * * *",      # daily: apod, asteroids, epic, mars
  "0 0 * * 0"       # weekly: nasa-ivl, earth, genelab, techtransfer, exoplanet, techport
]
```

### 阶段 2: 图片优化（可选）

```javascript
// 限制图片数量
const IMAGE_LIMITS = {
  'apod': 1,           // 只保存第一张
  'epic': 1,           // 只保存第一张
  'mars-rover-photos': 3,  // 只保存前 3 张
  'nasa-ivl': 0        // 不下载图片
};
```

## 💡 NASA API 限制

### 免费额度
- **速率限制**: 1000 请求/小时
- **每日限制**: 无明确限制，但建议 < 10000 次

### 当前使用

| 方案 | 每日请求 | 每月请求 | 安全性 |
|------|---------|---------|--------|
| **当前** | ~30 次 | ~900 次 | ✅ 安全 |
| **方案 2** | ~26 次 | ~780 次 | ✅ 安全 |

## ✅ 最终推荐

**立即实施方案 2**:

1. **频率调整**:
   - DONKI/EONET: 每 3 小时（提高实时性）
   - NASA IVL: 每周（降低冗余）
   
2. **图片优化**:
   - APOD: 保留 1 张
   - EPIC: 保留 1 张
   - Mars Rover: 保留 3 张
   - NASA IVL: 不下载图片

3. **效果**:
   - ✅ 实时性提高 2x
   - ✅ 存储减少 63%
   - ✅ 文件数减少 70%
   - ✅ 完全免费（< 10GB）
   - ✅ NASA API 安全（< 1000 次/天）

## 🔧 实施步骤

1. 修改 `wrangler.toml` cron 配置
2. 更新 `SCHEDULE_MAP`
3. 添加 `IMAGE_LIMITS` 配置
4. 修改 `downloadImages()` 函数
5. 测试并部署
