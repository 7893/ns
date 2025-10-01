import functions_framework
import base64
import json
import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT")

SCHEDULE_MAP = {
    "daily": ["apod", "asteroids-neows", "donki", "epic", "mars-rover-photos"],
    "hourly": ["eonet", "nasa-ivl"],
    "weekly": ["exoplanet", "genelab", "techport", "techtransfer", "earth"]
}

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    print(f"Dispatcher received trigger event.")
    
    # 延迟初始化publisher
    publisher = pubsub_v1.PublisherClient()
    
    try:
        # 从Cloud Event中获取数据
        message_data = cloud_event.data.get("message", {}).get("data", "")
        if message_data:
            data_str = base64.b64decode(message_data).decode("utf-8")
            data_json = json.loads(data_str)
            schedule_type = data_json.get("schedule_type")
        else:
            # 如果没有数据，默认为daily
            schedule_type = "daily"
            
        if not schedule_type:
            raise ValueError("'schedule_type' not found.")
        print(f"Dispatching jobs for schedule: {schedule_type}")
    except Exception as e:
        print(f"Error decoding trigger message: {e}")
        return

    jobs_to_dispatch = SCHEDULE_MAP.get(schedule_type, [])
    for job_id in jobs_to_dispatch:
        try:
            # Dynamically construct the topic path for each job
            topic_path = publisher.topic_path(PROJECT_ID, f"ns-topic-{job_id}")
            # Publish a simple message; the function is triggered by the topic itself
            future = publisher.publish(topic_path, b"Go!", subject=job_id)
            future.result()
            print(f"Successfully dispatched job to topic: ns-topic-{job_id}")
        except Exception as e:
            print(f"Error dispatching to ns-topic-{job_id}: {e}")
    print("Dispatcher finished.")
