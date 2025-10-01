import functions_framework
import json
import os
import requests
from datetime import datetime, timedelta
from google.cloud import storage

# NASA API配置
NASA_CONFIGS = {
    "apod": {
        "url": "https://api.nasa.gov/planetary/apod",
        "params": {"api_key": "NASA_API_KEY"}
    },
    "asteroids-neows": {
        "url": "https://api.nasa.gov/neo/rest/v1/feed",
        "params": {"api_key": "NASA_API_KEY", "start_date": "TODAY", "end_date": "TODAY"}
    },
    "donki": {
        "url": "https://api.nasa.gov/DONKI/notifications",
        "params": {"api_key": "NASA_API_KEY", "startDate": "WEEK_AGO", "endDate": "TODAY"}
    },
    "eonet": {
        "url": "https://eonet.gsfc.nasa.gov/api/v3/events",
        "params": {"status": "open", "limit": 100}
    },
    "epic": {
        "url": "https://api.nasa.gov/EPIC/api/natural/images",
        "params": {"api_key": "NASA_API_KEY"}
    },
    "mars-rover-photos": {
        "url": "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos",
        "params": {"api_key": "NASA_API_KEY", "sol": "LATEST"}
    },
    "nasa-ivl": {
        "url": "https://images-api.nasa.gov/search",
        "params": {"q": "space", "media_type": "image", "page_size": 20}
    },
    "exoplanet": {
        "url": "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
        "params": {"query": "select top 100 pl_name,hostname,disc_year from ps where disc_year > 2020", "format": "json"}
    },
    "genelab": {
        "url": "https://genelab-data.ndc.nasa.gov/genelab/data/search",
        "params": {"term": "space", "size": 50}
    },
    "techport": {
        "url": "https://api.nasa.gov/techport/api/projects",
        "params": {"api_key": "NASA_API_KEY"}
    },
    "techtransfer": {
        "url": "https://api.nasa.gov/techtransfer/patent",
        "params": {"api_key": "NASA_API_KEY", "engine": "patent"}
    },
    "earth": {
        "url": "https://api.nasa.gov/planetary/earth/imagery",
        "params": {"api_key": "NASA_API_KEY", "lon": -95.33, "lat": 29.78, "date": "WEEK_AGO", "dim": 0.15}
    }
}

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    data_source = attributes.get("source", "unknown")
    
    print(f"Processing {data_source}")
    
    try:
        config = NASA_CONFIGS.get(data_source)
        if not config:
            raise ValueError(f"Unknown source: {data_source}")
        
        # 处理动态参数
        params = config["params"].copy()
        nasa_api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        
        # 替换占位符
        for key, value in params.items():
            if isinstance(value, str):
                if value == "NASA_API_KEY":
                    params[key] = nasa_api_key
                elif value == "TODAY":
                    params[key] = datetime.now().strftime("%Y-%m-%d")
                elif value == "WEEK_AGO":
                    params[key] = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                elif value == "LATEST":
                    params[key] = "1000"  # 使用固定sol值
        
        response = requests.get(config["url"], params=params, timeout=60)
        response.raise_for_status()
        
        # 处理不同的响应格式
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
        else:
            data = {"raw_content": response.text, "content_type": response.headers.get('content-type')}
        
        # 保存数据
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{data_source}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(json.dumps(data, indent=2), content_type='application/json')
        
        print(f"Saved: gs://ns-2025-data/{file_path}")
        
    except Exception as e:
        print(f"Error processing {data_source}: {e}")
        
        # Fallback数据
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{data_source}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_error.json"
            
            error_data = {"error": str(e), "timestamp": now.isoformat(), "source": data_source}
            
            blob = bucket.blob(file_path)
            blob.upload_from_string(json.dumps(error_data), content_type='application/json')
            
            print(f"Error data saved: gs://ns-2025-data/{file_path}")
        except Exception as fe:
            print(f"Fallback failed: {fe}")
