import functions_framework
import json
import os
import requests
import base64
from datetime import datetime, timedelta
from google.cloud import storage, pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT", "sigma-outcome")

# 调度配置
SCHEDULE_MAP = {
    "daily": ["apod", "asteroids-neows", "donki", "epic", "mars-rover-photos"],
    "hourly": ["eonet", "nasa-ivl"], 
    "weekly": ["exoplanet", "genelab", "techport", "techtransfer", "earth"]
}

# NASA API配置
NASA_CONFIGS = {
    "apod": {"url": "https://api.nasa.gov/planetary/apod", "params": {"api_key": "NASA_API_KEY"}},
    "asteroids-neows": {"url": "https://api.nasa.gov/neo/rest/v1/feed", "params": {"api_key": "NASA_API_KEY", "start_date": "TODAY", "end_date": "TODAY"}},
    "donki": {"url": "https://api.nasa.gov/DONKI/notifications", "params": {"api_key": "NASA_API_KEY", "startDate": "WEEK_AGO", "endDate": "TODAY"}},
    "eonet": {"url": "https://eonet.gsfc.nasa.gov/api/v3/events", "params": {"status": "open", "limit": 100}},
    "epic": {"url": "https://api.nasa.gov/EPIC/api/natural/images", "params": {"api_key": "NASA_API_KEY"}},
    "mars-rover-photos": {"url": "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos", "params": {"api_key": "NASA_API_KEY", "sol": "1000"}},
    "nasa-ivl": {"url": "https://images-api.nasa.gov/search", "params": {"q": "space", "media_type": "image", "page_size": 20}},
    "exoplanet": {"url": "https://exoplanetarchive.ipac.caltech.edu/TAP/sync", "params": {"query": "select top 100 pl_name,hostname,disc_year from ps where disc_year > 2020", "format": "json"}},
    "genelab": {"url": "https://genelab-data.ndc.nasa.gov/genelab/data/search", "params": {"term": "space", "size": 50}},
    "techport": {"url": "https://api.nasa.gov/techport/api/projects", "params": {"api_key": "NASA_API_KEY"}},
    "techtransfer": {"url": "https://api.nasa.gov/techtransfer/patent", "params": {"api_key": "NASA_API_KEY", "engine": "patent"}},
    "earth": {"url": "https://api.nasa.gov/planetary/earth/imagery", "params": {"api_key": "NASA_API_KEY", "lon": -95.33, "lat": 29.78, "date": "WEEK_AGO", "dim": 0.15}}
}

@functions_framework.cloud_event
def handle_all(cloud_event):
    """统一处理调度和数据收集"""
    
    message = cloud_event.data.get("message", {})
    attributes = message.get("attributes", {})
    
    # 调度模式：处理定时触发
    if message.get("data"):
        try:
            data_str = base64.b64decode(message["data"]).decode("utf-8")
            data_json = json.loads(data_str)
            if "schedule_type" in data_json:
                dispatch_jobs(data_json["schedule_type"])
                return
        except:
            pass
    
    # 收集模式：处理数据源收集
    if "source" in attributes:
        collect_data(attributes["source"])
        return
    
    print("Unknown message format")

def dispatch_jobs(schedule_type):
    """调度任务"""
    print(f"Dispatching {schedule_type} jobs")
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, "ns-topic-unified")
    
    jobs = SCHEDULE_MAP.get(schedule_type, [])
    for source in jobs:
        try:
            future = publisher.publish(topic_path, b"collect", source=source)
            future.result()
            print(f"Dispatched: {source}")
        except Exception as e:
            print(f"Failed to dispatch {source}: {e}")
    
    print("Dispatch completed")

def collect_data(source):
    """收集数据"""
    print(f"Collecting {source}")
    
    try:
        config = NASA_CONFIGS.get(source)
        if not config:
            raise ValueError(f"Unknown source: {source}")
        
        # 处理参数
        params = config["params"].copy()
        nasa_api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
        
        for key, value in params.items():
            if isinstance(value, str):
                if value == "NASA_API_KEY":
                    params[key] = nasa_api_key
                elif value == "TODAY":
                    params[key] = datetime.now().strftime("%Y-%m-%d")
                elif value == "WEEK_AGO":
                    params[key] = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # API调用
        response = requests.get(config["url"], params=params, timeout=60)
        response.raise_for_status()
        
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
        else:
            data = {"raw_content": response.text[:1000]}  # 限制大小
        
        # 保存数据
        save_data(source, data)
        print(f"Successfully collected {source}")
        
    except Exception as e:
        print(f"Error collecting {source}: {e}")
        save_data(source, {"error": str(e), "timestamp": datetime.utcnow().isoformat()}, is_error=True)

def save_data(source, data, is_error=False):
    """保存数据到GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket("ns-2025-data")
    
    now = datetime.utcnow()
    suffix = "_error" if is_error else ""
    file_path = f"{source}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}{suffix}.json"
    
    blob = bucket.blob(file_path)
    blob.upload_from_string(json.dumps(data, indent=2), content_type='application/json')
    
    print(f"Saved: gs://ns-2025-data/{file_path}")
