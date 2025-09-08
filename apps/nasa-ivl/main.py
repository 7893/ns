import base64
import functions_framework

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """
    This is a placeholder function.
    It prints the received event data.
    """
    job_id = cloud_event["subject"] or "unknown_job"
    print(f"--- Worker Function for '{job_id}' received an event ---")
    print(f"Event ID: {cloud_event['id']}")
    print(f"Event Type: {cloud_event['type']}")
    print(f"Data: {base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')}")
    print("--- End of event ---")
