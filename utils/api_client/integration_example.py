"""
示例代码：如何在现有控制器中集成API客户端
"""
import os
import logging
from typing import Dict, Any, Optional

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Slot

# 导入API客户端模块
from utils.api_client import (
    ApiClient, 
    ApiConfig, 
    TaskHandler,
    SegmentationTask, 
    DetectionTask,
    ClassificationTask,
    ChangeDetectionTask
)


class ApiControllerMixin:
    """API控制器混入类，提供API相关功能
    
    此混入类可以添加到现有控制器中，以提供API调用功能
    """
    
    def setup_api_client(self, config_path: Optional[str] = None):
        """设置API客户端
        
        Args:
            config_path: API配置文件路径，如果为None则使用默认配置
        """
        if config_path and os.path.exists(config_path):
            self.api_config = ApiConfig.from_file(config_path)
        else:
            self.api_config = ApiConfig.default()
            
        self.api_client = ApiClient(self.api_config)
        
        # 创建任务处理器
        self.segmentation_task = SegmentationTask(self.api_client)
        self.detection_task = DetectionTask(self.api_client)
        self.classification_task = ClassificationTask(self.api_client)
        self.change_detection_task = ChangeDetectionTask(self.api_client)
        
        # 连接信号
        self._connect_task_signals()
    
    def _connect_task_signals(self):
        """连接任务处理器的信号"""
        # 分割任务信号
        self.segmentation_task.task_started.connect(self._on_task_started)
        self.segmentation_task.task_completed.connect(self._on_segmentation_completed)
        self.segmentation_task.task_failed.connect(self._on_task_failed)
        
        # 检测任务信号
        self.detection_task.task_started.connect(self._on_task_started)
        self.detection_task.task_completed.connect(self._on_detection_completed)
        self.detection_task.task_failed.connect(self._on_task_failed)
        
        # 分类任务信号
        self.classification_task.task_started.connect(self._on_task_started)
        self.classification_task.task_completed.connect(self._on_classification_completed)
        self.classification_task.task_failed.connect(self._on_task_failed)
        
        # 变化检测任务信号
        self.change_detection_task.task_started.connect(self._on_task_started)
        self.change_detection_task.task_completed.connect(self._on_change_detection_completed)
        self.change_detection_task.task_failed.connect(self._on_task_failed)
    
    @Slot(str)
    def _on_task_started(self, task_id: str):
        """任务开始处理
        
        Args:
            task_id: 任务ID
        """
        self.logger.info(f"任务开始: {task_id}")
        # 在UI上显示加载状态
        # self.page.show_loading(True, "正在处理...")
    
    @Slot(str, str)
    def _on_task_failed(self, task_id: str, error_msg: str):
        """任务失败处理
        
        Args:
            task_id: 任务ID
            error_msg: 错误信息
        """
        self.logger.error(f"任务失败: {task_id}, 错误: {error_msg}")
        # 隐藏加载状态
        # self.page.show_loading(False)
        
        # 显示错误信息
        QMessageBox.critical(self.page, "任务失败", f"处理失败: {error_msg}")
    
    @Slot(str, dict)
    def _on_segmentation_completed(self, task_id: str, result: Dict[str, Any]):
        """分割任务完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self.logger.info(f"分割任务完成: {task_id}")
        # 隐藏加载状态
        # self.page.show_loading(False)
        
        # 处理分割结果
        # 1. 从结果中获取分割图像URL
        segmentation_url = result.get("segmentation_url")
        if not segmentation_url:
            QMessageBox.warning(self.page, "结果不完整", "未找到分割结果图像")
            return
            
        # 2. 下载分割图像
        try:
            # 为下载的图像创建临时文件路径
            temp_dir = os.path.join(os.path.dirname(__file__), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            segmentation_path = os.path.join(temp_dir, f"segmentation_{task_id}.tif")
            
            # 下载分割图像
            self.api_client.download_file(segmentation_url, segmentation_path)
            
            # 3. 在UI上显示分割结果
            # self.page.display_segmentation_result(segmentation_path)
            
        except Exception as e:
            self.logger.error(f"下载分割结果失败: {str(e)}")
            QMessageBox.warning(self.page, "下载失败", f"下载分割结果失败: {str(e)}")
    
    @Slot(str, dict)
    def _on_detection_completed(self, task_id: str, result: Dict[str, Any]):
        """检测任务完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self.logger.info(f"检测任务完成: {task_id}")
        # 隐藏加载状态
        # self.page.show_loading(False)
        
        # 处理检测结果
        detections = result.get("detections", [])
        if not detections:
            QMessageBox.information(self.page, "检测结果", "未检测到任何目标")
            return
            
        # 在UI上显示检测结果
        # self.page.display_detection_result(detections)
    
    @Slot(str, dict)
    def _on_classification_completed(self, task_id: str, result: Dict[str, Any]):
        """分类任务完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self.logger.info(f"分类任务完成: {task_id}")
        # 隐藏加载状态
        # self.page.show_loading(False)
        
        # 处理分类结果
        classification = result.get("classification", {})
        if not classification:
            QMessageBox.warning(self.page, "结果不完整", "未找到分类结果")
            return
            
        # 获取类别和置信度
        class_name = classification.get("class")
        confidence = classification.get("confidence")
        
        # 在UI上显示分类结果
        # self.page.display_classification_result(class_name, confidence)
    
    @Slot(str, dict)
    def _on_change_detection_completed(self, task_id: str, result: Dict[str, Any]):
        """变化检测任务完成处理
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        self.logger.info(f"变化检测任务完成: {task_id}")
        # 隐藏加载状态
        # self.page.show_loading(False)
        
        # 处理变化检测结果
        change_map_url = result.get("change_map_url")
        if not change_map_url:
            QMessageBox.warning(self.page, "结果不完整", "未找到变化检测结果图像")
            return
            
        # 下载变化检测图像
        try:
            # 为下载的图像创建临时文件路径
            temp_dir = os.path.join(os.path.dirname(__file__), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            change_map_path = os.path.join(temp_dir, f"change_map_{task_id}.tif")
            
            # 下载变化检测图像
            self.api_client.download_file(change_map_url, change_map_path)
            
            # 在UI上显示变化检测结果
            # self.page.display_change_detection_result(change_map_path)
            
        except Exception as e:
            self.logger.error(f"下载变化检测结果失败: {str(e)}")
            QMessageBox.warning(self.page, "下载失败", f"下载变化检测结果失败: {str(e)}")


# 示例：如何在现有控制器中使用API混入类
class ExampleSegmentController:
    """分割控制器示例，展示如何集成API客户端"""
    
    def __init__(self):
        """初始化控制器"""
        self.logger = logging.getLogger("ExampleSegmentController")
        self.page = None
    
    def setup(self, page):
        """设置控制器的页面引用
        
        Args:
            page: 页面实例
        """
        self.page = page
        
        # 初始化API客户端
        # 在实际的控制器子类中，使用混入类的方式
        api_mixin = ApiControllerMixin()
        api_mixin.logger = self.logger
        api_mixin.page = self.page
        api_mixin.setup_api_client()
        
        # 将API混入类的属性和方法复制到当前类
        for attr_name in dir(api_mixin):
            if not attr_name.startswith('_') or attr_name == '_connect_task_signals':
                setattr(self, attr_name, getattr(api_mixin, attr_name))
        
        # 手动连接信号，因为混入时可能不会自动继承Qt的信号连接
        api_mixin._connect_task_signals()
    
    @Slot()
    def on_segment_button_clicked(self):
        """分割按钮点击事件处理"""
        # 获取当前选择的图像路径
        image_path = self.page.get_selected_image_path()
        if not image_path:
            QMessageBox.warning(self.page, "错误", "请先选择一张图像")
            return
        
        # 获取分割参数
        model_name = self.page.get_selected_model()
        params = {
            "threshold": self.page.get_threshold_value()
        }
        
        try:
            # 提交分割任务并等待结果
            self.segmentation_task.submit_task(
                image_path=image_path,
                model_name=model_name,
                params=params
            )
        except Exception as e:
            self.logger.error(f"提交分割任务失败: {str(e)}")
            QMessageBox.critical(self.page, "错误", f"提交任务失败: {str(e)}") 