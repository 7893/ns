import base64
import json
import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT")

SCHEDULE_MAP = {
    "daily": ["apod", "asteroids-neows", "donki", "epic", "insight", "mars-rover-photos"],
    "hourly": ["eonet", "nasa-ivl"],
    "weekly": ["exoplanet", "genelab", "techport", "techtransfer", "earth"]
}

publisher = pubsub_v1.PublisherClient()

def handle_pubsub(event, context):
    print(f"Dispatcher received trigger event.")
    try:
        data_str = base64.b64decode(event["data"]).decode("utf-8")
        data_json = json.loads(data_str)
        schedule_type = data_json.get("schedule_type")
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
            topic_path = publisher.topic_path(PROJECT_ID, f"topic-{job_id}")
            # Publish a simple message; the function is triggered by the topic itself
            future = publisher.publish(topic_path, b"Go!", subject=job_id)
            future.result()
            print(f"Successfully dispatched job to topic: topic-{job_id}")
        except Exception as e:
            print(f"Error dispatching to topic-{job_id}: {e}")
    print("Dispatcher finished.")