"""
场景分类API模型类，提供与远程API服务的场景分类功能交互
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple

from .api_base import ApiBaseModel


class ApiClassificationModel(ApiBaseModel):
    """场景分类API模型类，提供遥感影像场景分类的API集成"""
    
    def __init__(self):
        """初始化场景分类API模型"""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_error = None
    
    def classify_image(self, image_path: str, model_name: str = "default", 
                     params: Dict[str, Any] = None) -> Tuple[bool, Dict[str, Any]]:
        """对单张遥感影像进行场景分类
        
        Args:
            image_path: 影像路径
            model_name: 模型名称
            params: 模型参数
            
        Returns:
            (成功标志, 分类结果或错误信息)
        """
        try:
            if not os.path.exists(image_path):
                self.last_error = f"影像文件不存在: {image_path}"
                return False, {"error": self.last_error}
            
            if not self.check_api_availability():
                self.last_error = "API服务不可用"
                return False, {"error": self.last_error}
            
            # 调用API进行场景分类
            result = self.classification_task.classify_image(
                image_path=image_path,
                model_name=model_name,
                params=params or {}
            )
            
            return True, result
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"场景分类失败: {str(e)}")
            return False, {"error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的场景分类模型列表
        
        Returns:
            模型列表，每个模型包含名称、描述等信息
        """
        try:
            if not self.check_api_availability():
                return []
            
            # 获取可用模型
            models = self.classification_task.get_available_models()
            return models
            
        except Exception as e:
            self.logger.error(f"获取可用模型失败: {str(e)}")
            return []
    
    def save_classification_result(self, result: Dict[str, Any], output_path: str) -> bool:
        """保存分类结果到文件
        
        Args:
            result: 分类结果
            output_path: 输出路径
            
        Returns:
            是否成功保存
        """
        try:
            if not result:
                self.last_error = "无有效的分类结果"
                return False
            
            # 保存结果
            self.classification_task.save_result(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"保存分类结果失败: {str(e)}")
            return False 