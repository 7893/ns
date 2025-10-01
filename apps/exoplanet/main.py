import functions_framework
import json
from datetime import datetime
from google.cloud import storage

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    print("Function started")
    
    try:
        print("Creating storage client")
        storage_client = storage.Client()
        bucket = storage_client.bucket("ns-2025-data")
        
        now = datetime.utcnow()
        file_path = f"exoplanet/{now.year}/{now.month:02d}/{now.day:02d}/{now.strftime('%Y%m%d_%H%M%S')}_test.json"
        
        test_data = {"test": "minimal exoplanet data", "timestamp": now.isoformat()}
        
        print(f"Saving to {file_path}")
        blob = bucket.blob(file_path)
        blob.upload_from_string(json.dumps(test_data), content_type='application/json')
        
        print(f"Success: gs://ns-2025-data/{file_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("Function finished")
