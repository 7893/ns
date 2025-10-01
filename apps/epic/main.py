import functions_framework
import json
import requests
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA EPIC地球图片"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "epic")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取最近的EPIC图片列表
        client = NASAClient()
        epic_data = client.get("EPIC/api/natural")
        
        if not epic_data:
            raise Exception("No EPIC images available")
        
        # 取最新的图片
        latest_image = epic_data[0]
        image_name = latest_image['image']
        date_str = latest_image['date']
        
        # 解析日期用于构建图片URL
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date_path = date_obj.strftime('%Y/%m/%d')
        
        # 构建图片URL
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_path}/png/{image_name}.png?api_key={client.api_key}"
        
        # 下载图片
        response = requests.get(image_url, timeout=60)
        response.raise_for_status()
        
        # 保存到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        base_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}"
        
        # 保存图片
        image_path = f"{base_path}_{image_name}.png"
        image_blob = bucket.blob(image_path)
        image_blob.upload_from_string(
            response.content,
            content_type='image/png'
        )
        
        # 保存元数据
        metadata_path = f"{base_path}_metadata.json"
        metadata_blob = bucket.blob(metadata_path)
        metadata_blob.upload_from_string(
            json.dumps(latest_image, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Image saved to: gs://ns-2025-data/{image_path}")
        print(f"Metadata saved to: gs://ns-2025-data/{metadata_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"image_name": image_name, "date": date_str}
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
