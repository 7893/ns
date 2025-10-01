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
        # GeneLab使用独立的API，不需要NASA API密钥
        response = requests.get("https://genelab-data.ndc.nasa.gov/genelab/data/search?type=study", timeout=30)
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
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"studies_count": len(data.get("studies", [])) if isinstance(data, dict) else 0}
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
