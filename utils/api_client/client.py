"""
API客户端，处理与FastAPI服务的HTTP通信
"""
import json
import time
import logging
from typing import Dict, Any, Optional, Union, List, Tuple

import requests
from requests.exceptions import RequestException

from .config import ApiConfig


class ApiError(Exception):
    """API调用错误"""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class ApiClient:
    """API客户端，管理与远程API服务的通信"""
    
    def __init__(self, config: ApiConfig = None):
        """初始化API客户端
        
        Args:
            config: API配置，如果为None则使用默认配置
        """
        self.config = config or ApiConfig.default()
        self.logger = logging.getLogger("ApiClient")
        self.session = requests.Session()
        
        # 如果有API密钥，添加到请求头
        if self.config.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.config.api_key}"})
    
    def _make_url(self, endpoint: str) -> str:
        """构建完整的API URL
        
        Args:
            endpoint: API端点路径
            
        Returns:
            完整的API URL
        """
        # 确保endpoint以/开头
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
            
        return f"{self.config.base_endpoint}{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理API响应
        
        Args:
            response: 请求响应对象
            
        Returns:
            API响应数据
            
        Raises:
            ApiError: 当API返回错误时
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise ApiError("无法解析API响应", response.status_code, response.text)
        except requests.exceptions.HTTPError:
            error_msg = "API请求失败"
            details = None
            
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_msg = error_data.get('detail', error_msg)
                    details = error_data
            except:
                details = response.text
                
            raise ApiError(error_msg, response.status_code, details)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """发送GET请求
        
        Args:
            endpoint: API端点
            params: 查询参数
            
        Returns:
            API响应数据
        """
        url = self._make_url(endpoint)
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            return self._handle_response(response)
        except RequestException as e:
            raise ApiError(f"GET请求失败: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             files: Optional[Dict[str, Tuple[str, bytes, str]]] = None) -> Dict[str, Any]:
        """发送POST请求
        
        Args:
            endpoint: API端点
            data: 请求数据
            files: 上传的文件
            
        Returns:
            API响应数据
        """
        url = self._make_url(endpoint)
        try:
            # 如果有文件上传，不要JSON编码
            if files:
                response = self.session.post(
                    url,
                    data=data,
                    files=files,
                    timeout=self.config.timeout
                )
            else:
                response = self.session.post(
                    url,
                    json=data,
                    timeout=self.config.timeout
                )
            return self._handle_response(response)
        except RequestException as e:
            raise ApiError(f"POST请求失败: {str(e)}")
    
    def upload_file(self, endpoint: str, file_path: str, 
                   file_param_name: str = "file", 
                   additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """上传文件到API
        
        Args:
            endpoint: API端点
            file_path: 文件路径
            file_param_name: 文件参数名称
            additional_data: 附加表单数据
            
        Returns:
            API响应数据
        """
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                
            files = {file_param_name: (file_path.split('/')[-1], file_content, 'application/octet-stream')}
            return self.post(endpoint, data=additional_data, files=files)
        except IOError as e:
            raise ApiError(f"文件上传失败: {str(e)}")
    
    def download_file(self, endpoint: str, save_path: str, 
                     params: Optional[Dict[str, Any]] = None) -> str:
        """从API下载文件
        
        Args:
            endpoint: API端点
            save_path: 保存文件的路径
            params: 查询参数
            
        Returns:
            下载文件的本地路径
        """
        url = self._make_url(endpoint)
        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout,
                stream=True
            )
            
            if response.status_code != 200:
                error_msg = f"文件下载失败: HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and 'detail' in error_data:
                        error_msg = error_data['detail']
                except:
                    pass
                raise ApiError(error_msg, response.status_code)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return save_path
        except RequestException as e:
            raise ApiError(f"文件下载失败: {str(e)}")
    
    def wait_for_task(self, task_id: str, check_interval: int = 2, 
                     max_wait_time: int = 3600) -> Dict[str, Any]:
        """等待任务完成
        
        Args:
            task_id: 任务ID
            check_interval: 检查间隔时间(秒)
            max_wait_time: 最大等待时间(秒)
            
        Returns:
            任务结果
        """
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_wait_time:
                raise ApiError(f"等待任务超时: {task_id}", details={"elapsed_time": elapsed_time})
            
            task_info = self.get(f"/tasks/{task_id}")
            status = task_info.get("status")
            
            if status == "completed":
                return task_info.get("result", {})
            elif status == "failed":
                error_details = task_info.get("error", "未知错误")
                raise ApiError(f"任务执行失败: {error_details}", details=task_info)
            
            time.sleep(check_interval) 