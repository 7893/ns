import functions_framework
import json
import requests
from datetime import datetime
from google.cloud import storage
from ns_packages import NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA图像和视频库数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "nasa-ivl")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 搜索最新的NASA图像
        search_url = "https://images-api.nasa.gov/search"
        params = {
            "q": "earth",
            "media_type": "image",
            "page_size": 5
        }
        
        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        search_data = response.json()
        
        # 保存搜索结果数据
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        base_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}"
        
        # 保存搜索结果元数据
        metadata_path = f"{base_path}_search_results.json"
        metadata_blob = bucket.blob(metadata_path)
        metadata_blob.upload_from_string(
            json.dumps(search_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Search results saved to: gs://ns-2025-data/{metadata_path}")
        
        # 输出结构化日志
        items_count = len(search_data.get("collection", {}).get("items", []))
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"items_found": items_count, "query": "earth"}
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
