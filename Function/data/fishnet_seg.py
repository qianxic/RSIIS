import os
import sys
import traceback
import numpy as np
from PIL import Image
import rasterio
from rasterio.windows import Window
from rasterio.transform import from_origin
import warnings
# 抑制不必要的警告
warnings.filterwarnings('ignore', category=rasterio.errors.NotGeoreferencedWarning)

# 检查GDAL是否可用，用于增强诊断信息
try:
    from osgeo import gdal
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False

# 导入封装好的栅格和矢量处理工具
from utils.geo import RasterLoader, RasterData, VectorUtils
from utils.geo import RASTERIO_AVAILABLE, GDAL_AVAILABLE, VECTOR_LIBS_AVAILABLE

class FishnetSegmentation:
    """
    渔网分割功能模型层实现类
    负责图像的分割处理和结果生成，不涉及UI相关操作
    支持常规图像和GeoTIFF格式
    """
    
    def __init__(self):
        self.image_path = None
        self.image = None
        self.grid_params = {
            "grid_count": (4, 4)  # 默认4x4网格
        }
        self.grid_result = []
        
        # 使用 RasterData 存储栅格数据
        self.raster_data = None
        
        # 记录详细错误信息
        self.last_error = None
    
    def load_image(self, image_path):
        """
        加载图像文件，支持常规图像和GeoTIFF格式
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            bool: 加载是否成功
            dict: 图像信息 (宽度，高度，通道数等)
        """
        self.last_error = None
        self.image_path = image_path
        
        try:
            # 使用封装的 RasterLoader 加载栅格数据
            raster_data, success = RasterLoader.load(image_path)
            
            if not success:
                self.last_error = raster_data.error_message
                return False, {"error": raster_data.error_message}
            
            # 保存栅格数据
            self.raster_data = raster_data
            self.image = raster_data.image
            
            # 返回图像信息
            result = {
                "width": raster_data.width,
                "height": raster_data.height,
                "is_geotiff": raster_data.is_geotiff,
                "format": raster_data.metadata.get("format", "未知")
            }
            
            # 如果是GeoTIFF，添加更多信息
            if raster_data.is_geotiff:
                result["bands"] = raster_data.bands_count
                result["crs"] = str(raster_data.crs) if raster_data.crs else "未知"
                result["is_sentinel"] = raster_data.is_sentinel
                
                if raster_data.is_sentinel:
                    result["band_combination"] = raster_data.metadata.get("band_combination", "")
            
            return True, result
                
        except Exception as e:
            # 捕获并记录详细的异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            error_msg = f"加载图像出错: {str(e)}\n详细信息: {error_details}"
            self.last_error = error_msg
            return False, {"error": str(e), "detailed_error": error_details}
    
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
            self.last_error = f"设置网格参数出错: {str(e)}"
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
                    # 计算当前网格的位置
                    x = col * std_width
                    y = row * std_height
                    
                    # 计算实际宽高（处理不能整除的情况）
                    actual_width = std_width if col < cols - 1 else (width - x)
                    actual_height = std_height if row < rows - 1 else (height - y)
                    
                    # 跳过无效的裁剪区域
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
                        
                        grid_data = {
                            'position': (x, y, actual_width, actual_height),
                            'image_data': grid_img,  # 这里存储PIL图像对象
                            'row': row + 1,
                            'col': col + 1
                        }
                        
                        # 如果是GeoTIFF，添加地理参考信息
                        if self.raster_data and self.raster_data.is_geotiff and self.raster_data.geo_transform:
                            self._add_geo_info_to_grid(grid_data, x, y, actual_width, actual_height)
                        
                        # 添加到结果列表
                        self.grid_result.append(grid_data)
                    except Exception as e:
                        self.last_error = f"裁剪网格出错: 位置({row+1},{col+1}), 错误: {str(e)}"
            
            return True, self.grid_result
        except Exception as e:
            self.last_error = f"生成网格出错: {str(e)}"
            return False, {"error": str(e)}
    
    def _add_geo_info_to_grid(self, grid_data, x, y, width, height):
        """添加地理参考信息到网格数据"""
        if RASTERIO_AVAILABLE:
            from rasterio.windows import Window
            # 添加Window对象，用于后续保存GeoTIFF子图
            grid_data['geo_window'] = Window(x, y, width, height)
            
            # 计算子图的地理变换
            if hasattr(self.raster_data.geo_transform, '__call__'):
                # rasterio风格的transform
                from rasterio.transform import from_origin
                topleft_x, topleft_y = self.raster_data.geo_transform * (x, y)
                grid_data['geo_transform'] = from_origin(
                    topleft_x, topleft_y, 
                    self.raster_data.geo_transform.a, self.raster_data.geo_transform.e
                )
            else:
                # GDAL风格的transform
                grid_data['geo_transform'] = self.raster_data.geo_transform
                
            grid_data['geo_crs'] = self.raster_data.crs
    
    def get_grid_result(self):
        """
        获取分割结果
        
        Returns:
            list: 分割结果列表
        """
        return self.grid_result
    
    def export_result(self, export_dir, create_subfolders=True, export_shp=True):
        """
        导出分割结果
        
        Args:
            export_dir: 导出目录
            create_subfolders: 是否创建子文件夹
            export_shp: 是否导出Shapefile矢量格式
            
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
                
                # 根据是否有地理参考信息，选择不同的保存方式
                if self.raster_data and self.raster_data.is_geotiff and 'geo_window' in grid and self.raster_data.rasterio_dataset:
                    # 保存为GeoTIFF
                    save_name = f"{base_name}_{row}_{col}.tif"
                    save_path = os.path.join(grids_dir, save_name)
                    
                    # 使用rasterio保存带有地理参考信息的裁剪图像
                    if RASTERIO_AVAILABLE:
                        import rasterio
                        window = grid['geo_window']
                        
                        # 读取原始数据（保留所有波段）
                        data = self.raster_data.rasterio_dataset.read(window=window)
                        
                        # 写入GeoTIFF
                        profile = self.raster_data.rasterio_dataset.profile.copy()
                        profile.update({
                            'height': window.height,
                            'width': window.width,
                            'transform': grid['geo_transform']
                        })
                        
                        with rasterio.open(save_path, 'w', **profile) as dst:
                            dst.write(data)
                    else:
                        # 如果rasterio不可用，保存为普通PNG
                        save_name = f"{base_name}_{row}_{col}.png"
                        save_path = os.path.join(grids_dir, save_name)
                        grid_img.save(save_path)
                else:
                    # 保存为普通PNG
                    save_name = f"{base_name}_{row}_{col}.png"
                    save_path = os.path.join(grids_dir, save_name)
                    grid_img.save(save_path)
                
                saved_files.append(save_path)
            
            # 2. 保存分割示意图
            overview_path = os.path.join(save_dir, f"{base_name}_网格分割示意图.png")
            self._create_overview_image(overview_path)
            saved_files.append(overview_path)
            
            # 3. 如果需要，导出矢量格式
            if export_shp and self.raster_data and VECTOR_LIBS_AVAILABLE:
                shp_path = os.path.join(save_dir, f"{base_name}_网格矢量.shp")
                success, message = VectorUtils.grid_to_shapefile(
                    self.raster_data, 
                    self.grid_result, 
                    shp_path
                )
                
                if success:
                    saved_files.append(shp_path)
                else:
                    self.last_error = f"导出矢量文件失败: {message}"
            
            return True, {
                "save_dir": save_dir,
                "files_count": len(saved_files),
                "files": saved_files
            }
        except Exception as e:
            self.last_error = f"导出结果出错: {str(e)}"
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
            
            # 应用图像增强处理
            overview_img = self._enhance_grid_image(overview_img)
            
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
            self.last_error = f"创建示意图出错: {str(e)}"
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
            
            # 应用图像增强方法进行处理
            overview_img = self._enhance_grid_image(overview_img)
            
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
            self.last_error = f"创建预览示意图出错: {str(e)}"
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
            
            # 应用图像增强方法
            pil_image = self._enhance_grid_image(pil_image)
            
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
            self.last_error = f"图像格式转换出错: {str(e)}"
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

    def __del__(self):
        """析构函数，确保释放资源"""
        # 关闭资源
        if hasattr(self, 'raster_data') and self.raster_data:
            if self.raster_data.rasterio_dataset:
                self.raster_data.rasterio_dataset.close()

    def _enhance_grid_image(self, pil_image):
        """
        使用累积计数截断方法增强网格图像显示
        
        Args:
            pil_image: PIL图像对象
            
        Returns:
            PIL.Image: 处理后的图像对象
        """
        try:
            # 如果图像已经由RasterLoader处理过，则不需要再处理
            if self.raster_data and self.raster_data.is_geotiff:
                return pil_image
                
            # 转换为numpy数组
            img_array = np.array(pil_image)
            
            # 使用utils.geo.raster_loader中的增强方法
            from utils.geo.raster_loader import RasterLoader
            enhanced_array = RasterLoader._enhance_sentinel_image(img_array)
            
            # 转回PIL图像
            from PIL import Image
            return Image.fromarray(enhanced_array)
        except Exception as e:
            self.last_error = f"图像增强失败: {str(e)}"
            return pil_image  # 出错时返回原始图像
