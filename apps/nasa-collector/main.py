import functions_framework
import json
import requests
from datetime import datetime, timedelta
from google.cloud import storage

# NASA API配置
NASA_CONFIGS = {
    "apod": {
        "url": "https://api.nasa.gov/planetary/apod",
        "params": {"api_key": "DEMO_KEY"}
    },
    "asteroids": {
        "url": "https://api.nasa.gov/neo/rest/v1/feed",
        "params": {"api_key": "DEMO_KEY", "start_date": "TODAY", "end_date": "TODAY"}
    },
    "exoplanet": {
        "url": "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
        "params": {"query": "select top 100 pl_name,hostname from ps", "format": "json"}
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
        if "TODAY" in str(params):
            today = datetime.now().strftime("%Y-%m-%d")
            params = {k: v.replace("TODAY", today) if isinstance(v, str) else v for k, v in params.items()}
        
        response = requests.get(config["url"], params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
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
