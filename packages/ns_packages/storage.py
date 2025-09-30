import json
import os
from datetime import datetime
from google.cloud import storage

class GCSStorage:
    def __init__(self):
        self.bucket_name = "ns-2025-data"
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
    
    def save_data(self, job_id: str, data: dict) -> str:
        """保存数据到GCS"""
        try:
            # 生成文件路径: job_id/year/month/day/timestamp.json
            now = datetime.utcnow()
            file_path = f"{job_id}/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}.json"
            
            # 创建blob并上传
            blob = self.bucket.blob(file_path)
            blob.upload_from_string(
                json.dumps(data, indent=2, ensure_ascii=False),
                content_type='application/json'
            )
            
            return f"gs://{self.bucket_name}/{file_path}"
        except Exception as e:
            raise Exception(f"Failed to save data to GCS: {str(e)}")
