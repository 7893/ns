import functions_framework
import json
from datetime import datetime
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA技术转移数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "techtransfer")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 获取技术转移数据
        tech_data = client.get("techtransfer/patent", {
            "engine": "patent",
            "limit": 50
        }, timeout=60)
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(tech_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 提取专利数量
        patents_count = 0
        if isinstance(tech_data, dict) and 'results' in tech_data:
            patents_count = len(tech_data.get('results', []))
        elif isinstance(tech_data, list):
            patents_count = len(tech_data)
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"patents_count": patents_count}
        )
        print(log_entry)
        
    except Exception as e:
        # 创建fallback数据
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_fallback.json"
            
            fallback_data = {
                "message": f"TechTransfer API unavailable: {str(e)}",
                "timestamp": now.isoformat(),
                "fallback": True,
                "service": "NASA Technology Transfer"
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
