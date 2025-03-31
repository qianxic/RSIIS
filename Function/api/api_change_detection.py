"""
变化检测API模型类，提供与远程API服务的变化检测功能交互
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple

from .api_base import ApiBaseModel


class ApiChangeDetectionModel(ApiBaseModel):
    """变化检测API模型类，提供遥感影像变化检测的API集成"""
    
    def __init__(self):
        """初始化变化检测API模型"""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_error = None
    
    def detect_changes(self, before_image_path: str, after_image_path: str, 
                     model_name: str = "default", 
                     params: Dict[str, Any] = None) -> Tuple[bool, Dict[str, Any]]:
        """对单对遥感影像进行变化检测
        
        Args:
            before_image_path: 前期影像路径
            after_image_path: 后期影像路径
            model_name: 模型名称
            params: 模型参数
            
        Returns:
            (成功标志, 检测结果或错误信息)
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(before_image_path):
                self.last_error = f"前期影像文件不存在: {before_image_path}"
                return False, {"error": self.last_error}
                
            if not os.path.exists(after_image_path):
                self.last_error = f"后期影像文件不存在: {after_image_path}"
                return False, {"error": self.last_error}
            
            # 检查API是否可用
            if not self.check_api_availability():
                self.last_error = "API服务不可用"
                return False, {"error": self.last_error}
            
            # 调用API进行变化检测
            result = self.change_detection_task.detect_changes(
                before_image_path=before_image_path,
                after_image_path=after_image_path,
                model_name=model_name,
                params=params or {}
            )
            
            return True, result
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"变化检测失败: {str(e)}")
            return False, {"error": str(e)}
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """获取可用的变化检测模型列表
        
        Returns:
            模型列表，每个模型包含名称、描述等信息
        """
        try:
            if not self.check_api_availability():
                return []
            
            # 获取可用模型
            models = self.change_detection_task.get_available_models()
            return models
            
        except Exception as e:
            self.logger.error(f"获取可用模型失败: {str(e)}")
            return []
    
    def save_change_detection_result(self, result: Dict[str, Any], output_path: str) -> bool:
        """保存变化检测结果到文件
        
        Args:
            result: 变化检测结果
            output_path: 输出路径
            
        Returns:
            是否成功保存
        """
        try:
            if not result:
                self.last_error = "无有效的变化检测结果"
                return False
            
            # 保存结果
            self.change_detection_task.save_result(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"保存变化检测结果失败: {str(e)}")
            return False
    
    def get_change_statistics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """获取变化检测统计信息
        
        Args:
            result: 变化检测结果
            
        Returns:
            变化统计信息，包括变化面积、变化率等
        """
        try:
            if not result:
                return {"error": "无有效的变化检测结果"}
            
            # 获取统计信息
            stats = self.change_detection_task.get_statistics(result)
            return stats
            
        except Exception as e:
            self.logger.error(f"获取变化统计信息失败: {str(e)}")
            return {"error": str(e)}
    
    def export_changes_to_shapefile(self, result: Dict[str, Any], output_path: str) -> bool:
        """将检测到的变化区域导出为Shapefile格式
        
        Args:
            result: 变化检测结果
            output_path: 输出路径
            
        Returns:
            是否成功导出
        """
        try:
            if not result:
                self.last_error = "无有效的变化检测结果"
                return False
            
            # 导出为Shapefile
            self.change_detection_task.export_to_shapefile(result, output_path)
            return True
            
        except Exception as e:
            self.last_error = str(e)
            self.logger.error(f"导出变化区域为Shapefile失败: {str(e)}")
            return False 