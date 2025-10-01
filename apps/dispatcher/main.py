import functions_framework
import base64
import json
import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT")

SCHEDULE_MAP = {
    "daily": ["apod", "asteroids", "donki", "epic", "mars-rover"],
    "hourly": ["eonet", "nasa-ivl"],
    "weekly": ["exoplanet", "genelab", "techport", "techtransfer", "earth"]
}

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    print("Dispatcher started")
    
    publisher = pubsub_v1.PublisherClient()
    
    try:
        message_data = cloud_event.data.get("message", {}).get("data", "")
        if message_data:
            data_str = base64.b64decode(message_data).decode("utf-8")
            data_json = json.loads(data_str)
            schedule_type = data_json.get("schedule_type")
        else:
            schedule_type = "daily"
            
        print(f"Schedule: {schedule_type}")
    except Exception as e:
        print(f"Error: {e}")
        return

    jobs = SCHEDULE_MAP.get(schedule_type, [])
    topic_path = publisher.topic_path(PROJECT_ID, "ns-topic-collector")
    
    for source in jobs:
        try:
            future = publisher.publish(topic_path, b"collect", source=source)
            future.result()
            print(f"Dispatched: {source}")
        except Exception as e:
            print(f"Failed {source}: {e}")
    
    print("Dispatcher finished")
