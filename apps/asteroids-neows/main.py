import functions_framework
from datetime import datetime, timedelta
from ns_packages import NASAClient, NASADataParser

@functions_framework.cloud_event
def handle_pubsub(cloud_event):
    """获取近地小行星数据"""
    
    # 获取job_id
    attributes = cloud_event.data.get("message", {}).get("attributes", {})
    job_id = attributes.get("subject", "asteroids-neows")
    
    print(f"--- Function '{job_id}' started ---")
    
    try:
        # 计算查询日期范围（今天到未来7天）
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        
        start_date_str = today.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # 使用共享客户端获取数据
        client = NASAClient()
        raw_data = client.get_asteroids_neows(start_date_str, end_date_str)
        
        # 使用共享解析器处理数据
        parsed_data = NASADataParser.parse_asteroids(raw_data)
        
        # 输出结构化日志
        log_entry = NASADataParser.create_log_entry(
            job_id=job_id,
            status="SUCCESS",
            data={
                "date_range": f"{start_date_str} to {end_date_str}",
                "asteroid_count": len(parsed_data["asteroids"]),
                "element_count": parsed_data["element_count"]
            }
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
