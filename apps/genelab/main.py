import functions_framework
import json
import requests
from datetime import datetime
from google.cloud import storage
from ns_packages import NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取GeneLab基因实验室数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "genelab")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 使用GeneLab API搜索最新的研究数据
        url = "https://genelab-data.ndc.nasa.gov/genelab/data/search"
        params = {
            "term": "",
            "size": 20,
            "from": 0,
            "sort": "Release Date:desc"
        }
        
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'NS-Data-Collector/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        
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
        
        # 提取研究数量
        studies_count = 0
        if isinstance(data, dict) and 'hits' in data:
            studies_count = len(data.get('hits', []))
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"studies_count": studies_count}
        )
        print(log_entry)
        
    except Exception as e:
        # 创建fallback数据
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket("ns-2025-data")
            
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_fallback.json"
            
            fallback_data = {
                "message": f"GeneLab API unavailable: {str(e)}",
                "timestamp": now.isoformat(),
                "fallback": True,
                "service": "NASA GeneLab"
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
