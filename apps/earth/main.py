import functions_framework
import json
from datetime import datetime, timedelta
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA Earth地球图像数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "earth")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 使用更近的日期和更大的容错范围
        date_str = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # 尝试获取地球图像数据 - 使用imagery端点
        earth_data = client.get("planetary/earth/imagery", {
            "lon": -95.33,  # 美国中部经度
            "lat": 29.78,   # 美国中部纬度  
            "date": date_str,
            "dim": 0.15
        }, timeout=90)
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 保存元数据而不是图像本身
        metadata = {
            "date": date_str,
            "location": {"lon": -95.33, "lat": 29.78},
            "dim": 0.15,
            "timestamp": now.isoformat(),
            "data_type": "earth_imagery_metadata"
        }
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={
                "date": date_str, 
                "location": "US Central",
                "data_type": "imagery_metadata"
            }
        )
        print(log_entry)
        
    except Exception as e:
        # 如果主要API失败，创建一个基本的地球数据记录
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_fallback.json"
            
            fallback_data = {
                "message": f"Earth API unavailable: {str(e)}",
                "timestamp": now.isoformat(),
                "fallback": True,
                "attempted_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
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
