import requests
import os
from typing import Dict, Any, Optional

class NASAClient:
    """NASA API HTTP客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NASA_API_KEY", "DEMO_KEY")
        self.base_url = "https://api.nasa.gov"
        self.session = requests.Session()
        self.session.params = {"api_key": self.api_key}
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送GET请求到NASA API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_apod(self, date: Optional[str] = None) -> Dict[str, Any]:
        """获取每日天文图片"""
        params = {"date": date} if date else {}
        return self.get("planetary/apod", params)
    
    def get_asteroids_neows(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """获取近地小行星数据"""
        return self.get("neo/rest/v1/feed", {
            "start_date": start_date,
            "end_date": end_date
        })
