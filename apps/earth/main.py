import functions_framework
import json
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA Earth地球资产数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "earth")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 获取地球资产数据 - 使用纽约坐标
        date_str = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # 获取可用的地球资产
        earth_assets = client.get("planetary/earth/assets", {
            "lon": -74.0059,  # 纽约经度
            "lat": 40.7128,   # 纽约纬度
            "date": date_str,
            "dim": 0.25
        })
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(earth_assets, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={
                "date": date_str, 
                "location": "New York",
                "assets_count": len(earth_assets) if isinstance(earth_assets, list) else 0
            }
        )
        print(log_entry)
        
    except Exception as e:
        error_log = NASADataParser.create_log_entry(
            job_id=job_id,
            status="ERROR",
            error=str(e)
        )
        print(error_log)
    
    print(f"--- Function '{job_id}' finished ---")
