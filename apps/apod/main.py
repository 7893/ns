import base64
import json
import os
import functions_framework
import requests

# --- 配置 ---
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
APOD_API_URL = "https://api.nasa.gov/planetary/apod"
# --- 配置结束 ---


@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """
    接收来自 Pub/Sub 的事件，从 NASA API 获取每日天文图。
    """
    # 从 Pub/Sub 消息的属性中获取 job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("job_id", "unknown_job")
    
    print(f"--- Function '{job_id}' received event ID: {cloud_event['id']} ---")

    try:
        # 1. 准备并调用NASA API
        params = {"api_key": NASA_API_KEY}
        print(f"Calling APOD API at: {APOD_API_URL}")
        response = requests.get(APOD_API_URL, params=params, timeout=30)
        response.raise_for_status()

        # 2. 解析返回的JSON数据
        apod_data = response.json()
        print("Successfully fetched data from NASA API.")

        # 3. 准备并打印结构化日志
        log_payload = {
            "status": "SUCCESS",
            "job_id": job_id,
            "api_data": {
                "date": apod_data.get("date"),
                "title": apod_data.get("title"),
                "url": apod_data.get("url"),
                "media_type": apod_data.get("media_type"),
            }
        }
        print(json.dumps(log_payload))

    except requests.exceptions.RequestException as e:
        print(f"ERROR: API request failed. Error: {e}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred. Error: {e}")
    
    print(f"--- Function '{job_id}' finished. ---")