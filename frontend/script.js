// NS - NASA Data System Frontend
document.addEventListener('DOMContentLoaded', function() {
    loadSystemStatus();
    loadDataSources();
});

function loadSystemStatus() {
    const statusElement = document.getElementById('system-status');
    
    // 模拟系统状态
    const status = {
        functions: 1,
        topics: 1,
        lastUpdate: new Date().toLocaleString('zh-CN')
    };
    
    statusElement.innerHTML = `
        <div>函数数量: ${status.functions}</div>
        <div>Topic数量: ${status.topics}</div>
        <div>最后更新: ${status.lastUpdate}</div>
    `;
}

function loadDataSources() {
    const sourcesElement = document.getElementById('data-sources');
    
    const sources = [
        'APOD', 'Asteroids', 'DONKI', 'EONET', 'EPIC', 
        'Mars Rover Photos', 'NASA Image Library', 'Exoplanet',
        'GeneLab', 'TechPort', 'Tech Transfer', 'Earth Imagery'
    ];
    
    sourcesElement.innerHTML = sources.map(source => 
        `<span style="display: inline-block; margin: 0.5rem; padding: 0.5rem 1rem; background: #333; border-radius: 6px;">${source}</span>`
    ).join('');
}
