import functions_framework
import json
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA DONKI太阳活动数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "donki")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取最近7天的太阳耀斑数据
        client = NASAClient()
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        # 获取太阳耀斑数据
        flare_data = client.get("DONKI/FLR", {
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d")
        })
        
        # 保存数据到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 上传数据
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(flare_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"flares_count": len(flare_data), "date_range": f"{start_date} to {end_date}"}
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
