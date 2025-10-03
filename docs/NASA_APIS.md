# NASA API 完整列表

## 📊 总览

**总计：12 个 API**

| 类型 | 数量 | 说明 |
|------|------|------|
| JSON + 图片 | 4 | 返回 JSON 元数据 + 图片 URL |
| 直接图片 | 1 | 直接返回图片二进制 |
| 纯 JSON | 7 | 只返回 JSON 数据 |

## 📡 API 详细信息

### 1. APOD (Astronomy Picture of the Day)
- **类型**: JSON + 图片
- **返回**: JSON 元数据 + 1-2 张图片
- **调度**: 每日 00:00 UTC
- **URL**: https://api.nasa.gov/planetary/apod
- **图片字段**: `url`, `hdurl`

### 2. Asteroids NeoWs (Near Earth Object Web Service)
- **类型**: 纯 JSON
- **返回**: 近地小行星数据
- **调度**: 每日 00:00 UTC
- **URL**: https://api.nasa.gov/neo/rest/v1/feed

### 3. DONKI (Space Weather Database)
- **类型**: 纯 JSON
- **返回**: 空间天气通知
- **调度**: 每日 00:00 UTC
- **URL**: https://api.nasa.gov/DONKI/notifications

### 4. EONET (Earth Observatory Natural Event Tracker)
- **类型**: 纯 JSON
- **返回**: 地球观测自然事件
- **调度**: 每小时
- **URL**: https://eonet.gsfc.nasa.gov/api/v3/events

### 5. EPIC (Earth Polychromatic Imaging Camera)
- **类型**: JSON + 图片
- **返回**: JSON 元数据 + 5 张地球图片
- **调度**: 每日 00:00 UTC
- **URL**: https://api.nasa.gov/EPIC/api/natural/images
- **图片字段**: 构建 URL from `image` + `date`

### 6. Mars Rover Photos
- **类型**: JSON + 图片
- **返回**: JSON 元数据 + 10 张火星照片
- **调度**: 每日 00:00 UTC
- **URL**: https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos
- **图片字段**: `photos[].img_src`

### 7. NASA Image and Video Library
- **类型**: JSON + 图片
- **返回**: JSON 元数据 + 5 张图片
- **调度**: 每小时
- **URL**: https://images-api.nasa.gov/search
- **图片字段**: `collection.items[].links[].href`

### 8. Exoplanet Archive
- **类型**: 纯 JSON
- **返回**: 系外行星数据
- **调度**: 每周日 00:00 UTC
- **URL**: https://exoplanetarchive.ipac.caltech.edu/TAP/sync

### 9. GeneLab
- **类型**: 纯 JSON
- **返回**: 基因实验室数据
- **调度**: 每周日 00:00 UTC
- **URL**: https://genelab-data.ndc.nasa.gov/genelab/data/search

### 10. TechPort
- **类型**: 纯 JSON
- **返回**: 技术组合项目
- **调度**: 每周日 00:00 UTC
- **URL**: https://api.nasa.gov/techport/api/projects

### 11. Technology Transfer
- **类型**: 纯 JSON
- **返回**: 技术转移专利
- **调度**: 每周日 00:00 UTC
- **URL**: https://api.nasa.gov/techtransfer/patent

### 12. Earth Imagery
- **类型**: 直接图片
- **返回**: PNG 图片
- **调度**: 每周日 00:00 UTC
- **URL**: https://api.nasa.gov/planetary/earth/imagery

## 📅 调度统计

| 频率 | API 数量 | API 列表 |
|------|---------|---------|
| 每日 | 5 | APOD, Asteroids, DONKI, EPIC, Mars Rover |
| 每小时 | 2 | EONET, NASA IVL |
| 每周 | 5 | Exoplanet, GeneLab, TechPort, Tech Transfer, Earth |

## 📦 数据量统计

### 每次收集

| API | JSON 大小 | 图片数量 | 图片大小 | 总大小 |
|-----|----------|---------|---------|--------|
| APOD | 2KB | 1-2 | 2MB | ~2MB |
| Asteroids | 50KB | 0 | 0 | 50KB |
| DONKI | 10KB | 0 | 0 | 10KB |
| EONET | 30KB | 0 | 0 | 30KB |
| EPIC | 5KB | 5 | 2.5MB | ~2.5MB |
| Mars Rover | 100KB | 10 | 5MB | ~5MB |
| NASA IVL | 50KB | 5 | 2.5MB | ~2.5MB |
| Exoplanet | 20KB | 0 | 0 | 20KB |
| GeneLab | 30KB | 0 | 0 | 30KB |
| TechPort | 15KB | 0 | 0 | 15KB |
| Tech Transfer | 25KB | 0 | 0 | 25KB |
| Earth | 0 | 1 | 1MB | ~1MB |

### 每日总计
- JSON: ~1.7MB
- 图片: ~69.5MB
- **总计: ~71MB/天**

### 每月总计
- **~2.1GB/月**
