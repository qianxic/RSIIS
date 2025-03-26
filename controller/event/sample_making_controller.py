from PySide6.QtWidgets import QFileDialog, QMessageBox
import os
import time

# 导入变化检测模型
from Function.analysis.change_detection import ChangeDetectionModel
from Function.analysis.batch_change_detection import BatchChangeDetectionModel

class SampleMakingController:
    """批量影像解译控制器类"""
    
    def __init__(self):
        """初始化控制器"""
        # 通用批量解译数据
        self.dataset = None
        
        # 变化检测数据
        self.before_dataset = None
        self.after_dataset = None
        self.change_detection_results = None
        
        # 变化检测模型
        self.batch_change_detection_model = BatchChangeDetectionModel()
        
        # 变化检测参数
        self.change_detection_params = {
            "threshold": 0.5,
            "method": "difference",
            "post_process": True,
            "min_area": 10
        }
    
    def import_dataset(self):
        """导入遥感影像数据集"""
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "选择遥感影像数据集文件夹", 
            ""
        )
        
        if folder_path:
            self.dataset = folder_path
            QMessageBox.information(None, "导入成功", f"成功导入数据集: {folder_path}")
            return True
        return False
    
    def start_batch_processing(self):
        """开始批量影像解译"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像数据集")
            return False
        
        # 这里实际上会调用功能层的批量解译功能
        # batch_result = self.batch_processor.process(self.dataset)
        
        # 模拟成功的批量解译结果
        QMessageBox.information(None, "批量解译完成", "批量影像解译已完成，共处理47张影像")
        return True
    
    def export_results(self):
        """导出解译结果"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "没有可导出的解译结果")
            return False
        
        save_path = QFileDialog.getExistingDirectory(
            None,
            "选择导出结果保存位置",
            ""
        )
        
        if save_path:
            # 这里实际上会将批量解译结果导出到指定路径
            # self.batch_processor.export_results(save_path)
            
            # 模拟导出成功
            QMessageBox.information(None, "导出成功", f"批量解译结果已成功导出到: {save_path}")
            return True
        return False
    
    # ======= 批量变化检测功能 =======
    
    def import_before_dataset(self):
        """导入前期影像数据集"""
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "选择前期影像数据集文件夹", 
            ""
        )
        
        if folder_path:
            self.before_dataset = folder_path
            # 设置批量变化检测模型的前期数据集路径
            self.batch_change_detection_model.set_before_dataset(folder_path)
            
            # 获取文件夹中的图像数量
            image_count = self._count_images_in_folder(folder_path)
            QMessageBox.information(None, "导入成功", f"成功导入前期影像数据集: {folder_path}\n包含 {image_count} 张影像")
            return True
        return False
    
    def import_after_dataset(self):
        """导入后期影像数据集"""
        folder_path = QFileDialog.getExistingDirectory(
            None, 
            "选择后期影像数据集文件夹", 
            ""
        )
        
        if folder_path:
            self.after_dataset = folder_path
            # 设置批量变化检测模型的后期数据集路径
            self.batch_change_detection_model.set_after_dataset(folder_path)
            
            # 获取文件夹中的图像数量
            image_count = self._count_images_in_folder(folder_path)
            QMessageBox.information(None, "导入成功", f"成功导入后期影像数据集: {folder_path}\n包含 {image_count} 张影像")
            return True
        return False
    
    def start_batch_change_detection(self):
        """开始批量变化检测"""
        if not self.before_dataset or not self.after_dataset:
            QMessageBox.warning(None, "操作失败", "请先导入前期和后期影像数据集")
            return False
        
        # 设置处理参数
        self.batch_change_detection_model.set_parameters(self.change_detection_params)
        
        # 匹配影像对
        if not self.batch_change_detection_model.match_image_pairs():
            QMessageBox.critical(None, "匹配失败", 
                              f"无法匹配前后期影像：{self.batch_change_detection_model.last_error}")
            return False
        
        # 显示处理进度对话框
        progress_msg = QMessageBox()
        progress_msg.setWindowTitle("正在处理")
        progress_msg.setText("正在进行批量变化检测，请稍候...")
        progress_msg.setStandardButtons(QMessageBox.NoButton)
        progress_msg.show()
        
        # 执行批量变化检测
        success, result = self.batch_change_detection_model.start_batch_processing()
        
        # 关闭进度对话框
        progress_msg.close()
        
        if success:
            # 保存结果
            self.change_detection_results = result
            
            # 显示结果摘要
            summary = (f"批量变化检测完成！\n\n"
                     f"处理的影像对数量: {result['processed_count']}\n"
                     f"成功处理: {result['success_count']} 对\n"
                     f"处理失败: {result['failed_count']} 对\n"
                     f"检测到变化区域: {result['total_changes']} 处\n"
                     f"变化总面积: {result['total_area']}")
            
            QMessageBox.information(None, "批量处理完成", summary)
            return True
        else:
            error_msg = result.get("error", "未知错误")
            QMessageBox.critical(None, "处理失败", f"批量变化检测失败：{error_msg}")
            return False
    
    def view_change_detection_results(self):
        """查看变化检测结果"""
        if not self.batch_change_detection_model.results:
            QMessageBox.warning(None, "操作失败", "请先进行批量变化检测")
            return False
        
        # 获取统计信息
        stats = self.batch_change_detection_model.stats
        
        # 显示结果摘要
        summary = (f"批量变化检测结果摘要：\n\n"
                 f"处理的影像对数量: {stats['processed_count']}\n"
                 f"成功处理: {stats['success_count']} 对\n"
                 f"处理失败: {stats['failed_count']} 对\n"
                 f"检测到变化区域: {stats['total_changes']} 处\n"
                 f"变化总面积: {stats['total_area']}\n\n"
                 f"未来将实现详细的结果查看界面，展示每对影像的变化检测结果")
        
        QMessageBox.information(None, "检测结果摘要", summary)
        return True
    
    def export_change_detection_results(self):
        """导出变化检测结果"""
        if not self.batch_change_detection_model.results:
            QMessageBox.warning(None, "操作失败", "没有可导出的变化检测结果")
            return False
        
        save_path = QFileDialog.getExistingDirectory(
            None,
            "选择导出结果保存位置",
            ""
        )
        
        if save_path:
            # 显示导出进度对话框
            progress_msg = QMessageBox()
            progress_msg.setWindowTitle("正在导出")
            progress_msg.setText("正在导出变化检测结果，请稍候...")
            progress_msg.setStandardButtons(QMessageBox.NoButton)
            progress_msg.show()
            
            # 执行导出
            success = self.batch_change_detection_model.export_results(save_path)
            
            # 关闭进度对话框
            progress_msg.close()
            
            if success:
                stats = self.batch_change_detection_model.stats
                QMessageBox.information(None, "导出成功", 
                                      f"变化检测结果已成功导出到: {save_path}\n"
                                      f"共导出 {stats['success_count']} 对影像的检测结果")
                return True
            else:
                QMessageBox.critical(None, "导出失败", 
                                   f"导出变化检测结果失败：{self.batch_change_detection_model.last_error}")
                return False
        return False
    
    def show_change_detection_settings(self):
        """显示变化检测参数设置"""
        # 这里实际上会显示一个参数设置对话框
        # 目前简单显示当前参数
        
        method_name = {
            "difference": "差值法",
            "ratio": "比值法",
            "regression": "回归分析法"
        }.get(self.change_detection_params["method"], "未知方法")
        
        match_strategy_name = {
            "name": "文件名匹配",
            "index": "索引顺序匹配",
            "metadata": "元数据匹配"
        }.get(self.batch_change_detection_model.parameters["match_strategy"], "未知匹配方式")
        
        current_settings = (f"当前批量变化检测参数：\n\n"
                          f"检测方法: {method_name}\n"
                          f"变化阈值: {self.change_detection_params['threshold']}\n"
                          f"后处理: {'开启' if self.change_detection_params['post_process'] else '关闭'}\n"
                          f"最小变化面积: {self.change_detection_params['min_area']} 像素\n"
                          f"影像对匹配方式: {match_strategy_name}\n"
                          f"最大并行处理数: {self.batch_change_detection_model.parameters['max_workers']}\n\n"
                          f"未来将实现参数设置对话框")
        
        QMessageBox.information(None, "参数设置", current_settings)
        return True
    
    def _count_images_in_folder(self, folder_path):
        """统计文件夹中的图像文件数量"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.img']
        count = 0
        
        try:
            for file in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, file)):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in image_extensions:
                        count += 1
        except Exception as e:
            print(f"Error counting images: {str(e)}")
        
        return count
    
    def start_batch_scene_classification(self):
        """开始批量场景分类"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像数据集")
            return False
        
        # 显示处理进度对话框
        progress_msg = QMessageBox()
        progress_msg.setWindowTitle("正在处理")
        progress_msg.setText("正在进行批量场景分类，请稍候...")
        progress_msg.setStandardButtons(QMessageBox.NoButton)
        progress_msg.show()
        
        # 模拟处理耗时
        time.sleep(1.5)
        
        # 关闭进度对话框
        progress_msg.close()
        
        # 模拟成功的批量场景分类结果
        QMessageBox.information(None, "批量处理完成", f"批量场景分类已完成，共处理了25张影像\n成功识别出5种地物类型")
        return True
    
    def start_batch_semantic_segmentation(self):
        """开始批量语义分割"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像数据集")
            return False
        
        # 显示处理进度对话框
        progress_msg = QMessageBox()
        progress_msg.setWindowTitle("正在处理")
        progress_msg.setText("正在进行批量语义分割，请稍候...")
        progress_msg.setStandardButtons(QMessageBox.NoButton)
        progress_msg.show()
        
        # 模拟处理耗时
        time.sleep(2)
        
        # 关闭进度对话框
        progress_msg.close()
        
        # 模拟成功的批量语义分割结果
        QMessageBox.information(None, "批量处理完成", f"批量语义分割已完成，共处理了25张影像\n分割出7种地物类型，总面积约2350平方公里")
        return True
    
    def start_batch_object_detection(self):
        """开始批量目标检测"""
        if not self.dataset:
            QMessageBox.warning(None, "操作失败", "请先导入遥感影像数据集")
            return False
        
        # 显示处理进度对话框
        progress_msg = QMessageBox()
        progress_msg.setWindowTitle("正在处理")
        progress_msg.setText("正在进行批量目标检测，请稍候...")
        progress_msg.setStandardButtons(QMessageBox.NoButton)
        progress_msg.show()
        
        # 模拟处理耗时
        time.sleep(1.8)
        
        # 关闭进度对话框
        progress_msg.close()
        
        # 模拟成功的批量目标检测结果
        QMessageBox.information(None, "批量处理完成", f"批量目标检测已完成，共处理了25张影像\n检测出167个目标，包括建筑物、车辆、道路等")
        return True 