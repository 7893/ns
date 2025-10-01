import functions_framework
import json
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取DONKI太空天气数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "donki")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 获取过去7天的太空天气事件
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        data = client.get("DONKI/FLR", {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d")
        })
        
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
            data={"events_count": len(data) if isinstance(data, list) else 0}
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
