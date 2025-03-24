import os
import numpy as np
from PIL import Image

class FishnetSegmentation:
    """
    渔网分割功能模型层实现类
    负责图像的分割处理和结果生成，不涉及UI相关操作
    """
    
    def __init__(self):
        self.image_path = None
        self.image = None
        self.grid_params = {
            "grid_count": (4, 4)  # 默认4x4网格
        }
        self.grid_result = []
    
    def load_image(self, image_path):
        """
        加载图像文件
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            bool: 加载是否成功
            dict: 图像信息 (宽度，高度，通道数等)
        """
        try:
            self.image_path = image_path
            self.image = Image.open(image_path)
            
            # 确保图像为RGB模式
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')
            
            width, height = self.image.size
            return True, {
                "width": width,
                "height": height,
                "mode": self.image.mode,
                "format": self.image.format
            }
        except Exception as e:
            print(f"加载图像出错: {str(e)}")
            return False, {"error": str(e)}
    
    def set_grid_parameters(self, grid_count):
        """
        设置网格参数
        
        Args:
            grid_count: 元组 (rows, cols) 表示网格的行数和列数
            
        Returns:
            bool: 设置是否成功
            dict: 计算出的网格信息
        """
        try:
            rows, cols = grid_count
            if rows <= 0 or cols <= 0:
                return False, {"error": "网格行数和列数必须大于0"}
            
            self.grid_params["grid_count"] = (rows, cols)
            
            if self.image:
                width, height = self.image.size
                grid_width = width // cols
                grid_height = height // rows
                
                return True, {
                    "grid_count": (rows, cols),
                    "grid_size": (grid_width, grid_height),
                    "image_size": (width, height)
                }
            else:
                return False, {"error": "未加载图像"}
        except Exception as e:
            print(f"设置网格参数出错: {str(e)}")
            return False, {"error": str(e)}
    
    def generate_grid(self):
        """
        生成网格分割
        
        Returns:
            bool: 分割是否成功
            list: 分割结果列表，每个元素为一个字典，包含位置、行列信息和图像数据
        """
        if not self.image or not self.image_path:
            return False, {"error": "未加载图像"}
        
        try:
            # 获取图像尺寸
            width, height = self.image.size
            
            # 获取网格参数
            rows, cols = self.grid_params["grid_count"]
            
            # 计算每个网格的标准尺寸
            std_width = width // cols
            std_height = height // rows
            
            # 生成网格结果
            self.grid_result = []
            
            for row in range(rows):
                for col in range(cols):
                    # 计算当前网格的位置（标准均匀分割）
                    x = col * std_width
                    y = row * std_height
                    
                    # 计算当前网格的实际宽高（处理不能整除的情况）
                    actual_width = std_width
                    actual_height = std_height
                    
                    # 如果是最后一行/列，处理剩余像素
                    if col == cols - 1:
                        actual_width = width - x
                    if row == rows - 1:
                        actual_height = height - y
                    
                    # 确保裁剪区域有效
                    if actual_width <= 0 or actual_height <= 0:
                        continue
                    
                    # 确保不超出图像边界
                    actual_width = min(actual_width, width - x)
                    actual_height = min(actual_height, height - y)
                    
                    # 裁剪图像
                    try:
                        crop_box = (x, y, x + actual_width, y + actual_height)
                        grid_img = self.image.crop(crop_box)
                        
                        # 检查裁剪结果是否为空
                        if grid_img.size[0] <= 0 or grid_img.size[1] <= 0:
                            continue
                        
                        # 添加到结果列表
                        self.grid_result.append({
                            'position': (x, y, actual_width, actual_height),
                            'image_data': grid_img,  # 这里存储PIL图像对象
                            'row': row + 1,
                            'col': col + 1
                        })
                    except Exception as e:
                        print(f"裁剪网格出错: 位置({row+1},{col+1}), 错误: {str(e)}")
            
            return True, self.grid_result
        except Exception as e:
            print(f"生成网格出错: {str(e)}")
            return False, {"error": str(e)}
    
    def get_grid_result(self):
        """
        获取分割结果
        
        Returns:
            list: 分割结果列表
        """
        return self.grid_result
    
    def export_result(self, export_dir, create_subfolders=True):
        """
        导出分割结果
        
        Args:
            export_dir: 导出目录
            create_subfolders: 是否创建子文件夹
            
        Returns:
            bool: 导出是否成功
            dict: 导出信息
        """
        if not self.grid_result or not self.image_path:
            return False, {"error": "没有可用的分割结果"}
        
        try:
            # 生成原文件名的基础部分（不包括扩展名）
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            
            # 处理导出目录
            save_dir = export_dir
            grids_dir = export_dir
            
            if create_subfolders:
                # 创建以原图像名称命名的子文件夹
                save_dir = os.path.join(export_dir, f"{base_name}_分割结果")
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                # 创建用于保存网格图像的子文件夹
                grids_dir = os.path.join(save_dir, "网格图像")
                if not os.path.exists(grids_dir):
                    os.makedirs(grids_dir)
            
            # 保存结果
            saved_files = []
            
            # 1. 保存每个网格图像
            for grid in self.grid_result:
                row, col = grid['row'], grid['col']
                grid_img = grid['image_data']
                
                # 构建保存文件名：原文件名_行_列.png
                save_name = f"{base_name}_{row}_{col}.png"
                save_path = os.path.join(grids_dir, save_name)
                
                # 保存图像
                grid_img.save(save_path)
                saved_files.append(save_path)
            
            # 2. 保存分割示意图
            overview_path = os.path.join(save_dir, f"{base_name}_网格分割示意图.png")
            self._create_overview_image(overview_path)
            saved_files.append(overview_path)
            
            return True, {
                "save_dir": save_dir,
                "files_count": len(saved_files),
                "files": saved_files
            }
        except Exception as e:
            print(f"导出结果出错: {str(e)}")
            return False, {"error": str(e)}
    
    def _create_overview_image(self, save_path):
        """
        创建并保存分割示意图
        
        Args:
            save_path: 保存路径
            
        Returns:
            bool: 是否成功
        """
        try:
            if not self.image:
                return False
            
            # 创建新图像，与原图大小相同
            overview_img = self.image.copy()
            width, height = overview_img.size
            
            # 在PIL图像上绘制网格线和编号
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(overview_img)
            
            # 尝试加载字体，如果失败则使用默认字体
            try:
                # 尝试使用系统字体
                font_size = 12
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # 如果无法加载TrueType字体，使用默认字体
                font = ImageFont.load_default()
            
            # 红色网格线和编号 - 固定使用纯红色RGB值
            grid_color = (255, 0, 0)  # 纯红色
            text_color = (255, 0, 0)  # 纯红色文字
            text_bg_color = (255, 255, 255, 180)  # 白色半透明背景
            
            # 绘制网格线和编号
            for i, grid in enumerate(self.grid_result):
                x, y, grid_width, grid_height = grid['position']
                
                # 绘制网格边框，使用红色
                draw.rectangle([x, y, x + grid_width, y + grid_height], outline=grid_color, width=2)
                
                # 绘制编号背景
                text = f"{i+1}"
                
                # 绘制背景矩形
                text_width, text_height = font.getsize(text) if hasattr(font, 'getsize') else (font_size*len(text), font_size)
                draw.rectangle([x+2, y+2, x+2+text_width+4, y+2+text_height+4], fill=text_bg_color)
                
                # 绘制文本
                draw.text((x+4, y+4), text, fill=text_color, font=font)
            
            # 保存示意图
            overview_img.save(save_path)
            return True
        except Exception as e:
            print(f"创建示意图出错: {str(e)}")
            return False
            
    def create_overview_image_for_ui(self):
        """
        创建分割示意图，用于UI显示
        
        Returns:
            dict: 包含示意图图像数据和元数据的字典，可用于UI层创建预览图像
                 或None（如果创建失败）
        """
        try:
            if not self.image or not self.grid_result:
                return None
            
            # 创建新图像，与原图大小相同
            overview_img = self.image.copy()
            
            # 在PIL图像上绘制网格线和编号
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(overview_img)
            
            # 尝试加载字体，如果失败则使用默认字体
            try:
                # 尝试使用系统字体
                font_size = 16
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # 如果无法加载TrueType字体，使用默认字体
                font = ImageFont.load_default()
            
            # 红色网格线和编号 - 使用纯红色RGB值(R, G, B)
            # 注意：在convert_pil_to_qimage_format方法中会将RGB转换为BGR
            # 因此，真正的红色应该是(255, 0, 0)
            grid_color = (255, 0, 0)  # 纯红色
            text_color = (255, 0, 0)  # 纯红色文字
            text_bg_color = (255, 255, 255, 180)  # 白色半透明背景
            
            # 绘制网格线和编号
            for i, grid in enumerate(self.grid_result):
                x, y, grid_width, grid_height = grid['position']
                
                # 绘制网格边框，使用红色
                # 注意：指定宽度为2像素确保线条清晰可见
                draw.rectangle([x, y, x + grid_width, y + grid_height], outline=grid_color, width=2)
                
                # 绘制编号背景
                text = f"{i+1}"
                
                # 绘制背景矩形
                text_width, text_height = font.getsize(text) if hasattr(font, 'getsize') else (font_size*len(text), font_size)
                draw.rectangle([x+2, y+2, x+2+text_width+4, y+2+text_height+4], fill=text_bg_color)
                
                # 绘制文本
                draw.text((x+4, y+4), text, fill=text_color, font=font)
            
            # 将PIL图像转换为UI兼容格式
            return self.convert_pil_to_qimage_format(overview_img)
            
        except Exception as e:
            print(f"创建预览示意图出错: {str(e)}")
            return None
    
    # 辅助方法：将PIL图像转换为QImage格式的方法（用于UI层集成）
    def convert_pil_to_qimage_format(self, pil_image):
        """
        将PIL图像转换为QImage兼容的格式（不直接返回QImage对象，保持模型层与UI层的分离）
        
        Args:
            pil_image: PIL图像对象
            
        Returns:
            dict: 包含图像数据和元数据的字典，便于UI层创建QImage
        """
        try:
            # 确保图像是RGB模式
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # 注意：PySide6中QImage使用ARGB/RGBA格式，这需要将RGB通道重新排序
            # 之前的代码是将RGB转为BGR，但这可能导致红色变蓝色的问题
            # 因此使用直接转换方式，不交换通道
            
            # 获取图像数据
            width, height = pil_image.size
            data = pil_image.tobytes("raw", "RGB")
            
            # 返回图像数据和元数据，使用RGB格式
            return {
                "data": data,
                "width": width,
                "height": height,
                "bytes_per_line": width * 3,
                "format": "RGB888"  # 对应于QImage.Format_RGB888
            }
        except Exception as e:
            print(f"图像格式转换出错: {str(e)}")
            return None
            
    def get_ui_compatible_results(self):
        """
        获取用于UI显示的兼容结果
        
        Returns:
            list: 转换后的分割结果列表，适用于UI层
        """
        ui_result = []
        
        for grid in self.grid_result:
            # 复制基本信息
            ui_grid = {
                'position': grid['position'],
                'row': grid['row'],
                'col': grid['col']
            }
            
            # 将PIL图像转换为UI兼容格式
            pil_image = grid['image_data']
            ui_grid['image_data'] = self.convert_pil_to_qimage_format(pil_image)
            
            ui_result.append(ui_grid)
        
        return ui_result
