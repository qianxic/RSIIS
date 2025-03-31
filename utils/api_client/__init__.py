"""
API 客户端模块，用于与远程FastAPI服务通信
"""

from .client import ApiClient
from .config import ApiConfig

# 暂时移除任务处理器导入，解决循环导入问题
# from .task_handlers import TaskHandler, SegmentationTask, DetectionTask, ClassificationTask, ChangeDetectionTask

__all__ = [
    'ApiClient',
    'ApiConfig',
    # 'TaskHandler',
    # 'SegmentationTask',
    # 'DetectionTask',
    # 'ClassificationTask',
    # 'ChangeDetectionTask'
] 