import os
import time
import numpy as np
from PIL import Image
from datetime import datetime
import multiprocessing as mp
from tqdm import tqdm

# 导入单对影像变化检测模型
from Function.analysis.change_detection import ChangeDetectionModel

class BatchChangeDetectionModel:
    """批量变化检测模型类，实现多对遥感影像的批量变化检测处理"""
    
    def __init__(self):
        """初始化模型"""
        # 数据集路径
        self.before_dataset_path = None
        self.after_dataset_path = None
        
        # 影像对应关系
        self.image_pairs = []
        
        # 处理结果
        self.results = {}
        
        # 处理状态
        self.is_processing = False
        self.process_progress = 0
        
        # 统计信息
        self.stats = {
            "processed_count": 0,
            "success_count": 0,
            "failed_count": 0,
            "total_changes": 0,
            "total_area": 0.0
        }
        
        # 变化检测参数
        self.parameters = {
            "threshold": 0.5,           # 变化检测阈值
            "method": "difference",     # 检测方法，可选：difference, ratio, regression
            "post_process": True,       # 是否进行后处理
            "min_area": 10,             # 最小变化区域面积
            "max_workers": mp.cpu_count() - 1 or 1,  # 最大并行处理数量
            "match_strategy": "name"    # 影像匹配策略: name, index, metadata
        }
        
        # 最后错误信息
        self.last_error = ""
    
    def set_before_dataset(self, dataset_path):
        """设置前期影像数据集路径"""
        self.before_dataset_path = dataset_path
        return True
    
    def set_after_dataset(self, dataset_path):
        """设置后期影像数据集路径"""
        self.after_dataset_path = dataset_path
        return True
    
    def set_parameters(self, parameters):
        """设置处理参数"""
        # 更新参数
        for key, value in parameters.items():
            if key in self.parameters:
                self.parameters[key] = value
        
        return True
    
    def match_image_pairs(self):
        """匹配前后期影像对"""
        if not self.before_dataset_path or not self.after_dataset_path:
            self.last_error = "请先设置前期和后期影像数据集路径"
            return False
        
        try:
            self.image_pairs = []
            
            # 获取前期和后期数据集中的图像文件列表
            before_images = self._get_image_files(self.before_dataset_path)
            after_images = self._get_image_files(self.after_dataset_path)
            
            if not before_images or not after_images:
                self.last_error = "数据集中没有找到有效的图像文件"
                return False
            
            # 根据不同的匹配策略进行影像对匹配
            match_strategy = self.parameters["match_strategy"]
            
            if match_strategy == "name":
                # 根据文件名匹配
                self._match_by_name(before_images, after_images)
            elif match_strategy == "index":
                # 根据索引顺序匹配
                self._match_by_index(before_images, after_images)
            else:
                # 默认按文件名匹配
                self._match_by_name(before_images, after_images)
            
            if not self.image_pairs:
                self.last_error = "未能成功匹配任何影像对"
                return False
            
            return True
            
        except Exception as e:
            self.last_error = f"匹配影像对时出错：{str(e)}"
            return False
    
    def start_batch_processing(self):
        """执行批量变化检测处理"""
        if not self.image_pairs:
            # 尝试匹配影像对
            if not self.match_image_pairs():
                return False, {"error": self.last_error}
        
        try:
            self.is_processing = True
            self.process_progress = 0
            
            # 重置统计信息
            self.stats = {
                "processed_count": 0,
                "success_count": 0,
                "failed_count": 0,
                "total_changes": 0,
                "total_area": 0.0
            }
            
            self.results = {}
            
            # 设置进度总数
            total_pairs = len(self.image_pairs)
            self.stats["processed_count"] = total_pairs
            
            # 单进程处理
            if len(self.image_pairs) <= 5 or self.parameters["max_workers"] <= 1:
                self._process_sequential()
            else:
                # 多进程处理
                self._process_parallel()
            
            # 更新统计信息
            self.stats["success_count"] = sum(1 for result in self.results.values() if result.get("success", False))
            self.stats["failed_count"] = self.stats["processed_count"] - self.stats["success_count"]
            
            # 计算总的变化量
            total_changes = 0
            total_area = 0.0
            for result in self.results.values():
                if result.get("success", False):
                    total_changes += result.get("changes_count", 0)
                    # 提取数字部分
                    area_str = result.get("change_area", "0")
                    if isinstance(area_str, str):
                        area_str = area_str.split(" ")[0]
                    try:
                        total_area += float(area_str)
                    except:
                        pass
            
            self.stats["total_changes"] = total_changes
            self.stats["total_area"] = f"{total_area:.2f} 平方公里"
            
            self.is_processing = False
            self.process_progress = 100
            
            return True, self.stats
            
        except Exception as e:
            self.last_error = str(e)
            self.is_processing = False
            self.process_progress = 0
            return False, {"error": f"批量变化检测处理失败: {str(e)}"}
    
    def export_results(self, output_dir):
        """导出批量变化检测结果"""
        if not self.results:
            self.last_error = "没有可导出的结果"
            return False
        
        try:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 创建汇总报告文件
            report_path = os.path.join(output_dir, "change_detection_report.txt")
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"批量变化检测报告\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"前期数据集: {self.before_dataset_path}\n")
                f.write(f"后期数据集: {self.after_dataset_path}\n\n")
                f.write(f"处理影像对数量: {self.stats['processed_count']}\n")
                f.write(f"成功处理数量: {self.stats['success_count']}\n")
                f.write(f"处理失败数量: {self.stats['failed_count']}\n")
                f.write(f"总变化区域数量: {self.stats['total_changes']}\n")
                f.write(f"变化总面积: {self.stats['total_area']}\n\n")
                f.write(f"参数设置:\n")
                f.write(f"  检测方法: {self.parameters['method']}\n")
                f.write(f"  变化阈值: {self.parameters['threshold']}\n")
                f.write(f"  后处理: {'开启' if self.parameters['post_process'] else '关闭'}\n")
                f.write(f"  最小变化面积: {self.parameters['min_area']} 像素\n\n")
                f.write(f"各影像对处理详情:\n")
                
                for i, (pair_id, result) in enumerate(self.results.items()):
                    f.write(f"\n[{i+1}] 影像对: {pair_id}\n")
                    if result.get("success", False):
                        f.write(f"  状态: 成功\n")
                        f.write(f"  处理时间: {result.get('timestamp', '未记录')}\n")
                        f.write(f"  变化区域数量: {result.get('changes_count', 0)}\n")
                        f.write(f"  变化面积: {result.get('change_area', '未记录')}\n")
                    else:
                        f.write(f"  状态: 失败\n")
                        f.write(f"  错误信息: {result.get('error', '未知错误')}\n")
            
            # 创建结果图像目录
            images_dir = os.path.join(output_dir, "change_maps")
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # 保存变化检测图
            for pair_id, result in self.results.items():
                if result.get("success", False) and "change_map" in result:
                    try:
                        # 创建彩色变化图 (红色表示变化区域)
                        change_map = result["change_map"]
                        result_image = np.zeros((change_map.shape[0], change_map.shape[1], 3), dtype=np.uint8)
                        result_image[:, :, 0] = change_map  # 红色通道
                        
                        # 转换为PIL图像并保存
                        pil_image = Image.fromarray(result_image)
                        save_path = os.path.join(images_dir, f"{pair_id}.png")
                        pil_image.save(save_path)
                    except Exception as e:
                        print(f"Error saving change map for {pair_id}: {str(e)}")
            
            return True
            
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def _get_image_files(self, folder_path):
        """获取文件夹中的图像文件列表"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.img']
        image_files = []
        
        for file in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file)):
                ext = os.path.splitext(file)[1].lower()
                if ext in image_extensions:
                    image_files.append(file)
        
        return sorted(image_files)
    
    def _match_by_name(self, before_images, after_images):
        """根据文件名匹配前后期影像对"""
        before_names = {self._get_base_name(img): img for img in before_images}
        after_names = {self._get_base_name(img): img for img in after_images}
        
        common_names = set(before_names.keys()) & set(after_names.keys())
        
        for name in common_names:
            before_path = os.path.join(self.before_dataset_path, before_names[name])
            after_path = os.path.join(self.after_dataset_path, after_names[name])
            self.image_pairs.append({
                "id": name,
                "before_path": before_path,
                "after_path": after_path
            })
    
    def _match_by_index(self, before_images, after_images):
        """根据索引顺序匹配前后期影像对"""
        min_count = min(len(before_images), len(after_images))
        
        for i in range(min_count):
            before_path = os.path.join(self.before_dataset_path, before_images[i])
            after_path = os.path.join(self.after_dataset_path, after_images[i])
            pair_id = f"pair_{i+1:04d}"
            self.image_pairs.append({
                "id": pair_id,
                "before_path": before_path,
                "after_path": after_path
            })
    
    def _get_base_name(self, filename):
        """获取文件基础名称，用于匹配"""
        # 移除扩展名
        base = os.path.splitext(filename)[0]
        
        # 尝试移除常见的日期/时间后缀，如 "_20210101", "_2021-01-01" 等
        import re
        # 移除日期后缀
        base = re.sub(r'_\d{8}$', '', base)
        base = re.sub(r'_\d{4}-\d{2}-\d{2}$', '', base)
        
        return base
    
    def _process_sequential(self):
        """单进程顺序处理所有影像对"""
        change_detector = ChangeDetectionModel()
        
        for i, pair in enumerate(self.image_pairs):
            pair_id = pair["id"]
            before_path = pair["before_path"]
            after_path = pair["after_path"]
            
            # 更新进度
            self.process_progress = int((i / len(self.image_pairs)) * 100)
            
            # 处理单对影像
            result = self._process_single_pair(change_detector, pair_id, before_path, after_path)
            self.results[pair_id] = result
    
    def _process_parallel(self):
        """多进程并行处理所有影像对"""
        # 创建进程池
        pool = mp.Pool(self.parameters["max_workers"])
        
        # 准备任务参数
        tasks = []
        for pair in self.image_pairs:
            tasks.append((pair["id"], pair["before_path"], pair["after_path"], self.parameters))
        
        # 提交任务到进程池
        results = []
        for task in tasks:
            result = pool.apply_async(process_pair_worker, args=task)
            results.append((task[0], result))
        
        # 关闭进程池，不再接受新任务
        pool.close()
        
        # 等待所有任务完成并收集结果
        for i, (pair_id, async_result) in enumerate(results):
            try:
                result = async_result.get()
                self.results[pair_id] = result
                # 更新进度
                self.process_progress = int(((i + 1) / len(results)) * 100)
            except Exception as e:
                self.results[pair_id] = {
                    "success": False,
                    "error": f"处理异常: {str(e)}"
                }
        
        # 等待所有进程结束
        pool.join()
    
    def _process_single_pair(self, detector, pair_id, before_path, after_path):
        """处理单对影像"""
        try:
            # 加载前期影像
            success_before, info_before = detector.load_before_image(before_path)
            if not success_before:
                return {
                    "success": False,
                    "error": f"加载前期影像失败: {info_before.get('error', '未知错误')}"
                }
            
            # 加载后期影像
            success_after, info_after = detector.load_after_image(after_path)
            if not success_after:
                return {
                    "success": False,
                    "error": f"加载后期影像失败: {info_after.get('error', '未知错误')}"
                }
            
            # 设置检测参数
            detector.set_parameters(self.parameters)
            
            # 执行变化检测
            success, result = detector.detect_changes()
            
            if success:
                # 补充结果信息
                result["pair_id"] = pair_id
                result["before_path"] = before_path
                result["after_path"] = after_path
                result["success"] = True
                return result
            else:
                return {
                    "success": False,
                    "error": result.get("error", "变化检测处理失败")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def process_pair_worker(pair_id, before_path, after_path, parameters):
    """多进程工作函数，处理单对影像"""
    try:
        # 创建变化检测器
        detector = ChangeDetectionModel()
        
        # 加载前期影像
        success_before, info_before = detector.load_before_image(before_path)
        if not success_before:
            return {
                "success": False,
                "error": f"加载前期影像失败: {info_before.get('error', '未知错误')}"
            }
        
        # 加载后期影像
        success_after, info_after = detector.load_after_image(after_path)
        if not success_after:
            return {
                "success": False,
                "error": f"加载后期影像失败: {info_after.get('error', '未知错误')}"
            }
        
        # 设置检测参数
        detector.set_parameters(parameters)
        
        # 执行变化检测
        success, result = detector.detect_changes()
        
        if success:
            # 补充结果信息
            result["pair_id"] = pair_id
            result["before_path"] = before_path
            result["after_path"] = after_path
            result["success"] = True
            return result
        else:
            return {
                "success": False,
                "error": result.get("error", "变化检测处理失败")
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        } 