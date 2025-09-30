import functions_framework
import json
import os
from datetime import datetime
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA每日天文图片"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "apod")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 使用共享客户端获取数据
        client = NASAClient()
        raw_data = client.get_apod()
        
        # 使用共享解析器处理数据
        parsed_data = NASADataParser.parse_apod(raw_data)
        
        # 保存数据到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        # 生成文件路径
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 上传数据
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(parsed_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        file_url = f"gs://ns-2025-data/{file_path}"
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data=parsed_data
        )
        print(f"Data saved to: {file_url}")
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
