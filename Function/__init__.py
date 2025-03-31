"""
Function模块 - 包含系统功能实现

主要包括：
1. api - API实现模块，提供与远程API服务的交互
2. analysis - 已迁移到API实现，仅保留用于兼容性
3. data - 数据处理相关功能
4. base - 基础功能实现
"""

# 导出API实现
from .api import (
    ApiSegmentationModel, 
    ApiDetectionModel, 
    ApiClassificationModel, 
    ApiChangeDetectionModel,
    ApiBatchProcessingModel
)

__all__ = [
    'ApiSegmentationModel', 
    'ApiDetectionModel', 
    'ApiClassificationModel', 
    'ApiChangeDetectionModel',
    'ApiBatchProcessingModel'
] 