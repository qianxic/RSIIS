"""
API基础控制器类，为其他控制器提供API调用功能
"""
import os
import logging
from typing import Dict, Any, Optional, Tuple

from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QObject, Slot, Qt

# 导入API客户端模块
from utils.api_client import ApiClient, ApiConfig

# 从task_handlers直接导入，避免循环导入
from utils.api_client.task_handlers import (
    SegmentationTask, 
    DetectionTask,
    ClassificationTask,
    ChangeDetectionTask
)

# 导入Docker管理工具
from utils.api_client.docker_utils import ensure_api_service

# 定义ApiError以解决启动问题
class ApiError(Exception):
    """API调用异常"""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

class ApiBaseController(QObject):
    """API基础控制器类
    
    为控制器提供访问远程API服务的功能。
    此类可以被继承或作为混入类使用。
    """
    
    def __init__(self, parent=None):
        """初始化API基础控制器"""
        super().__init__(parent)
        self.api_client = None
        self.api_config = None
        
        # 任务处理器
        self.segmentation_task = None
        self.detection_task = None
        self.classification_task = None
        self.change_detection_task = None
        
        # 任务执行中标志
        self.is_task_running = False
        
        # 日志记录器
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # UI页面引用
        self.page = None
    
    def setup_api(self, page=None, config_path: Optional[str] = None):
        """设置API客户端
        
        Args:
            page: UI页面引用
            config_path: API配置文件路径
        """
        self.page = page
        
        # 加载API配置
        if config_path and os.path.exists(config_path):
            self.api_config = ApiConfig.from_file(config_path)
        else:
            # 尝试从默认位置加载
            default_config = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "utils", "api_client", "api_config.json"
            )
            if os.path.exists(default_config):
                self.api_config = ApiConfig.from_file(default_config)
            else:
                self.api_config = ApiConfig.default()
        
        # 创建API客户端
        self.api_client = ApiClient(self.api_config)
        
        # 创建任务处理器
        self.segmentation_task = SegmentationTask(self.api_client)
        self.detection_task = DetectionTask(self.api_client)
        self.classification_task = ClassificationTask(self.api_client)
        self.change_detection_task = ChangeDetectionTask(self.api_client)
        
        # 连接信号
        self._connect_task_signals()
        
        self.logger.info(f"API客户端已设置, 连接到 {self.api_config.base_endpoint}")
        
        # 检查API服务可用性
        self.check_api_availability(show_message=False)
    
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
        """任务开始回调
        
        Args:
            task_id: 任务ID
        """
        self.logger.info(f"任务开始: {task_id}")
        self.is_task_running = True
        
        # 显示加载中状态
        QApplication.setOverrideCursor(Qt.WaitCursor)
        
        # 如果页面有loading组件，调用显示loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(True, "正在处理...")
    
    @Slot(str, str)
    def _on_task_failed(self, task_id: str, error_msg: str):
        """任务失败回调
        
        Args:
            task_id: 任务ID
            error_msg: 错误信息
        """
        self.logger.error(f"任务失败: {task_id}, 错误: {error_msg}")
        self.is_task_running = False
        
        # 恢复光标
        QApplication.restoreOverrideCursor()
        
        # 如果页面有loading组件，隐藏loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(False)
            
        # 显示错误信息
        QMessageBox.critical(self.page or None, "任务失败", f"处理失败: {error_msg}")
    
    @Slot(str, dict)
    def _on_segmentation_completed(self, task_id: str, result: Dict[str, Any]):
        """分割任务完成回调
        
        Args:
            task_id: 任务ID
            result: 任务结果数据
        """
        self.logger.info(f"分割任务完成: {task_id}")
        self.is_task_running = False
        
        # 恢复光标
        QApplication.restoreOverrideCursor()
        
        # 如果页面有loading组件，隐藏loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(False)
        
        # 处理分割结果
        # 1. 从结果中获取分割图像URL
        segmentation_url = result.get("segmentation_url")
        if not segmentation_url:
            QMessageBox.warning(self.page or None, "结果不完整", "未找到分割结果图像")
            return
            
        # 2. 下载分割图像
        try:
            # 为下载的图像创建临时文件路径
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "utils", "api_client", "temp")
            os.makedirs(temp_dir, exist_ok=True)
            segmentation_path = os.path.join(temp_dir, f"segmentation_{task_id}.tif")
            
            # 下载分割图像
            self.api_client.download_file(segmentation_url, segmentation_path)
            
            # 3. 在UI上显示分割结果
            if hasattr(self.page, 'display_segmentation_result') and callable(getattr(self.page, 'display_segmentation_result')):
                self.page.display_segmentation_result(segmentation_path)
            else:
                QMessageBox.information(self.page or None, "分割完成", f"分割结果已保存到：{segmentation_path}")
            
        except Exception as e:
            self.logger.error(f"下载分割结果失败: {str(e)}")
            QMessageBox.warning(self.page or None, "下载失败", f"下载分割结果失败: {str(e)}")
    
    @Slot(str, dict)
    def _on_detection_completed(self, task_id: str, result: Dict[str, Any]):
        """检测任务完成回调
        
        Args:
            task_id: 任务ID
            result: 任务结果数据
        """
        self.logger.info(f"检测任务完成: {task_id}")
        self.is_task_running = False
        
        # 恢复光标
        QApplication.restoreOverrideCursor()
        
        # 如果页面有loading组件，隐藏loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(False)
        
        # 处理检测结果
        detections = result.get("detections", [])
        if not detections:
            QMessageBox.information(self.page or None, "检测结果", "未检测到任何目标")
            return
            
        # 在UI上显示检测结果
        if hasattr(self.page, 'display_detection_result') and callable(getattr(self.page, 'display_detection_result')):
            self.page.display_detection_result(detections)
        else:
            # 格式化检测结果
            detection_summary = f"检测到 {len(detections)} 个目标:\n\n"
            for i, det in enumerate(detections[:5], 1):  # 只显示前5个
                cls = det.get("class", "未知")
                conf = det.get("confidence", 0) * 100
                detection_summary += f"{i}. 类别: {cls}, 置信度: {conf:.2f}%\n"
                
            if len(detections) > 5:
                detection_summary += f"\n... 还有 {len(detections) - 5} 个目标未显示"
                
            QMessageBox.information(self.page or None, "检测完成", detection_summary)
    
    @Slot(str, dict)
    def _on_classification_completed(self, task_id: str, result: Dict[str, Any]):
        """分类任务完成回调
        
        Args:
            task_id: 任务ID
            result: 任务结果数据
        """
        self.logger.info(f"分类任务完成: {task_id}")
        self.is_task_running = False
        
        # 恢复光标
        QApplication.restoreOverrideCursor()
        
        # 如果页面有loading组件，隐藏loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(False)
        
        # 处理分类结果
        classification = result.get("classification", {})
        if not classification:
            QMessageBox.warning(self.page or None, "结果不完整", "未找到分类结果")
            return
            
        # 获取类别和置信度
        class_name = classification.get("class", "未知")
        confidence = classification.get("confidence", 0) * 100
        
        # 在UI上显示分类结果
        if hasattr(self.page, 'display_classification_result') and callable(getattr(self.page, 'display_classification_result')):
            self.page.display_classification_result(class_name, confidence)
        else:
            QMessageBox.information(self.page or None, "分类完成", 
                                  f"分类结果:\n类别: {class_name}\n置信度: {confidence:.2f}%")
    
    @Slot(str, dict)
    def _on_change_detection_completed(self, task_id: str, result: Dict[str, Any]):
        """变化检测任务完成回调
        
        Args:
            task_id: 任务ID
            result: 任务结果数据
        """
        self.logger.info(f"变化检测任务完成: {task_id}")
        self.is_task_running = False
        
        # 恢复光标
        QApplication.restoreOverrideCursor()
        
        # 如果页面有loading组件，隐藏loading
        if hasattr(self.page, 'show_loading') and callable(getattr(self.page, 'show_loading')):
            self.page.show_loading(False)
        
        # 处理变化检测结果
        change_map_url = result.get("change_map_url")
        if not change_map_url:
            QMessageBox.warning(self.page or None, "结果不完整", "未找到变化检测结果图像")
            return
            
        # 下载变化检测图像
        try:
            # 为下载的图像创建临时文件路径
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "utils", "api_client", "temp")
            os.makedirs(temp_dir, exist_ok=True)
            change_map_path = os.path.join(temp_dir, f"change_map_{task_id}.tif")
            
            # 下载变化检测图像
            self.api_client.download_file(change_map_url, change_map_path)
            
            # 在UI上显示变化检测结果
            if hasattr(self.page, 'display_change_detection_result') and callable(getattr(self.page, 'display_change_detection_result')):
                self.page.display_change_detection_result(change_map_path)
            else:
                QMessageBox.information(self.page or None, "变化检测完成", f"变化检测结果已保存到：{change_map_path}")
            
        except Exception as e:
            self.logger.error(f"下载变化检测结果失败: {str(e)}")
            QMessageBox.warning(self.page or None, "下载失败", f"下载变化检测结果失败: {str(e)}")
    
    def check_api_availability(self, auto_start: bool = True, show_message: bool = True) -> bool:
        """检查API服务可用性
        
        Args:
            auto_start: 如果API服务不可用，是否尝试启动
            show_message: 是否显示消息对话框
            
        Returns:
            如果API服务可用，返回True，否则返回False
        """
        if not self.api_client:
            self.logger.warning("API客户端未初始化")
            return False
        
        # 首先使用API客户端检查
        try:
            # 尝试ping API服务
            result = self.api_client.get("/ping")
            self.logger.info(f"API服务可用: {result}")
            if show_message:
                QMessageBox.information(self.page or None, "API服务状态", "API服务已连接并可用")
            return True
        except ApiError:
            pass
        except Exception as e:
            self.logger.error(f"检查API时发生未知错误: {str(e)}")
        
        # 如果API客户端检查失败，尝试使用Docker工具
        if auto_start:
            self.logger.info("尝试启动API服务...")
            
            # 设置等待光标
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            try:
                # 尝试确保API服务可用
                available, error = ensure_api_service(
                    host=self.api_config.host,
                    port=self.api_config.port
                )
                
                # 恢复光标
                QApplication.restoreOverrideCursor()
                
                if available:
                    self.logger.info("API服务已成功启动")
                    if show_message:
                        QMessageBox.information(self.page or None, "API服务状态", "API服务已成功启动")
                    return True
                else:
                    self.logger.error(f"无法启动API服务: {error}")
                    if show_message:
                        QMessageBox.critical(self.page or None, "API服务状态", f"无法启动API服务: {error}")
                    return False
            except Exception as e:
                self.logger.error(f"启动API服务时发生错误: {str(e)}")
                if show_message:
                    QMessageBox.critical(self.page or None, "API服务状态", f"启动API服务时发生错误: {str(e)}")
                return False
            finally:
                # 确保光标被恢复
                QApplication.restoreOverrideCursor()
        else:
            if show_message:
                QMessageBox.warning(self.page or None, "API服务状态", "API服务不可用")
            return False 