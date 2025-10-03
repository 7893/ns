const API_BASE = "https://ns.YOUR_SUBDOMAIN.workers.dev";

document.addEventListener('DOMContentLoaded', () => {
    loadSystemStatus();
    loadDataSources();
});

async function loadSystemStatus() {
    try {
        const res = await fetch(`${API_BASE}/api/stats`);
        const stats = await res.json();
        const statusElement = document.getElementById('system-status');
        const count = Object.keys(stats).length;
        statusElement.innerHTML = `
            <div>数据源: ${count}</div>
            <div>状态: 运行中</div>
            <div>最后更新: ${new Date().toLocaleString('zh-CN')}</div>
        `;
    } catch (e) {
        console.error("Failed to load status:", e);
    }
}

async function loadDataSources() {
    const sources = ['apod', 'asteroids-neows', 'donki', 'eonet', 'epic', 
        'mars-rover-photos', 'nasa-ivl', 'exoplanet', 'genelab', 'techport', 
        'techtransfer', 'earth'];
    
    const sourcesElement = document.getElementById('data-sources');
    sourcesElement.innerHTML = sources.map(s => 
        `<span style="display:inline-block;margin:0.5rem;padding:0.5rem 1rem;background:#333;border-radius:6px;cursor:pointer" onclick="viewSource('${s}')">${s}</span>`
    ).join('');
}

async function viewSource(source) {
    try {
        const res = await fetch(`${API_BASE}/api/latest?source=${source}`);
        const data = await res.json();
        alert(`${source}:\n${JSON.stringify(data, null, 2).slice(0, 500)}...`);
    } catch (e) {
        alert(`Error: ${e.message}`);
    }
}

