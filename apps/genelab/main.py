import functions_framework
import json
from datetime import datetime
from google.cloud import storage
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取NASA数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "unknown")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 获取数据 - 使用通用端点
        client = NASAClient()
        
        # 根据不同的job_id使用不同的端点
        if job_id == "genelab":
            data = client.get("genelab-data/")
        elif job_id == "techport":
            data = client.get("techport/api/projects")
        elif job_id == "techtransfer":
            data = client.get("techtransfer/")
        else:
            data = {"message": f"Data for {job_id}", "timestamp": datetime.utcnow().isoformat()}
        
        # 保存数据到GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
        
        # 上传数据
        blob = bucket.blob(file_path)
        blob.upload_from_string(
            json.dumps(data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        
        print(f"Data saved to: gs://ns-2025-data/{file_path}")
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={"data_type": job_id}
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
