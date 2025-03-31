"""
任务处理器模块，定义与API服务通信的任务处理类
"""
import os
import logging
from abc import ABC, abstractmethod, ABCMeta
from typing import Dict, Any, Optional, List, Tuple, Union
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Qt

from .client import ApiClient, ApiError
from .config import ApiConfig


# 创建一个自定义元类来解决ABC和QObject的元类冲突
class TaskHandlerMeta(type(QObject), ABCMeta):
    """解决QObject和ABC元类冲突的自定义元类"""
    pass


class TaskHandler(QObject, metaclass=TaskHandlerMeta):
    """任务处理器基类"""
    
    # 定义信号
    task_started = Signal(str)
    task_progress = Signal(str, int)  # 任务ID, 进度百分比
    task_completed = Signal(str, dict)  # 任务ID, 结果数据
    task_failed = Signal(str, str)  # 任务ID, 错误信息
    
    def __init__(self, api_client: Optional[ApiClient] = None):
        """初始化任务处理器
        
        Args:
            api_client: API客户端实例，如果为None则创建新实例
        """
        super().__init__()
        self.api_client = api_client or ApiClient()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def submit_task(self, *args, **kwargs) -> str:
        """提交任务到API服务
        
        Returns:
            任务ID
        """
        pass
    
    @abstractmethod
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """获取任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务结果数据
        """
        pass
    
    def execute_task(self, *args, **kwargs) -> Dict[str, Any]:
        """执行任务并等待结果
        
        Returns:
            任务结果数据
        """
        # 提交任务
        task_id = self.submit_task(*args, **kwargs)
        self.task_started.emit(task_id)
        
        try:
            # 等待任务完成
            result = self.api_client.wait_for_task(task_id)
            self.task_completed.emit(task_id, result)
            return result
        except ApiError as e:
            self.task_failed.emit(task_id, str(e))
            raise e


class SegmentationTask(TaskHandler):
    """影像分割任务处理器"""
    
    def submit_task(self, image_path: str, model_name: str = "default", 
                   params: Optional[Dict[str, Any]] = None) -> str:
        """提交分割任务
        
        Args:
            image_path: 影像路径
            model_name: 模型名称
            params: 其他参数
            
        Returns:
            任务ID
        """
        self.logger.info(f"提交分割任务: {image_path}, 模型: {model_name}")
        
        # 准备请求数据
        data = {
            "model_name": model_name
        }
        
        if params:
            data.update(params)
        
        # 上传文件并提交任务
        result = self.api_client.upload_file(
            "/tasks/segmentation",
            file_path=image_path,
            additional_data=data
        )
        
        # 返回任务ID
        task_id = result.get("task_id")
        if not task_id:
            raise ApiError("无法获取任务ID", details=result)
            
        return task_id
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """获取分割任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            分割结果数据，包含分割图像URL
        """
        return self.api_client.get(f"/tasks/segmentation/{task_id}")


class DetectionTask(TaskHandler):
    """目标检测任务处理器"""
    
    def submit_task(self, image_path: str, model_name: str = "default", 
                   confidence: float = 0.5, 
                   params: Optional[Dict[str, Any]] = None) -> str:
        """提交目标检测任务
        
        Args:
            image_path: 影像路径
            model_name: 模型名称
            confidence: 置信度阈值
            params: 其他参数
            
        Returns:
            任务ID
        """
        self.logger.info(f"提交目标检测任务: {image_path}, 模型: {model_name}")
        
        # 准备请求数据
        data = {
            "model_name": model_name,
            "confidence": confidence
        }
        
        if params:
            data.update(params)
        
        # 上传文件并提交任务
        result = self.api_client.upload_file(
            "/tasks/detection",
            file_path=image_path,
            additional_data=data
        )
        
        # 返回任务ID
        task_id = result.get("task_id")
        if not task_id:
            raise ApiError("无法获取任务ID", details=result)
            
        return task_id
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """获取目标检测任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            检测结果数据，包含检测框、类别和置信度
        """
        return self.api_client.get(f"/tasks/detection/{task_id}")


class ClassificationTask(TaskHandler):
    """场景分类任务处理器"""
    
    def submit_task(self, image_path: str, model_name: str = "default", 
                   params: Optional[Dict[str, Any]] = None) -> str:
        """提交场景分类任务
        
        Args:
            image_path: 影像路径
            model_name: 模型名称
            params: 其他参数
            
        Returns:
            任务ID
        """
        self.logger.info(f"提交场景分类任务: {image_path}, 模型: {model_name}")
        
        # 准备请求数据
        data = {
            "model_name": model_name
        }
        
        if params:
            data.update(params)
        
        # 上传文件并提交任务
        result = self.api_client.upload_file(
            "/tasks/classification",
            file_path=image_path,
            additional_data=data
        )
        
        # 返回任务ID
        task_id = result.get("task_id")
        if not task_id:
            raise ApiError("无法获取任务ID", details=result)
            
        return task_id
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """获取场景分类任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            分类结果数据，包含类别和置信度
        """
        return self.api_client.get(f"/tasks/classification/{task_id}")


class ChangeDetectionTask(TaskHandler):
    """变化检测任务处理器"""
    
    def submit_task(self, before_image_path: str, after_image_path: str, 
                   model_name: str = "default", 
                   params: Optional[Dict[str, Any]] = None) -> str:
        """提交变化检测任务
        
        Args:
            before_image_path: 变化前影像路径
            after_image_path: 变化后影像路径
            model_name: 模型名称
            params: 其他参数
            
        Returns:
            任务ID
        """
        self.logger.info(f"提交变化检测任务: {before_image_path} -> {after_image_path}, 模型: {model_name}")
        
        # 准备请求数据
        data = {
            "model_name": model_name
        }
        
        if params:
            data.update(params)
        
        # 上传文件并提交任务
        files = {
            "before_image": (os.path.basename(before_image_path), open(before_image_path, "rb"), "application/octet-stream"),
            "after_image": (os.path.basename(after_image_path), open(after_image_path, "rb"), "application/octet-stream")
        }
        
        try:
            result = self.api_client.post(
                "/tasks/change_detection",
                data=data,
                files=files
            )
        finally:
            # 确保文件被关闭
            for file_obj in files.values():
                file_obj[1].close()
        
        # 返回任务ID
        task_id = result.get("task_id")
        if not task_id:
            raise ApiError("无法获取任务ID", details=result)
            
        return task_id
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """获取变化检测任务结果
        
        Args:
            task_id: 任务ID
            
        Returns:
            变化检测结果数据，包含变化区域图像URL
        """
        return self.api_client.get(f"/tasks/change_detection/{task_id}") 