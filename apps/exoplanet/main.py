import functions_framework
import json
import requests
from datetime import datetime
from google.cloud import storage
from ns_packages import NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取系外行星数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "exoplanet")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 使用新的NASA Exoplanet Archive TAP服务
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        params = {
            "query": "select top 100 pl_name,hostname,disc_year,pl_orbper,pl_bmasse,pl_rade from ps where disc_year > 2020 order by disc_year desc",
            "format": "json"
        }
        
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"exoplanets_count": len(data) if isinstance(data, list) else 0}
        )
        print(log_entry)
        
    except Exception as e:
        print(f"Exoplanet API error: {str(e)}")
        
        # 创建fallback数据
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_fallback.json"
            
            fallback_data = {
                "message": f"Exoplanet API unavailable: {str(e)}",
                "timestamp": now.isoformat(),
                "fallback": True,
                "service": "NASA Exoplanet Archive"
            }
            
            blob = bucket.blob(file_path)
            blob.upload_from_string(
                json.dumps(fallback_data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            print(f"Fallback data saved to: gs://ns-2025-data/{file_path}")
            
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
        
        error_log = NASADataParser.create_log_entry(
            job_id=job_id,
            status="ERROR",
            error=str(e)
        )
        print(error_log)
    
    print(f"--- Function '{job_id}' finished ---")
