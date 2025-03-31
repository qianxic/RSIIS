"""
API配置模块，管理API连接参数
"""
import os
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ApiConfig:
    """API配置类，管理API连接参数"""
    host: str
    port: int
    base_url: str = ""
    api_key: str = ""
    timeout: int = 30
    use_ssl: bool = False
    
    @property
    def base_endpoint(self) -> str:
        """获取API基础URL"""
        protocol = "https" if self.use_ssl else "http"
        return f"{protocol}://{self.host}:{self.port}{self.base_url}"
    
    @classmethod
    def from_file(cls, config_path: str) -> 'ApiConfig':
        """从配置文件加载API配置"""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"API配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return cls(
            host=config_data.get('host', 'localhost'),
            port=config_data.get('port', 8000),
            base_url=config_data.get('base_url', ''),
            api_key=config_data.get('api_key', ''),
            timeout=config_data.get('timeout', 30),
            use_ssl=config_data.get('use_ssl', False)
        )
    
    @classmethod
    def default(cls) -> 'ApiConfig':
        """获取默认API配置"""
        return cls(
            host="localhost",
            port=8000,
            base_url="/api/v1"
        ) 