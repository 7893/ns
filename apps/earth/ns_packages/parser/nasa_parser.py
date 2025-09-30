from typing import Dict, Any, List
import json

class NASADataParser:
    """NASA数据解析器"""
    
    @staticmethod
    def parse_apod(data: Dict[str, Any]) -> Dict[str, Any]:
        """解析APOD数据"""
        return {
            "date": data.get("date"),
            "title": data.get("title"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "hdurl": data.get("hdurl"),
            "media_type": data.get("media_type"),
            "copyright": data.get("copyright")
        }
    
    @staticmethod
    def parse_asteroids(data: Dict[str, Any]) -> Dict[str, Any]:
        """解析小行星数据"""
        near_earth_objects = data.get("near_earth_objects", {})
        parsed_data = {
            "element_count": data.get("element_count", 0),
            "dates": list(near_earth_objects.keys()),
            "asteroids": []
        }
        
        for date, asteroids in near_earth_objects.items():
            for asteroid in asteroids:
                parsed_data["asteroids"].append({
                    "id": asteroid.get("id"),
                    "name": asteroid.get("name"),
                    "date": date,
                    "estimated_diameter_km": asteroid.get("estimated_diameter", {}).get("kilometers", {}),
                    "is_potentially_hazardous": asteroid.get("is_potentially_hazardous_asteroid"),
                    "close_approach_data": asteroid.get("close_approach_data", [])
                })
        
        return parsed_data
    
    @staticmethod
    def create_log_entry(job_id: str, status: str, data: Any = None, error: str = None) -> str:
        """创建结构化日志条目"""
        log_entry = {
            "job_id": job_id,
            "status": status,
            "timestamp": None  # 由Cloud Functions自动添加
        }
        
        if data:
            log_entry["data"] = data
        if error:
            log_entry["error"] = error
            
        return json.dumps(log_entry)
