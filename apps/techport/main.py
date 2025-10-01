import functions_framework
import json
from datetime import datetime
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA TechPort技术组合数据"""
    
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "techport")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        client = NASAClient()
        
        # 获取TechPort项目列表
        projects_data = client.get("techport/api/projects", {
            "updatedSince": (datetime.now().replace(day=1)).strftime("%Y-%m-%d")
        }, timeout=60)
        
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(projects_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 提取项目数量
        projects_count = 0
        if isinstance(projects_data, dict) and 'projects' in projects_data:
            projects_count = len(projects_data.get('projects', []))
        elif isinstance(projects_data, list):
            projects_count = len(projects_data)
        
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"projects_count": projects_count}
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
                "message": f"TechPort API unavailable: {str(e)}",
                "timestamp": now.isoformat(),
                "fallback": True,
                "service": "NASA TechPort"
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
