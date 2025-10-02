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
    
    // Manual trigger: /collect?source=apod
    if (url.pathname === "/collect") {
      const source = url.searchParams.get("source");
      if (!source) return new Response("Missing source parameter", { status: 400 });
      
      await collectData(source, env);
      return new Response(`Collected ${source}`, { status: 200 });
    }
    
    // Status endpoint
    if (url.pathname === "/") {
      return new Response("NS Worker running", { status: 200 });
    }
    
    return new Response("Not found", { status: 404 });
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
  
  console.log(`Saved: ${key}`);
}

function getDate(daysOffset) {
  const date = new Date();
  date.setDate(date.getDate() + daysOffset);
  return date.toISOString().split("T")[0];
}
