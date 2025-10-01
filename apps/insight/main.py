import functions_framework
import json
from datetime import datetime
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA InSight火星天气数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "insight")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取InSight火星天气数据
        client = NASAClient()
        weather_data = client.get("insight_weather/")
        
        # 保存数据到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 上传数据
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(weather_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"sol_keys": len(weather_data.get("sol_keys", [])) if isinstance(weather_data, dict) else 0}
        )
        print(log_entry)
        
    except Exception as e:
        # 错误处理
        error_log = NASADataParser.create_log_entry(
            job_id=job_id,
            status="ERROR",
            error=str(e)
        )
        print(error_log)
    
    print(f"--- Function '{job_id}' finished ---")
