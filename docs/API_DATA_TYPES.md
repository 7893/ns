# NASA API 数据类型分析

## 📊 数据源分类

### 1. JSON 元数据（只返回 JSON）

| 数据源 | 返回内容 | 是否包含图片 URL |
|--------|---------|----------------|
| **apod** | JSON 元数据 + 图片 URL | ✅ `url`, `hdurl` |
| **asteroids-neows** | JSON 数据 | ❌ 纯数据 |
| **donki** | JSON 数据 | ❌ 纯数据 |
| **eonet** | JSON 数据 | ❌ 纯数据 |
| **epic** | JSON 元数据 + 图片 URL | ✅ `image` 字段 |
| **mars-rover-photos** | JSON 元数据 + 图片 URL | ✅ `img_src` |
| **nasa-ivl** | JSON 元数据 + 图片 URL | ✅ `links[].href` |
| **exoplanet** | JSON 数据 | ❌ 纯数据 |
| **genelab** | JSON 数据 | ❌ 纯数据 |
| **techport** | JSON 数据 | ❌ 纯数据 |
| **techtransfer** | JSON 数据 | ❌ 纯数据 |
| **earth** | **PNG 图片** | ⚠️ 直接返回图片 |

### 2. 问题识别

#### ⚠️ Earth API 返回图片而非 JSON

**当前问题：**
```javascript
// Earth API 返回 image/png，不是 JSON
const data = contentType.includes("application/json") 
  ? await response.json()
  : { raw_content: (await response.text()).slice(0, 1000) };
```

**Earth API 响应：**
- Content-Type: `image/png`
- 返回二进制图片数据
- 当前代码会尝试 `text()` 然后截断，**错误！**

#### ⚠️ 图片 URL 未下载

**当前问题：**
- APOD, EPIC, Mars Rover Photos, NASA IVL 返回图片 URL
- 我们只保存了 JSON 元数据
- **没有下载实际图片**

## 🔧 需要修复的问题

### 1. Earth API（高优先级）

**当前行为：**
```javascript
// ❌ 错误：尝试将二进制图片转为文本
{ raw_content: (await response.text()).slice(0, 1000) }
```

**应该：**
```javascript
// ✅ 正确：保存二进制图片到 R2
const imageBuffer = await response.arrayBuffer();
await env.NS_DATA.put(key, imageBuffer, {
  httpMetadata: { contentType: "image/png" }
});
```

### 2. 图片 URL 处理（可选）

**选项 A：只保存元数据（当前）**
- ✅ 简单，快速
- ✅ 存储空间小
- ❌ 需要二次请求获取图片
- ❌ 图片可能失效

**选项 B：下载并保存图片**
- ✅ 完整数据
- ✅ 永久保存
- ❌ 存储空间大
- ❌ 下载时间长
- ❌ 可能超出免费额度

**推荐：选项 A（只保存元数据）**

## 📝 修复方案

### 方案 1：区分数据类型（推荐）

```javascript
const NASA_CONFIGS = {
  // ... 其他配置
  earth: { 
    url: "https://api.nasa.gov/planetary/earth/imagery", 
    params: { api_key: "NASA_API_KEY", lon: -95.33, lat: 29.78, date: "WEEK_AGO", dim: 0.15 },
    type: "image" // 标记为图片类型
  }
};

async function collectData(source, env) {
  const config = NASA_CONFIGS[source];
  const response = await fetch(url.toString(), { signal: AbortSignal.timeout(60000) });
  
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  
  let data, contentType;
  
  if (config.type === "image") {
    // 处理图片
    const imageBuffer = await response.arrayBuffer();
    contentType = response.headers.get("content-type");
    await saveImageData(source, imageBuffer, contentType, env);
  } else {
    // 处理 JSON
    const contentTypeHeader = response.headers.get("content-type") || "";
    data = contentTypeHeader.includes("application/json") 
      ? await response.json()
      : { raw_content: await response.text() };
    await saveData(source, data, env);
  }
}
```

### 方案 2：自动检测（简单）

```javascript
const contentType = response.headers.get("content-type") || "";

if (contentType.includes("image/")) {
  // 图片
  const imageBuffer = await response.arrayBuffer();
  await saveImageData(source, imageBuffer, contentType, env);
} else if (contentType.includes("application/json")) {
  // JSON
  const data = await response.json();
  await saveData(source, data, env);
} else {
  // 其他文本
  const data = { raw_content: await response.text() };
  await saveData(source, data, env);
}
```

## 🎯 推荐实现

**采用方案 2（自动检测）+ 只保存元数据**

理由：
1. ✅ 简单，无需配置
2. ✅ 自动适应所有类型
3. ✅ Earth API 正确保存图片
4. ✅ 其他 API 保存 JSON 元数据（含图片 URL）
5. ✅ 存储空间可控

## 📊 存储空间估算

### 当前方案（只保存元数据）
- JSON 平均大小：10-50KB
- 每月数据：754 次 × 30KB = 22MB
- **年存储：264MB** ✅

### 如果下载所有图片
- 图片平均大小：500KB-2MB
- APOD: 1 次/天 × 1MB = 30MB/月
- EPIC: 1 次/天 × 10 张 × 500KB = 150MB/月
- Mars: 1 次/天 × 20 张 × 500KB = 300MB/月
- Earth: 1 次/周 × 1MB = 4MB/月
- **月存储：~500MB** ⚠️
- **年存储：~6GB** ⚠️

## ✅ 结论

1. **立即修复 Earth API**：保存图片而非文本
2. **保持当前策略**：其他 API 只保存 JSON 元数据
3. **未来扩展**：如需要，可选择性下载特定图片

## 🔗 相关 API 文档

- APOD: https://api.nasa.gov/planetary/apod
- Earth Imagery: https://api.nasa.gov/planetary/earth/imagery
- EPIC: https://api.nasa.gov/EPIC/api/natural/images
- Mars Rover: https://api.nasa.gov/mars-photos/api/v1/rovers
