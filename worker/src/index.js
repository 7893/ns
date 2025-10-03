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
<header><h1>🚀 NS - NASA Data System</h1><p>极简化的NASA数据收集系统</p></header>
<main>
<section class="status"><h2>系统状态</h2><div id="system-status">加载中...</div></section>
<section class="data-sources"><h2>数据源</h2><div id="data-sources">加载中...</div></section>
</main>
</div>
<script src="/script.js"></script>
</body>
</html>`;

const CSS = \`* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0a; color: #fff; line-height: 1.6; }
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
header { text-align: center; margin-bottom: 3rem; }
header h1 { font-size: 3rem; margin-bottom: 0.5rem; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
header p { color: #888; font-size: 1.2rem; }
section { background: #1a1a1a; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; border: 1px solid #333; }
section h2 { margin-bottom: 1rem; color: #4ecdc4; }
#system-status, #data-sources { color: #ccc; }\`;

const JS = \`async function loadSystemStatus() {
  try {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    const statusElement = document.getElementById('system-status');
    const count = Object.keys(stats).length;
    statusElement.innerHTML = \\\`<div>数据源: \${count}</div><div>状态: 运行中</div><div>最后更新: \${new Date().toLocaleString('zh-CN')}</div>\\\`;
  } catch (e) { console.error(e); }
}
async function loadDataSources() {
  const sources = ['apod', 'asteroids-neows', 'donki', 'eonet', 'epic', 'mars-rover-photos', 'nasa-ivl', 'exoplanet', 'genelab', 'techport', 'techtransfer', 'earth'];
  const sourcesElement = document.getElementById('data-sources');
  sourcesElement.innerHTML = sources.map(s => \\\`<span style="display:inline-block;margin:0.5rem;padding:0.5rem 1rem;background:#333;border-radius:6px;cursor:pointer" onclick="viewSource('\${s}')">\${s}</span>\\\`).join('');
}
async function viewSource(source) {
  try {
    const res = await fetch(\\\`/api/latest?source=\${source}\\\`);
    const data = await res.json();
    alert(\\\`\${source}:\\n\${JSON.stringify(data, null, 2).slice(0, 500)}...\\\`);
  } catch (e) { alert(\\\`Error: \${e.message}\\\`); }
}
document.addEventListener('DOMContentLoaded', () => { loadSystemStatus(); loadDataSources(); });\`;

const SCHEDULE_MAP = {
  daily: ["apod", "asteroids-neows", "donki", "epic", "mars-rover-photos"],
  hourly: ["eonet", "nasa-ivl"],
  weekly: ["exoplanet", "genelab", "techport", "techtransfer", "earth"]
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
    if (cron === "0 0 * * *") scheduleType = "daily";
    else if (cron === "0 * * * *") scheduleType = "hourly";
    else if (cron === "0 0 * * 0") scheduleType = "weekly";
    
    if (!scheduleType) return;
    
    console.log(`Running ${scheduleType} schedule`);
    const sources = SCHEDULE_MAP[scheduleType];
    
    // Collect all sources in parallel
    await Promise.allSettled(
      sources.map(source => collectData(source, env))
    );
  }
};

async function collectData(source, env) {
  console.log(`Collecting ${source}`);
  
  try {
    const config = NASA_CONFIGS[source];
    if (!config) throw new Error(`Unknown source: ${source}`);
    
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
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    
    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json") 
      ? await response.json()
      : { raw_content: (await response.text()).slice(0, 1000) };
    
    // Save to R2
    await saveData(source, data, env);
    console.log(`Successfully collected ${source}`);
    
  } catch (error) {
    console.error(`Error collecting ${source}:`, error);
    await saveData(source, { error: error.message, timestamp: new Date().toISOString() }, env, true);
  }
}

async function saveData(source, data, env, isError = false) {
  const now = new Date();
  const year = now.getUTCFullYear();
  const month = String(now.getUTCMonth() + 1).padStart(2, "0");
  const day = String(now.getUTCDate()).padStart(2, "0");
  const timestamp = now.toISOString().replace(/[-:]/g, "").split(".")[0];
  const suffix = isError ? "_error" : "";
  
  const key = `${source}/${year}/${month}/${day}/${timestamp}${suffix}.json`;
  
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
  
  console.log(`Saved: ${key}`);
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
  const cacheKey = `latest:${source}`;
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
    const list = await env.NS_DATA.list({ prefix: `${source}/`, limit: 1 });
    stats[source] = { count: list.objects.length, latest: list.objects[0]?.uploaded || null };
  }
  
  return stats;
}
