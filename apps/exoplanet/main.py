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
        # NASA Exoplanet Archive API (不需要API密钥)
        response = requests.get("https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI", {
            "table": "exoplanets",
            "format": "json",
            "select": "pl_name,pl_orbper,pl_bmasse,pl_rade,st_dist",
            "where": "pl_orbper<365 and pl_bmasse>0",
            "order": "pl_name",
            "limit": 100
        }, timeout=30)
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
        error_log = NASADataParser.create_log_entry(
            job_id=job_id,
            status="ERROR",
            error=str(e)
        )
        print(error_log)
    
    print(f"--- Function '{job_id}' finished ---")
