"""
批量处理控制器类，提供遥感影像批量处理功能
"""
import os
import time
import logging
import glob
import json
import csv
import random
import shutil
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PySide6.QtCore import QObject, Qt, Signal, Slot, QTimer
from Function.api.api_batch_processing import ApiBatchProcessingModel

# 移除对API的依赖
# from .api_base_controller import ApiBaseController

class BatchController(QObject):
    """批量处理控制器类"""
    
    # 信号定义
    input_dir_changed = Signal(str)           # 输入目录改变
    output_dir_changed = Signal(str)          # 输出目录改变
    before_dir_changed = Signal(str)          # 前期影像目录改变
    after_dir_changed = Signal(str)           # 后期影像目录改变
    task_created = Signal(str)                # 任务创建
    task_started = Signal(str)                # 任务开始
    task_finished = Signal(str)               # 任务完成
    task_failed = Signal(str, str)            # 任务失败（任务ID，错误信息）
    task_status_changed = Signal(str, str)    # 任务状态改变（任务ID，新状态）
    task_progress_changed = Signal(str, int)  # 任务进度改变（任务ID，进度百分比）
    task_list_changed = Signal(list)          # 任务列表改变
    
    def __init__(self, api_client=None):
        """初始化批量处理控制器"""
        super().__init__()
        
        self.logger = logging.getLogger("BatchController")
        
        # 初始化目录属性
        self.input_dir = ""
        self.output_dir = ""
        self.before_dir = ""
        self.after_dir = ""
        
        # 页面引用
        self.page = None
        
        # 任务映射表
        self.task_types = {
            "segmentation": "语义分割",
            "detection": "目标检测",
            "classification": "场景分类",
            "change_detection": "变化检测"
        }
        
        # 任务状态
        self.task_states = {
            "pending": "等待中",
            "running": "运行中",
            "completed": "已完成",
            "failed": "失败"
        }
        
        # 任务缓存
        self.task_cache = []
        
        # 初始化API模型
        try:
            self.api_model = ApiBatchProcessingModel()
        except Exception as e:
            self.logger.error(f"初始化批量处理API模型失败: {e}")
            self.api_model = None
    
    def setup(self, page=None):
        """设置控制器的页面引用和其他初始化
        
        Args:
            page: 批量处理页面实例
        """
        self.page = page
        self.logger.info("批量处理控制器初始化完成")
        
        # 返回self以支持链式调用
        return self
    
    def set_page(self, page):
        """设置页面引用
        
        Args:
            page: 批量处理页面实例
        """
        self.page = page
        self.logger.info("批量处理页面引用已设置")
        
        # 返回self以支持链式调用
        return self
    
    def _check_directory(self, directory, purpose=""):
        """检查目录是否有效
        
        Args:
            directory: 要检查的目录路径
            purpose: 目录用途描述（用于日志）
            
        Returns:
            bool: 目录是否有效
        """
        if not directory:
            self.logger.warning(f"{purpose}目录未设置")
            return False
            
        if not os.path.exists(directory):
            self.logger.warning(f"{purpose}目录不存在: {directory}")
            return False
            
        if not os.path.isdir(directory):
            self.logger.warning(f"{purpose}路径不是有效目录: {directory}")
            return False
            
        return True
    
    def select_input_directory(self):
        """选择输入目录
        
        Returns:
            tuple: (success, directory_path)
        """
        # 打开文件对话框，选择目录
        directory = QFileDialog.getExistingDirectory(
            None, 
            "选择输入目录", 
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )
        
        if not directory:
            self.logger.info("用户取消了输入目录选择")
            return False, ""
        
        self.input_dir = directory
        self.logger.info(f"已选择输入目录: {directory}")
        
        # 更新UI上的目录标签
        if hasattr(self, "page") and hasattr(self.page, "input_dir_label"):
            self.page.input_dir_label.setText(f"当前输入目录: {directory}")
        
        # 发出信号
        self.input_dir_changed.emit(directory)
        
        # 显示消息框
        QMessageBox.information(None, "目录选择", f"已选择输入目录: {directory}")
        return True, directory
    
    def select_output_directory(self):
        """选择输出目录
        
        Returns:
            tuple: (success, directory_path)
        """
        # 打开文件对话框，选择目录
        directory = QFileDialog.getExistingDirectory(
            None, 
            "选择输出目录", 
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )
        
        if not directory:
            self.logger.info("用户取消了输出目录选择")
            return False, ""
        
        self.output_dir = directory
        self.logger.info(f"已选择输出目录: {directory}")
        
        # 更新UI上的目录标签
        if hasattr(self, "page") and hasattr(self.page, "output_dir_label"):
            self.page.output_dir_label.setText(f"当前输出目录: {directory}")
        
        # 发出信号
        self.output_dir_changed.emit(directory)
        
        # 显示消息框
        QMessageBox.information(None, "目录选择", f"已选择输出目录: {directory}")
        return True, directory
    
    def select_before_directory(self):
        """选择前期影像目录
        
        Returns:
            tuple: (success, directory_path)
        """
        # 打开文件对话框，选择目录
        directory = QFileDialog.getExistingDirectory(
            None, 
            "选择前期影像目录", 
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )
        
        if not directory:
            self.logger.info("用户取消了前期影像目录选择")
            return False, ""
        
        self.before_dir = directory
        self.logger.info(f"已选择前期影像目录: {directory}")
        
        # 更新UI上的目录标签
        if hasattr(self, "page") and hasattr(self.page, "before_dir_label"):
            self.page.before_dir_label.setText(f"当前前期影像目录: {directory}")
        
        # 发出信号
        self.before_dir_changed.emit(directory)
        
        # 显示消息框
        QMessageBox.information(None, "目录选择", f"已选择前期影像目录: {directory}")
        return True, directory
    
    def select_after_directory(self):
        """选择后期影像目录
        
        Returns:
            tuple: (success, directory_path)
        """
        # 打开文件对话框，选择目录
        directory = QFileDialog.getExistingDirectory(
            None, 
            "选择后期影像目录", 
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )
        
        if not directory:
            self.logger.info("用户取消了后期影像目录选择")
            return False, ""
        
        self.after_dir = directory
        self.logger.info(f"已选择后期影像目录: {directory}")
        
        # 更新UI上的目录标签
        if hasattr(self, "page") and hasattr(self.page, "after_dir_label"):
            self.page.after_dir_label.setText(f"当前后期影像目录: {directory}")
        
        # 发出信号
        self.after_dir_changed.emit(directory)
        
        # 显示消息框
        QMessageBox.information(None, "目录选择", f"已选择后期影像目录: {directory}")
        return True, directory
    
    def create_batch_task(self, task_type):
        """开始批量处理任务
        
        Args:
            task_type: 任务类型（"segmentation", "detection", "classification", "change_detection"）
            
        Returns:
            bool: 是否成功启动任务
        """
        if task_type not in self.task_types:
            self.logger.error(f"不支持的任务类型: {task_type}")
            QMessageBox.warning(None, "执行失败", f"不支持的任务类型: {task_type}")
            return False
        
        # 检查必要的目录
        if task_type == "change_detection":
            # 变化检测需要前后期影像目录
            if not self._check_directory(self.before_dir, "前期影像"):
                QMessageBox.warning(None, "目录错误", "请先选择有效的前期影像目录")
                return False
            
            if not self._check_directory(self.after_dir, "后期影像"):
                QMessageBox.warning(None, "目录错误", "请先选择有效的后期影像目录")
                return False
            
            if not self._check_directory(self.output_dir, "输出"):
                QMessageBox.warning(None, "目录错误", "请先选择有效的输出目录")
                return False
        else:
            # 其他任务类型需要输入和输出目录
            if not self._check_directory(self.input_dir, "输入"):
                QMessageBox.warning(None, "目录错误", "请先选择有效的输入目录")
                return False
            
            if not self._check_directory(self.output_dir, "输出"):
                QMessageBox.warning(None, "目录错误", "请先选择有效的输出目录")
                return False
        
        try:
            # 显示进度提示
            QApplication.setOverrideCursor(Qt.WaitCursor)
            
            # 提示用户任务已开始
            QMessageBox.information(
                None, 
                "任务开始", 
                f"正在开始{self.task_types[task_type]}批量处理任务..."
            )
            
            # 直接执行任务
            success = False
            if self.api_model:
                # 根据任务类型调用不同的API执行方法
                if task_type == "segmentation":
                    success = self.api_model.execute_segmentation_task(self.input_dir, self.output_dir)
                elif task_type == "detection":
                    success = self.api_model.execute_detection_task(self.input_dir, self.output_dir)
                elif task_type == "classification":
                    success = self.api_model.execute_classification_task(self.input_dir, self.output_dir)
                elif task_type == "change_detection":
                    success = self.api_model.execute_change_detection_task(
                        self.before_dir, self.after_dir, self.output_dir
                    )
            else:
                # API不可用
                self.logger.error("API服务不可用，无法执行任务")
                QMessageBox.warning(None, "执行失败", "API服务不可用，无法执行任务")
                QApplication.restoreOverrideCursor()
                return False
            
            # 恢复鼠标指针
            QApplication.restoreOverrideCursor()
            
            if success:
                self.logger.info(f"成功执行{self.task_types[task_type]}任务")
                
                # 显示成功消息
                QMessageBox.information(
                    None, 
                    "任务执行成功", 
                    f"{self.task_types[task_type]}任务执行成功！\n结果已保存到: {self.output_dir}"
                )
                return True
            else:
                self.logger.error(f"执行{self.task_types[task_type]}任务失败")
                QMessageBox.warning(None, "执行失败", f"执行{self.task_types[task_type]}任务失败")
                return False
                
        except Exception as e:
            # 恢复鼠标指针
            QApplication.restoreOverrideCursor()
            
            self.logger.error(f"执行任务时发生错误: {e}")
            QMessageBox.warning(None, "执行失败", f"执行任务时发生错误: {str(e)}")
            return False
    
    def start_batch_task(self, task_id):
        """启动批量处理任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            bool: 是否成功启动任务
        """
        # 该方法已被直接执行任务的方法替代
        self.logger.warning("start_batch_task方法已弃用，请使用create_batch_task直接执行任务")
        return False
    
    # 创建方法别名，以便以后修改UI绑定为直接使用start_batch_task
    create_batch_task = create_batch_task
    
    def cleanup(self):
        """清理资源"""
        pass
    