import numpy as np
from PIL import Image
import os
import time
from datetime import datetime

class ChangeDetectionModel:
    """变化检测模型类，实现多时相遥感影像的变化检测"""
    
    def __init__(self):
        """初始化模型"""
        # 当前加载的影像
        self.before_image = None
        self.after_image = None
        
        # 影像路径
        self.before_image_path = None
        self.after_image_path = None
        
        # 检测结果
        self.detection_result = None
        
        # 检测参数
        self.parameters = {
            "threshold": 0.5,           # 变化检测阈值
            "method": "difference",     # 检测方法，可选：difference, ratio, regression
            "post_process": True,       # 是否进行后处理
            "min_area": 10              # 最小变化区域面积
        }
        
        # 处理状态
        self.is_processing = False
        self.process_progress = 0
        
        # 最后错误信息
        self.last_error = ""
    
    def load_before_image(self, image_path):
        """加载前期影像"""
        try:
            # 这里模拟加载图像，实际实现会更复杂
            # 如果是GeoTIFF文件，会使用GDAL或rasterio加载
            self.before_image_path = image_path
            self.before_image = Image.open(image_path)
            
            # 获取图像信息
            width, height = self.before_image.size
            format_name = self.before_image.format
            
            # 返回加载状态和图像信息
            return True, {
                "width": width,
                "height": height,
                "format": format_name,
                "path": image_path
            }
            
        except Exception as e:
            self.last_error = str(e)
            return False, {
                "error": "加载前期影像失败",
                "detailed_error": str(e)
            }
    
    def load_after_image(self, image_path):
        """加载后期影像"""
        try:
            # 这里模拟加载图像，实际实现会更复杂
            # 如果是GeoTIFF文件，会使用GDAL或rasterio加载
            self.after_image_path = image_path
            self.after_image = Image.open(image_path)
            
            # 获取图像信息
            width, height = self.after_image.size
            format_name = self.after_image.format
            
            # 返回加载状态和图像信息
            return True, {
                "width": width,
                "height": height,
                "format": format_name,
                "path": image_path
            }
            
        except Exception as e:
            self.last_error = str(e)
            return False, {
                "error": "加载后期影像失败",
                "detailed_error": str(e)
            }
    
    def set_parameters(self, parameters):
        """设置变化检测参数"""
        # 更新参数
        for key, value in parameters.items():
            if key in self.parameters:
                self.parameters[key] = value
        
        return True
    
    def detect_changes(self):
        """执行变化检测"""
        # 检查影像是否已加载
        if self.before_image is None or self.after_image is None:
            self.last_error = "请先加载前期和后期影像"
            return False, {"error": self.last_error}
        
        try:
            self.is_processing = True
            self.process_progress = 0
            
            # 这里会实现实际的变化检测算法
            # 目前只是一个简单的模拟实现
            
            # 模拟处理过程
            for i in range(10):
                time.sleep(0.2)  # 模拟处理时间
                self.process_progress = (i + 1) * 10
            
            # 模拟生成变化检测结果
            # 实际实现会根据算法具体生成变化图
            change_map = np.zeros((self.before_image.size[1], self.before_image.size[0]), dtype=np.uint8)
            
            # 模拟一些随机变化区域
            np.random.seed(int(time.time()))
            change_count = np.random.randint(10, 20)
            
            # 随机添加一些变化区域
            for i in range(change_count):
                x = np.random.randint(0, self.before_image.size[0] - 100)
                y = np.random.randint(0, self.before_image.size[1] - 100)
                width = np.random.randint(20, 100)
                height = np.random.randint(20, 100)
                
                # 随机设置变化区域
                change_map[y:y+height, x:x+width] = 255
            
            # 计算变化统计信息
            change_area = np.sum(change_map > 0) * 30 * 30 / 1000000  # 假设每像素30m, 计算平方公里
            
            # 保存结果
            self.detection_result = {
                "change_map": change_map,
                "changes_count": change_count,
                "change_area": f"{change_area:.2f} 平方公里",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.is_processing = False
            self.process_progress = 100
            
            return True, self.detection_result
            
        except Exception as e:
            self.last_error = str(e)
            self.is_processing = False
            self.process_progress = 0
            return False, {"error": f"变化检测处理失败: {str(e)}"}
    
    def export_result(self, save_path):
        """导出变化检测结果"""
        # 检查是否已完成检测
        if self.detection_result is None or "change_map" not in self.detection_result:
            self.last_error = "请先执行变化检测"
            return False
        
        try:
            # 获取变化图
            change_map = self.detection_result["change_map"]
            
            # 创建彩色变化图 (红色表示变化区域)
            result_image = np.zeros((change_map.shape[0], change_map.shape[1], 3), dtype=np.uint8)
            result_image[:, :, 0] = change_map  # 红色通道
            
            # 转换为PIL图像
            pil_image = Image.fromarray(result_image)
            
            # 根据文件扩展名保存不同格式
            file_ext = os.path.splitext(save_path)[1].lower()
            
            if file_ext in ['.tif', '.tiff']:
                # 保存为GeoTIFF
                # 这里实际会使用GDAL或rasterio保存，并附加地理信息
                pil_image.save(save_path)
            else:
                # 普通图像格式
                pil_image.save(save_path)
            
            return True
            
        except Exception as e:
            self.last_error = str(e)
            return False 