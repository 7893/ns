import functions_framework
import json
import requests
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取火星车照片"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "mars-rover-photos")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取最新的火星车照片
        client = NASAClient()
        
        # 获取Perseverance火星车最新照片
        rover_data = client.get("mars-photos/api/v1/rovers/perseverance/latest_photos")
        
        if not rover_data.get('latest_photos'):
            raise Exception("No Mars rover photos available")
        
        # 取前3张最新照片
        photos = rover_data['latest_photos'][:3]
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        base_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}"
        
        saved_photos = []
        
        for i, photo in enumerate(photos):
            try:
                # 下载照片
                photo_url = photo['img_src']
                response = requests.get(photo_url, timeout=60)
                response.raise_for_status()
                
                # 获取文件扩展名
                file_ext = photo_url.split('.')[-1].lower()
                if file_ext not in ['jpg', 'jpeg', 'png']:
                    file_ext = 'jpg'
                
                # 保存照片
                photo_path = f"{base_path}_photo_{i+1}.{file_ext}"
                photo_blob = bucket.blob(photo_path)
                photo_blob.upload_from_string(
                    response.content,
                    content_type=f'image/{file_ext}'
                )
                
                saved_photos.append({
                    "path": photo_path,
                    "id": photo['id'],
                    "camera": photo['camera']['name'],
                    "earth_date": photo['earth_date']
                })
                
                print(f"Photo {i+1} saved to: gs://ns-2025-data/{photo_path}")
                
            except Exception as e:
                print(f"Failed to download photo {i+1}: {e}")
        
        # 保存元数据
        metadata = {
            "rover": "Perseverance",
            "photos": saved_photos,
            "total_photos": len(saved_photos)
        }
        
        metadata_path = f"{base_path}_metadata.json"
        metadata_blob = bucket.blob(metadata_path)
        metadata_blob.upload_from_string(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Metadata saved to: gs://ns-2025-data/{metadata_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"photos_saved": len(saved_photos), "rover": "Perseverance"}
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
