import functions_framework
import json
import requests
from datetime import datetime
from google.cloud import storage
from ns_packages import NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA EONET自然事件数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "eonet")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # EONET API不需要API密钥
        response = requests.get("https://eonet.gsfc.nasa.gov/api/v3/events", timeout=30)
        response.raise_for_status()
        raw_data = response.json()
        
        # 保存数据到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        # 生成文件路径
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 上传数据
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(raw_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"events_count": len(raw_data.get("events", [])), "title": raw_data.get("title", "")}
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
