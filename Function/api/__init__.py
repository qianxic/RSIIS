"""
API模块，提供与远程API服务交互的功能
"""

from .api_base import ApiBaseModel
from .api_segmentation import ApiSegmentationModel
from .api_detection import ApiDetectionModel
from .api_classification import ApiClassificationModel
from .api_change_detection import ApiChangeDetectionModel
from .api_batch_processing import ApiBatchProcessingModel

# 导出所有API模型类
__all__ = [
    'ApiBaseModel',
    'ApiSegmentationModel', 
    'ApiDetectionModel', 
    'ApiClassificationModel', 
    'ApiChangeDetectionModel',
    'ApiBatchProcessingModel'
] 