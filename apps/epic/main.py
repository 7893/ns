import functions_framework
import json
import requests
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取EPIC地球多色成像相机数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "epic")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 获取最近可用日期的EPIC图片列表
        date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        data = client.get("EPIC/api/natural/date/" + date_str)
        
        if data and len(data) > 0:
            # 下载第一张图片
            first_image = data[0]
            image_name = first_image['image']
            
            # 构建图片URL
            date_path = date_str.replace('-', '/')
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_path}/png/{image_name}.png?api_key={client.api_key}"
            
            # 下载图片
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            base_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}"
            
            # 保存图片
            image_path = f"{base_path}_epic.png"
            image_blob = bucket.blob(image_path)
            image_blob.upload_from_string(
                response.content,
                content_type='image/png'
            )
            
            # 保存元数据
            metadata_path = f"{base_path}_metadata.json"
            metadata_blob = bucket.blob(metadata_path)
            metadata_blob.upload_from_string(
                json.dumps(data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            print(f"Image saved to: gs://ns-2025-data/{image_path}")
            print(f"Metadata saved to: gs://ns-2025-data/{metadata_path}")
        else:
            # 只保存元数据
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
            data={"images_count": len(data) if data else 0, "date": date_str}
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
