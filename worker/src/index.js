const HTML = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NS - NASA Data System</title>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="container">
<header><h1>🚀 NS - NASA Data System</h1><p>12 个 NASA API 数据收集系统</p></header>
<main>
<section class="stats-grid">
<div class="stat-card"><h3>📊 总 API 数</h3><div id="total-apis" class="big-number">12</div></div>
<div class="stat-card"><h3>📦 总下载量</h3><div id="total-downloads" class="big-number">-</div></div>
<div class="stat-card"><h3>💾 存储使用</h3><div id="storage-used" class="big-number">-</div></div>
<div class="stat-card"><h3>⏰ 下次同步</h3><div id="next-sync" class="big-number">-</div></div>
</section>
<section class="api-list">
<h2>数据源列表</h2>
<div id="api-sources">加载中...</div>
</section>
</main>
</div>
<script src="/script.js"></script>
</body>
</html>`;

const CSS = `* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #fff; line-height: 1.6; }
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
header { text-align: center; margin-bottom: 3rem; }
header h1 { font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
header p { color: #888; font-size: 1.2rem; }
section { background: #1a1a1a; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; border: 1px solid #333; }
section h2 { margin-bottom: 1rem; color: #4ecdc4; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; background: transparent; padding: 0; }
.stat-card { background: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 1.5rem; text-align: center; }
.stat-card h3 { font-size: 0.9rem; color: #888; margin-bottom: 0.5rem; }
.big-number { font-size: 2.5rem; font-weight: bold; color: #4ecdc4; }
.api-item { background: #222; padding: 1rem; margin-bottom: 0.5rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
.api-name { font-weight: bold; color: #4ecdc4; }
.api-info { display: flex; gap: 1rem; font-size: 0.9rem; color: #888; }
.api-badge { background: #333; padding: 0.25rem 0.5rem; border-radius: 4px; }
.schedule-daily { color: #ff6b6b; }
.schedule-every3h { color: #ee5a6f; }
.schedule-weekly { color: #ffd93d; }`;

const JS = `const API_INFO = {
  'apod': { name: 'APOD', type: 'JSON+图片', schedule: 'daily', images: 1 },
  'asteroids-neows': { name: 'Asteroids', type: 'JSON', schedule: 'daily', images: 0 },
  'donki': { name: 'DONKI', type: 'JSON', schedule: 'every3h', images: 0 },
  'eonet': { name: 'EONET', type: 'JSON', schedule: 'every3h', images: 0 },
  'epic': { name: 'EPIC', type: 'JSON+图片', schedule: 'daily', images: 1 },
  'mars-rover-photos': { name: 'Mars Rover', type: 'JSON+图片', schedule: 'daily', images: 3 },
  'nasa-ivl': { name: 'NASA IVL', type: 'JSON', schedule: 'weekly', images: 0 },
  'exoplanet': { name: 'Exoplanet', type: 'JSON', schedule: 'weekly', images: 0 },
  'genelab': { name: 'GeneLab', type: 'JSON', schedule: 'weekly', images: 0 },
  'techport': { name: 'TechPort', type: 'JSON', schedule: 'weekly', images: 0 },
  'techtransfer': { name: 'Tech Transfer', type: 'JSON', schedule: 'weekly', images: 0 },
  'earth': { name: 'Earth', type: '图片', schedule: 'weekly', images: 1 }
};

async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    
    let totalDownloads = 0;
    Object.values(stats).forEach(s => totalDownloads += (s.count || 0));
    
    document.getElementById('total-downloads').textContent = totalDownloads;
    document.getElementById('storage-used').textContent = '~' + Math.round(totalDownloads * 1.5) + 'MB';
    
    const now = new Date();
    const next3h = new Date(now);
    next3h.setHours(Math.floor(now.getHours() / 3) * 3 + 3, 0, 0, 0);
    const minutes = Math.floor((next3h - now) / 60000);
    document.getElementById('next-sync').textContent = minutes + '分钟';
    
    displayAPIs(stats);
  } catch (e) {
    console.error(e);
  }
}

function displayAPIs(stats) {
  const container = document.getElementById('api-sources');
  const scheduleNames = {
    'daily': '每日',
    'every3h': '每3小时',
    'weekly': '每周'
  };
  const scheduleColors = {
    'daily': 'schedule-daily',
    'every3h': 'schedule-every3h',
    'weekly': 'schedule-weekly'
  };
  
  const html = Object.entries(API_INFO).map(([key, info]) => {
    const stat = stats[key] || {};
    const count = stat.count || 0;
    const scheduleClass = scheduleColors[info.schedule];
    const scheduleText = scheduleNames[info.schedule];
    
    return '<div class="api-item"><div><div class="api-name">' + info.name + '</div><div class="api-info"><span class="api-badge">' + info.type + '</span><span class="api-badge ' + scheduleClass + '">' + scheduleText + '</span>' + (info.images > 0 ? '<span class="api-badge">' + info.images + '张图片</span>' : '') + '</div></div><div style="text-align:right"><div style="font-size:1.5rem;font-weight:bold;color:#4ecdc4">' + count + '</div><div style="font-size:0.8rem;color:#888">次收集</div></div></div>';
  }).join('');
  
  container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', loadStats);
setInterval(loadStats, 60000);`;

async function loadStats() {
  try {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    
    let totalDownloads = 0;
    Object.values(stats).forEach(s => totalDownloads += (s.count || 0));
    
    document.getElementById('total-downloads').textContent = totalDownloads;
    document.getElementById('storage-used').textContent = '~' + Math.round(totalDownloads * 2.5) + 'MB';
    
    const now = new Date();
    const next6h = new Date(now);
    next6h.setHours(Math.floor(now.getHours() / 6) * 6 + 6, 0, 0, 0);
    const minutes = Math.floor((next6h - now) / 60000);
    document.getElementById('next-sync').textContent = minutes + '分钟';
    
    displayAPIs(stats);
  } catch (e) {
    console.error(e);
  }
}

function displayAPIs(stats) {
  const container = document.getElementById('api-sources');
  const scheduleNames = {
    'daily': '每日',
    'every6h': '每6小时',
    'weekly': '每周'
  };
  const scheduleColors = {
    'daily': 'schedule-daily',
    'every6h': 'schedule-every6h',
    'weekly': 'schedule-weekly'
  };
  
  const html = Object.entries(API_INFO).map(([key, info]) => {
    const stat = stats[key] || {};
    const count = stat.count || 0;
    const scheduleClass = scheduleColors[info.schedule];
    const scheduleText = scheduleNames[info.schedule];
    
    return '<div class="api-item"><div><div class="api-name">' + info.name + '</div><div class="api-info"><span class="api-badge">' + info.type + '</span><span class="api-badge ' + scheduleClass + '">' + scheduleText + '</span>' + (info.images > 0 ? '<span class="api-badge">' + info.images + '张图片</span>' : '') + '</div></div><div style="text-align:right"><div style="font-size:1.5rem;font-weight:bold;color:#4ecdc4">' + count + '</div><div style="font-size:0.8rem;color:#888">次收集</div></div></div>';
  }).join('');
  
  container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', loadStats);
setInterval(loadStats, 60000);`;


const SCHEDULE_MAP = {
  every3h: ["donki", "eonet"],                                                        // 实时事件
  daily: ["apod", "asteroids-neows", "epic", "mars-rover-photos"],                   // 常规更新
  weekly: ["nasa-ivl", "earth", "genelab", "techtransfer", "exoplanet", "techport"]  // 慢更新
};

const IMAGE_LIMITS = {
  'apod': 1,                // 只保存第一张
  'epic': 1,                // 只保存第一张（代表性足够）
  'mars-rover-photos': 3,   // 只保存前 3 张
  'nasa-ivl': 0             // 不下载图片（只保存 JSON 中的 URL）
};

const NASA_CONFIGS = {
  apod: { url: "https://api.nasa.gov/planetary/apod", params: { api_key: "NASA_API_KEY" } },
  "asteroids-neows": { url: "https://api.nasa.gov/neo/rest/v1/feed", params: { api_key: "NASA_API_KEY", start_date: "TODAY", end_date: "TODAY" } },
  donki: { url: "https://api.nasa.gov/DONKI/notifications", params: { api_key: "NASA_API_KEY", startDate: "WEEK_AGO", endDate: "TODAY" } },
  eonet: { url: "https://eonet.gsfc.nasa.gov/api/v3/events", params: { status: "open", limit: 100 } },
  epic: { url: "https://api.nasa.gov/EPIC/api/natural/images", params: { api_key: "NASA_API_KEY" } },
  "mars-rover-photos": { url: "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos", params: { api_key: "NASA_API_KEY", sol: "1000" } },
  "nasa-ivl": { url: "https://images-api.nasa.gov/search", params: { q: "space", media_type: "image", page_size: 20 } },
  exoplanet: { url: "https://exoplanetarchive.ipac.caltech.edu/TAP/sync", params: { query: "select top 100 pl_name,hostname,disc_year from ps where disc_year > 2020", format: "json" } },
  genelab: { url: "https://genelab-data.ndc.nasa.gov/genelab/data/search", params: { term: "space", size: 50 } },
  techport: { url: "https://api.nasa.gov/techport/api/projects", params: { api_key: "NASA_API_KEY" } },
  techtransfer: { url: "https://api.nasa.gov/techtransfer/patent", params: { api_key: "NASA_API_KEY", engine: "patent" } },
  earth: { url: "https://api.nasa.gov/planetary/earth/imagery", params: { api_key: "NASA_API_KEY", lon: -95.33, lat: 29.78, date: "WEEK_AGO", dim: 0.15 } }
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, POST" } });
    }
    
    // API routes
    if (url.pathname.startsWith("/api/") || url.pathname === "/collect") {
      if (url.pathname === "/collect") {
        const source = url.searchParams.get("source");
        if (!source) return json({ error: "Missing source" }, 400);
        await collectData(source, env);
        return json({ success: true, source });
      }
      if (url.pathname === "/api/latest") {
        const source = url.searchParams.get("source");
        if (!source) return json({ error: "Missing source" }, 400);
        const data = await getLatest(source, env);
        return json(data);
      }
      if (url.pathname === "/api/list") {
        const source = url.searchParams.get("source");
        const data = await listFiles(source, env);
        return json(data);
      }
      if (url.pathname === "/api/stats") {
        const stats = await getStats(env);
        return json(stats);
      }
      return json({ error: "Not found" }, 404);
    }
    
    // Static frontend
    if (url.pathname === "/" || url.pathname === "/index.html") {
      return new Response(HTML, { headers: { "Content-Type": "text/html" } });
    }
    if (url.pathname === "/style.css") {
      return new Response(CSS, { headers: { "Content-Type": "text/css" } });
    }
    if (url.pathname === "/script.js") {
      return new Response(JS, { headers: { "Content-Type": "application/javascript" } });
    }
    
    return json({ error: "Not found" }, 404);
  },

  async scheduled(event, env, ctx) {
    const cron = event.cron;
    let scheduleType;
    
    // Determine schedule type from cron
    if (cron === "0 */3 * * *") scheduleType = "every3h";
    else if (cron === "0 0 * * *") scheduleType = "daily";
    else if (cron === "0 0 * * 0") scheduleType = "weekly";
    
    if (!scheduleType) return;
    
    console.log("Running " + scheduleType + " schedule");
    const sources = SCHEDULE_MAP[scheduleType];
    
    // Collect all sources in parallel
    await Promise.allSettled(
      sources.map(source => collectData(source, env))
    );
  }
};

async function collectData(source, env) {
  console.log("Collecting " + source);
  
  try {
    const config = NASA_CONFIGS[source];
    if (!config) throw new Error("Unknown source: " + source);
    
    // Build params
    const params = { ...config.params };
    const apiKey = env.NASA_API_KEY || "DEMO_KEY";
    
    for (const [key, value] of Object.entries(params)) {
      if (value === "NASA_API_KEY") params[key] = apiKey;
      else if (value === "TODAY") params[key] = getDate(0);
      else if (value === "WEEK_AGO") params[key] = getDate(-7);
    }
    
    // Build URL
    const url = new URL(config.url);
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    
    // Fetch data
    const response = await fetch(url.toString(), { 
      signal: AbortSignal.timeout(60000)
    });
    
    if (!response.ok) throw new Error("HTTP " + response.status);
    
    const contentType = response.headers.get("content-type") || "";
    
    // Handle different content types
    if (contentType.includes("image/")) {
      // Save image binary data (e.g., Earth API)
      const imageBuffer = await response.arrayBuffer();
      await saveImageData(source, imageBuffer, contentType, env);
    } else if (contentType.includes("application/json")) {
      // Save JSON data
      const data = await response.json();
      await saveData(source, data, env);
      
      // Download images if JSON contains image URLs
      await downloadImages(source, data, env);
    } else {
      // Save as text (fallback)
      const text = await response.text();
      await saveData(source, { raw_content: text, content_type: contentType }, env);
    }
    
    console.log("Successfully collected " + source);
    
  } catch (error) {
    console.error("Error collecting " + source + ":", error);
    await saveData(source, { error: error.message, timestamp: new Date().toISOString() }, env, true);
  }
}

async function downloadImages(source, data, env) {
  const imageUrls = extractImageUrls(source, data);
  if (imageUrls.length === 0) return;
  
  console.log("Downloading " + imageUrls.length + " images for " + source);
  
  // Download all images
  const images = [];
  for (const imgUrl of imageUrls) {
    try {
      const imgResponse = await fetch(imgUrl, { signal: AbortSignal.timeout(30000) });
      if (!imgResponse.ok) continue;
      
      const imgBuffer = await imgResponse.arrayBuffer();
      images.push(imgBuffer);
    } catch (e) {
      console.error("Failed to download image " + imgUrl + ":", e.message);
    }
  }
  
  if (images.length === 0) return;
  
  // If multiple images, merge them; otherwise save single image
  if (images.length > 1) {
    await saveMergedImages(source, images, env);
  } else {
    const imgContentType = "image/jpeg";
    await saveImageData(source, images[0], imgContentType, env);
  }
}

function extractImageUrls(source, data) {
  const urls = [];
  const limit = IMAGE_LIMITS[source] || 0;
  
  if (limit === 0) return urls;  // 不下载图片
  
  try {
    switch (source) {
      case "apod":
        // APOD: url or hdurl
        if (data.url) urls.push(data.url);
        if (data.hdurl && data.hdurl !== data.url && urls.length < limit) urls.push(data.hdurl);
        break;
        
      case "epic":
        // EPIC: multiple images
        if (Array.isArray(data)) {
          data.slice(0, limit).forEach(item => {
            if (item.image) {
              const date = item.date.split(' ')[0].replace(/-/g, '/');
              urls.push("https://epic.gsfc.nasa.gov/archive/natural/" + date + "/png/" + item.image + ".png");
            }
          });
        }
        break;
        
      case "mars-rover-photos":
        // Mars Rover: photos array
        if (data.photos && Array.isArray(data.photos)) {
          data.photos.slice(0, limit).forEach(photo => {
            if (photo.img_src) urls.push(photo.img_src);
          });
        }
        break;
        
      case "nasa-ivl":
        // NASA Image Library: items with links (limit = 0, won't download)
        if (data.collection && data.collection.items) {
          data.collection.items.slice(0, limit).forEach(item => {
            if (item.links && item.links[0] && item.links[0].href) {
              urls.push(item.links[0].href);
            }
          });
        }
        break;
    }
  } catch (e) {
    console.error("Error extracting image URLs from " + source + ":", e);
  }
  
  return urls;
}

async function saveData(source, data, env, isError = false) {
  const now = new Date();
  const year = now.getUTCFullYear();
  const month = String(now.getUTCMonth() + 1).padStart(2, "0");
  const day = String(now.getUTCDate()).padStart(2, "0");
  const timestamp = now.toISOString().replace(/[-:]/g, "").split(".")[0];
  const suffix = isError ? "_error" : "";
  
  const key = source + "/" + year + "/" + month + "/" + day + "/" + timestamp + suffix + ".json";
  
  await env.NS_DATA.put(key, JSON.stringify(data, null, 2), {
    httpMetadata: { contentType: "application/json" }
  });
  
  // Log to D1
  try {
    await env.DB.prepare(
      "INSERT INTO collections (source, timestamp, status, error) VALUES (?, ?, ?, ?)"
    ).bind(source, now.toISOString(), isError ? "error" : "success", isError ? data.error : null).run();
  } catch (e) {
    console.error("DB log failed:", e);
  }
  
  console.log("Saved: " + key);
}

async function saveMergedImages(source, images, env) {
  const now = new Date();
  const year = now.getUTCFullYear();
  const month = String(now.getUTCMonth() + 1).padStart(2, "0");
  const day = String(now.getUTCDate()).padStart(2, "0");
  const timestamp = now.toISOString().replace(/[-:]/g, "").split(".")[0];
  
  // Create a simple merged format: save as ZIP or concatenate
  // For simplicity, we'll create a JSON manifest with base64 encoded images
  const merged = {
    source,
    timestamp: now.toISOString(),
    count: images.length,
    images: images.map((img, idx) => ({
      index: idx,
      size: img.byteLength,
      data: arrayBufferToBase64(img)
    }))
  };
  
  const key = source + "/" + year + "/" + month + "/" + day + "/" + timestamp + "_merged.json";
  
  await env.NS_DATA.put(key, JSON.stringify(merged), {
    httpMetadata: { contentType: "application/json" }
  });
  
  // Log to D1
  try {
    await env.DB.prepare(
      "INSERT INTO collections (source, timestamp, status, error) VALUES (?, ?, ?, ?)"
    ).bind(source, now.toISOString(), "success", null).run();
  } catch (e) {
    console.error("DB log failed:", e);
  }
  
  console.log("Saved merged images: " + key + " (" + images.length + " images)");
}

function arrayBufferToBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

async function saveImageData(source, imageBuffer, contentType, env) {
  const now = new Date();
  const year = now.getUTCFullYear();
  const month = String(now.getUTCMonth() + 1).padStart(2, "0");
  const day = String(now.getUTCDate()).padStart(2, "0");
  const timestamp = now.toISOString().replace(/[-:]/g, "").split(".")[0];
  
  // Determine file extension from content type
  const ext = contentType.includes("png") ? "png" : contentType.includes("jpeg") || contentType.includes("jpg") ? "jpg" : "bin";
  const key = source + "/" + year + "/" + month + "/" + day + "/" + timestamp + "." + ext;
  
  await env.NS_DATA.put(key, imageBuffer, {
    httpMetadata: { contentType }
  });
  
  // Log to D1
  try {
    await env.DB.prepare(
      "INSERT INTO collections (source, timestamp, status, error) VALUES (?, ?, ?, ?)"
    ).bind(source, now.toISOString(), "success", null).run();
  } catch (e) {
    console.error("DB log failed:", e);
  }
  
  console.log("Saved image: " + key);
}

function getDate(daysOffset) {
  const date = new Date();
  date.setDate(date.getDate() + daysOffset);
  return date.toISOString().split("T")[0];
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
  });
}

async function getLatest(source, env) {
  const cacheKey = "latest:" + source;
  const cached = await env.CACHE.get(cacheKey, "json");
  if (cached) return cached;
  
  const list = await env.NS_DATA.list({ prefix: `${source}/`, limit: 1 });
  if (list.objects.length === 0) return { error: "No data" };
  
  const obj = await env.NS_DATA.get(list.objects[0].key);
  const data = await obj.json();
  
  await env.CACHE.put(cacheKey, JSON.stringify(data), { expirationTtl: 3600 });
  return data;
}

async function listFiles(source, env) {
  const prefix = source ? `${source}/` : "";
  const list = await env.NS_DATA.list({ prefix, limit: 100 });
  return { files: list.objects.map(o => ({ key: o.key, size: o.size, uploaded: o.uploaded })) };
}

async function getStats(env) {
  const sources = Object.keys(NASA_CONFIGS);
  const stats = {};
  
  for (const source of sources) {
    const list = await env.NS_DATA.list({ prefix: `${source}/`, limit: 100 });
    stats[source] = { 
      count: list.objects.length, 
      latest: list.objects[0]?.uploaded || null,
      size: list.objects.reduce((sum, obj) => sum + (obj.size || 0), 0)
    };
  }
  
  return stats;
}
