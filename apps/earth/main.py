import functions_framework
import json
import requests
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA Earth地球卫星图片"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "earth")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取地球图片 - 使用纽约坐标作为示例
        client = NASAClient()
        
        # 获取最近的地球图片
        date_str = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        earth_data = client.get("planetary/earth/imagery", {
            "lon": -74.0059,  # 纽约经度
            "lat": 40.7128,   # 纽约纬度
            "date": date_str,
            "dim": 0.15
        })
        
        # 如果返回的是图片URL，下载图片
        if isinstance(earth_data, dict) and "url" in earth_data:
            image_url = earth_data["url"]
            
            # 下载图片
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            # 保存到GCS
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            base_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}"
            
            # 保存图片
            image_path = f"{base_path}_earth.jpg"
            image_blob = bucket.blob(image_path)
            image_blob.upload_from_string(
                response.content,
                content_type='image/jpeg'
            )
            
            # 保存元数据
            metadata = {
                "date": date_str,
                "longitude": -74.0059,
                "latitude": 40.7128,
                "location": "New York",
                "image_url": image_url
            }
            
            metadata_path = f"{base_path}_metadata.json"
            metadata_blob = bucket.blob(metadata_path)
            metadata_blob.upload_from_string(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            print(f"Image saved to: gs://ns-2025-data/{image_path}")
            print(f"Metadata saved to: gs://ns-2025-data/{metadata_path}")
            
        else:
            # 如果是其他数据格式，直接保存JSON
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
            
            blob = bucket.blob(file_path)
            blob.upload_from_string(
                json.dumps(earth_data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"date": date_str, "location": "New York"}
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
