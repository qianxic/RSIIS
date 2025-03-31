"""
语义分割API模型，提供影像分割的API接口
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple

from .api_base import ApiBaseModel


class ApiSegmentationModel(ApiBaseModel):
    """语义分割API模型类"""
    
    def __init__(self):
        """初始化语义分割API模型"""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_error = None
    
    def segment_image(self, image_path: str, output_path: str = None,
                     model_name: str = "default", 
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """语义分割单张影像
        
        Args:
            image_path: 影像路径
            output_path: 输出结果路径，为None时不保存结果
            model_name: 模型名称
            params: 其他参数
            
        Returns:
            分割结果
        """
        try:
            if not os.path.exists(image_path):
                self.last_error = f"影像文件不存在: {image_path}"
                return {"success": False, "error": self.last_error}
            
            if not self.check_api_availability():
                self.last_error = "API服务不可用"
                return {"success": False, "error": self.last_error}
            
            # 调用API进行语义分割
            result = self.segmentation_task.segment_image(
                image_path=image_path,
                model_name=model_name,
                params=params or {}
            )
            
            # 如果指定了输出路径，保存结果
            if output_path and result.get("success", False):
                self.save_segmentation_result(result, output_path)
            
            return result
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"语义分割失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的语义分割模型列表
        
        Returns:
            模型列表，每个模型包含名称、描述等信息
        """
        try:
            if not self.check_api_availability():
                return []
            
            # 获取可用模型
            models = self.segmentation_task.get_available_models()
            return models
            
        except Exception as e:
            self.logger.error(f"获取可用模型失败: {str(e)}")
            return []
    
    def save_segmentation_result(self, result: Dict[str, Any], output_path: str) -> bool:
        """保存分割结果到文件
        
        Args:
            result: 分割结果
            output_path: 输出路径
            
        Returns:
            是否成功保存
        """
        try:
            if not result:
                self.last_error = "无有效的分割结果"
                return False
            
            # 保存结果
            self.segmentation_task.save_result(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"保存分割结果失败: {str(e)}")
            return False 