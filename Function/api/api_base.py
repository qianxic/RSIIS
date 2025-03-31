"""
API基础模型类，提供远程API服务调用的基础功能
"""

import os
import logging
from typing import Dict, Any, Optional, List, Tuple


class ApiBaseModel:
    """API基础模型类，提供远程API服务调用的基础功能"""
    
    def __init__(self):
        """初始化API基础模型"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_client = None
        self.config = None
        self.segmentation_task = None
        self.detection_task = None
        self.classification_task = None
        self.change_detection_task = None
        self.last_error = None
        
        # 初始化API客户端
        self._init_api_client()
    
    def _init_api_client(self, config_path: str = None):
        """初始化API客户端
        
        Args:
            config_path: API配置文件路径，如果为None则使用默认路径
        """
        try:
            # 导入API客户端模块
            from utils.api_client import ApiClient, ApiConfig
            from utils.api_client.task_handlers import (
                SegmentationTask, 
                DetectionTask, 
                ClassificationTask, 
                ChangeDetectionTask
            )
            
            # 加载配置
            config_path = config_path or os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                'config', 
                'api_config.json'
            )
            
            # 创建API配置
            self.config = ApiConfig.from_file(config_path)
            
            # 创建API客户端
            self.api_client = ApiClient(self.config)
            
            # 初始化任务处理器
            self.segmentation_task = SegmentationTask(self.api_client)
            self.detection_task = DetectionTask(self.api_client)
            self.classification_task = ClassificationTask(self.api_client)
            self.change_detection_task = ChangeDetectionTask(self.api_client)
            
            self.logger.info("API客户端初始化成功")
            
        except ImportError as e:
            self.logger.error(f"导入API客户端模块失败: {str(e)}")
            self.last_error = f"API客户端模块未安装或路径错误: {str(e)}"
            
        except Exception as e:
            self.logger.error(f"初始化API客户端失败: {str(e)}")
            self.last_error = f"初始化API客户端失败: {str(e)}"
    
    def check_api_availability(self, auto_start: bool = False) -> bool:
        """检查API服务是否可用
        
        Args:
            auto_start: 如果服务不可用，是否尝试启动服务
            
        Returns:
            API服务是否可用
        """
        try:
            if not self.api_client:
                self.logger.warning("API客户端未初始化")
                return False
            
            # 检查API连接
            available = self.api_client.check_connection()
            
            if not available and auto_start:
                self.logger.info("API服务不可用，尝试自动启动")
                # 尝试启动API服务
                started = self.api_client.start_service()
                if started:
                    self.logger.info("API服务已成功启动")
                    # 再次检查连接
                    available = self.api_client.check_connection()
                else:
                    self.logger.error("自动启动API服务失败")
            
            if available:
                self.logger.info("API服务可用")
            else:
                self.logger.warning("API服务不可用")
                
            return available
            
        except Exception as e:
            self.logger.error(f"检查API可用性出错: {str(e)}")
            return False 