"""
目标检测API模型类，提供与远程API服务的目标检测功能交互
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple

from .api_base import ApiBaseModel


class ApiDetectionModel(ApiBaseModel):
    """目标检测API模型类，提供遥感影像目标检测的API集成"""
    
    def __init__(self):
        """初始化目标检测API模型"""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_error = None
    
    def detect_objects(self, image_path: str, model_name: str = "default", 
                     confidence: float = 0.5, 
                     params: Dict[str, Any] = None) -> Tuple[bool, Dict[str, Any]]:
        """对单张遥感影像进行目标检测
        
        Args:
            image_path: 影像路径
            model_name: 模型名称
            confidence: 置信度阈值
            params: 其他模型参数
            
        Returns:
            (成功标志, 检测结果或错误信息)
        """
        try:
            if not os.path.exists(image_path):
                self.last_error = f"影像文件不存在: {image_path}"
                return False, {"error": self.last_error}
            
            if not self.check_api_availability():
                self.last_error = "API服务不可用"
                return False, {"error": self.last_error}
            
            # 准备参数
            detection_params = params or {}
            detection_params["confidence"] = confidence
            
            # 调用API进行目标检测
            result = self.detection_task.detect_objects(
                image_path=image_path,
                model_name=model_name,
                params=detection_params
            )
            
            return True, result
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"目标检测失败: {str(e)}")
            return False, {"error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的目标检测模型列表
        
        Returns:
            模型列表，每个模型包含名称、描述等信息
        """
        try:
            if not self.check_api_availability():
                return []
            
            # 获取可用模型
            models = self.detection_task.get_available_models()
            return models
            
        except Exception as e:
            self.logger.error(f"获取可用模型失败: {str(e)}")
            return []
    
    def save_detection_result(self, result: Dict[str, Any], output_path: str) -> bool:
        """保存检测结果到文件
        
        Args:
            result: 检测结果
            output_path: 输出路径
            
        Returns:
            是否成功保存
        """
        try:
            if not result:
                self.last_error = "无有效的检测结果"
                return False
            
            # 保存结果
            self.detection_task.save_result(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"保存检测结果失败: {str(e)}")
            return False
    
    def export_objects_to_shapefile(self, result: Dict[str, Any], output_path: str) -> bool:
        """将检测到的目标导出为Shapefile格式
        
        Args:
            result: 检测结果
            output_path: 输出路径
            
        Returns:
            是否成功导出
        """
        try:
            if not result:
                self.last_error = "无有效的检测结果"
                return False
            
            # 导出为Shapefile
            self.detection_task.export_to_shapefile(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"导出目标为Shapefile失败: {str(e)}")
            return False 