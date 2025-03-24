import os
import sys
import traceback
import warnings
import numpy as np
from PIL import Image
import warnings

# 尝试导入地理空间库，并记录可用性
try:
    import rasterio
    from rasterio.windows import Window
    from rasterio.transform import from_origin
    # 抑制不必要的警告
    warnings.filterwarnings('ignore', category=rasterio.errors.NotGeoreferencedWarning)
    RASTERIO_AVAILABLE = True
except ImportError:
    RASTERIO_AVAILABLE = False

try:
    from osgeo import gdal, ogr, osr
    GDAL_AVAILABLE = True
except ImportError:
    GDAL_AVAILABLE = False

try:
    import shapely
    from shapely.geometry import Polygon, mapping
    import fiona
    from fiona.crs import from_epsg
    VECTOR_LIBS_AVAILABLE = True
except ImportError:
    VECTOR_LIBS_AVAILABLE = False


class RasterData:
    """
    栅格数据类，用于存储加载后的数据和元数据
    """
    def __init__(self):
        self.image = None               # PIL图像对象，用于显示
        self.image_path = None          # 图像文件路径
        self.width = 0                  # 宽度
        self.height = 0                 # 高度
        self.bands_count = 0            # 波段数
        self.data_type = None           # 数据类型
        self.is_geotiff = False         # 是否为GeoTIFF
        self.is_sentinel = False        # 是否为Sentinel数据
        self.crs = None                 # 坐标参考系统
        self.geo_transform = None       # 地理变换矩阵
        self.band_names = []            # 波段名称
        self.band_indices = {}          # 波段索引（例如，{'red': 1, 'green': 2, 'blue': 3}）
        self.metadata = {}              # 其他元数据
        self.array = None               # numpy数组（可用于分析）
        self.rasterio_dataset = None    # rasterio数据集
        self.gdal_dataset = None        # GDAL数据集
        self.error_message = None       # 错误信息


class RasterLoader:
    """
    栅格数据加载器 - 提供统一的接口来加载不同格式的栅格数据，
    支持GeoTIFF、常规图像格式，以及Sentinel-2卫星数据等
    """
    
    @staticmethod
    def load(file_path):
        """
        加载栅格数据，自动选择合适的方法
        
        Args:
            file_path: 文件路径
            
        Returns:
            RasterData: 加载的栅格数据对象
            bool: 是否成功加载
        """
        raster = RasterData()
        raster.image_path = os.path.normpath(os.path.abspath(file_path))
        
        # 确保文件存在
        if not os.path.exists(file_path):
            raster.error_message = f"文件不存在：{file_path}"
            return raster, False

        # 特殊处理TIFF/GeoTIFF格式
        if file_path.lower().endswith(('.tif', '.tiff')):
            # 尝试使用多种方法加载
            # 1. 优先使用rasterio（最佳支持地理信息）
            if RASTERIO_AVAILABLE:
                success, message = RasterLoader._load_with_rasterio(raster)
                if success:
                    return raster, True
                # 如果失败，尝试下一种方法
            
            # 2. 尝试GDAL
            if GDAL_AVAILABLE:
                success, message = RasterLoader._load_with_gdal(raster)
                if success:
                    return raster, True
                raster.error_message = message
            
            # 3. 尝试PIL（作为后备选项）
            success, message = RasterLoader._load_with_pil(raster)
            if success:
                return raster, True
                
            # 所有方法都失败
            if not raster.error_message:
                raster.error_message = "无法以任何方式加载栅格数据"
            return raster, False
        
        # 非TIFF格式，直接使用PIL
        success, message = RasterLoader._load_with_pil(raster)
        if success:
            return raster, True
        
        raster.error_message = message
        return raster, False
    
    @staticmethod
    def _load_with_rasterio(raster):
        """使用rasterio加载GeoTIFF"""
        try:
            # 使用rasterio环境设置，提高兼容性
            with rasterio.Env(GDAL_SKIP='PDF'):  # 跳过PDF驱动避免某些冲突
                # 打开GeoTIFF文件
                dataset = rasterio.open(raster.image_path)
                
                # 保存基本信息
                raster.rasterio_dataset = dataset
                raster.width = dataset.width
                raster.height = dataset.height
                raster.bands_count = dataset.count
                raster.data_type = dataset.dtypes[0] if dataset.count > 0 else None
                raster.is_geotiff = True
                raster.geo_transform = dataset.transform
                raster.crs = dataset.crs
                
                # 检测是否为Sentinel-2数据（通常波段数较多）
                raster.is_sentinel = raster.bands_count > 10
                
                # 获取波段描述
                if dataset.descriptions:
                    raster.band_names = [desc if desc else f"Band_{i+1}" 
                                       for i, desc in enumerate(dataset.descriptions)]
                else:
                    raster.band_names = [f"Band_{i+1}" for i in range(raster.bands_count)]
                
                # 根据不同数据类型采用不同的处理策略
                if raster.is_sentinel:
                    RasterLoader._process_sentinel(raster)
                elif raster.bands_count >= 3:
                    # 标准RGB读取（适用于正常的3波段数据）
                    red = dataset.read(1)
                    green = dataset.read(2)
                    blue = dataset.read(3)
                    rgb = np.stack([red, green, blue], axis=2)
                else:
                    # 单波段，转换为RGB
                    single_band = dataset.read(1)
                    rgb = np.stack([single_band, single_band, single_band], axis=2)
                
                # 标准化处理并创建PIL图像
                rgb_norm = RasterLoader._enhance_sentinel_image(rgb)
                raster.array = rgb_norm
                raster.image = Image.fromarray(rgb_norm)
                
                return True, "成功"
                
        except Exception as e:
            # 记录详细的异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            # 关闭已打开的rasterio文件
            if raster.rasterio_dataset:
                raster.rasterio_dataset.close()
                raster.rasterio_dataset = None
            
            return False, f"rasterio加载失败: {str(e)}\n{error_details}"
    
    @staticmethod
    def _load_with_gdal(raster):
        """使用GDAL加载GeoTIFF"""
        try:
            # 打开数据集
            dataset = gdal.Open(raster.image_path, gdal.GA_ReadOnly)
            if dataset is None:
                return False, "GDAL无法打开文件"
                
            # 保存基本信息
            raster.gdal_dataset = dataset
            raster.width = dataset.RasterXSize
            raster.height = dataset.RasterYSize
            raster.bands_count = dataset.RasterCount
            raster.is_geotiff = True
            
            # 获取变换和投影信息
            raster.geo_transform = dataset.GetGeoTransform()
            raster.crs = dataset.GetProjection()
            
            # 读取数据 - 默认假设band1=红, band2=绿, band3=蓝
            # 但有些数据可能是band1=蓝, band2=绿, band3=红，这取决于数据源
            if raster.bands_count >= 3:
                # 多波段 - 获取波段名称以帮助确定正确的RGB顺序
                band_names = []
                for i in range(1, raster.bands_count + 1):
                    band = dataset.GetRasterBand(i)
                    name = band.GetDescription() or f"Band_{i}"
                    band_names.append(name.lower())
                
                # 根据波段名称确定RGB索引
                red_idx, green_idx, blue_idx = 1, 2, 3  # 默认顺序
                
                # 尝试通过名称识别波段
                for i, name in enumerate(band_names):
                    band_idx = i + 1  # GDAL使用1-based索引
                    if 'red' in name or 'b4' in name or 'band4' in name:
                        red_idx = band_idx
                    elif 'green' in name or 'b3' in name or 'band3' in name:
                        green_idx = band_idx
                    elif 'blue' in name or 'b2' in name or 'band2' in name:
                        blue_idx = band_idx
                
                # 确保索引在有效范围内
                red_idx = min(red_idx, raster.bands_count)
                green_idx = min(green_idx, raster.bands_count)
                blue_idx = min(blue_idx, raster.bands_count)
                
                # 读取相应波段
                red = dataset.GetRasterBand(red_idx).ReadAsArray()
                green = dataset.GetRasterBand(green_idx).ReadAsArray()
                blue = dataset.GetRasterBand(blue_idx).ReadAsArray()
                
                # 设置波段索引信息
                raster.band_indices = {'red': red_idx, 'green': green_idx, 'blue': blue_idx}
                
                # 保存波段组合信息
                raster.metadata["band_combination"] = f"R{red_idx}G{green_idx}B{blue_idx}"
            else:
                # 单波段 - 转为RGB
                band = dataset.GetRasterBand(1).ReadAsArray()
                red = green = blue = band
                raster.band_indices = {'red': 1, 'green': 1, 'blue': 1}
            
            # 修正：正确堆叠RGB通道
            # 在NumPy中，RGB图像的形状是(height, width, 3)，其中最后一个维度按R,G,B顺序排列
            rgb = np.dstack([red, green, blue])
            
            # 数据归一化
            rgb_norm = RasterLoader._enhance_sentinel_image(rgb)
            raster.array = rgb_norm
            raster.image = Image.fromarray(rgb_norm)
            
            # 获取波段信息
            raster.band_names = []
            for i in range(1, raster.bands_count + 1):
                band = dataset.GetRasterBand(i)
                name = band.GetDescription()
                if not name:
                    name = f"Band_{i}"
                raster.band_names.append(name)
            
            return True, "成功"
            
        except Exception as e:
            # 记录详细的异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            return False, f"GDAL加载失败: {str(e)}\n{error_details}"
    
    @staticmethod
    def _load_with_pil(raster):
        """使用PIL加载常规图像"""
        try:
            # 使用PIL加载图像
            image = Image.open(raster.image_path)
            
            # 保存基本信息
            raster.is_geotiff = False
            raster.image = image
            
            # 确保图像为RGB模式
            if image.mode != 'RGB':
                raster.image = image.convert('RGB')
            
            raster.width, raster.height = raster.image.size
            
            # 如果需要，可以转换为numpy数组
            raster.array = np.array(raster.image)
            
            # 设置波段信息（常规RGB）
            raster.bands_count = 3
            raster.band_names = ["Red", "Green", "Blue"]
            raster.band_indices = {"red": 0, "green": 1, "blue": 2}
            
            # 添加图像元数据
            raster.metadata["format"] = image.format
            raster.metadata["mode"] = image.mode
            
            return True, "成功"
            
        except Exception as e:
            # 记录详细的异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            return False, f"PIL加载失败: {str(e)}\n{error_details}"
    
    @staticmethod
    def _process_sentinel(raster):
        """专门处理Sentinel-2数据"""
        try:
            # 识别波段
            raster.band_indices = {}
            
            # 尝试识别常用的波段命名方式
            for i, band_name in enumerate(raster.band_names):
                lower_name = band_name.lower() if band_name else ''
                
                band_index = i + 1  # rasterio使用1-based索引
                
                if 'red' in lower_name or 'b4' in lower_name or 'band4' in lower_name:
                    raster.band_indices['red'] = band_index
                elif 'green' in lower_name or 'b3' in lower_name or 'band3' in lower_name:
                    raster.band_indices['green'] = band_index
                elif 'blue' in lower_name or 'b2' in lower_name or 'band2' in lower_name:
                    raster.band_indices['blue'] = band_index
                elif 'nir' in lower_name or 'b8' in lower_name or 'band8' in lower_name:
                    raster.band_indices['nir'] = band_index
            
            # 如果无法通过描述识别，则采用默认的Sentinel-2波段索引
            if not all(key in raster.band_indices for key in ['red', 'green', 'blue']):
                # Sentinel-2默认波段: B4=Red, B3=Green, B2=Blue
                if raster.bands_count >= 4:
                    raster.band_indices = {'red': 4, 'green': 3, 'blue': 2}
                else:
                    # 如果波段数少于4，使用前三个波段
                    raster.band_indices = {'red': min(3, raster.bands_count), 
                                         'green': min(2, raster.bands_count), 
                                         'blue': min(1, raster.bands_count)}
            
            # 调整索引以适应rasterio的1-based索引和数据集实际波段数
            for key, value in raster.band_indices.items():
                if value > raster.bands_count:
                    raster.band_indices[key] = min(value, raster.bands_count)
            
            # 读取选定的波段
            red_idx = raster.band_indices.get('red', 1)
            green_idx = raster.band_indices.get('green', 1)
            blue_idx = raster.band_indices.get('blue', 1)
            
            red = raster.rasterio_dataset.read(red_idx)
            green = raster.rasterio_dataset.read(green_idx)
            blue = raster.rasterio_dataset.read(blue_idx)
            
            # 修正：正确堆叠RGB通道 - 注意numpy的RGB顺序
            # 在NumPy中，RGB图像的形状是(height, width, 3)，其中最后一个维度按R,G,B顺序排列
            rgb = np.dstack([red, green, blue])
            
            # 应用增强的标准化处理
            rgb_norm = RasterLoader._enhance_sentinel_image(rgb)
            
            # 保存数据
            raster.array = rgb_norm
            raster.image = Image.fromarray(rgb_norm)
            
            # 记录使用的波段组合
            raster.metadata["band_combination"] = f"R{red_idx}G{green_idx}B{blue_idx}"
            
            return True, "成功"
            
        except Exception as e:
            # 记录详细的异常信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            return False, f"Sentinel-2数据处理失败: {str(e)}\n{error_details}"
    
    @staticmethod
    def _enhance_sentinel_image(array):
        """
        处理图像显示 - 使用累积计数截断(Cumulative count cut)方法
        对所有类型图像进行更好的图像增强，参考QGIS的渲染策略
        
        Args:
            array: 原始numpy数组
            
        Returns:
            numpy.ndarray: 处理后的数组
        """
        try:
            # 检查数据是否有效
            if array is None or array.size == 0:
                return np.zeros((10, 10, 3), dtype=np.uint8)
            
            # 替换无效值（负值或异常大值）
            array = np.nan_to_num(array, nan=0, posinf=0, neginf=0)
            
            # 判断数据类型和范围
            if array.dtype != np.uint8:
                # 使用Cumulative count cut方法 (2%-98%)
                # 这与QGIS的默认渲染策略相同
                p2 = np.percentile(array, 2)    # 2%的数据小于此值
                p98 = np.percentile(array, 98)  # 98%的数据小于此值
                
                # 避免除零错误
                if p98 - p2 < 0.0001:
                    # 退回到简单的最大最小值归一化
                    min_val = np.min(array)
                    max_val = np.max(array)
                    if max_val - min_val < 0.0001:
                        min_val, max_val = 0, 1
                    normalized = np.clip((array - min_val) / (max_val - min_val) * 255, 0, 255).astype(np.uint8)
                else:
                    # 线性拉伸到0-255范围，使用累积截断值
                    normalized = np.clip((array - p2) / (p98 - p2) * 255, 0, 255).astype(np.uint8)
                
                return normalized
            
            return array
            
        except Exception as e:
            # 如果处理失败，尝试返回原始数组
            if array is not None:
                if array.dtype != np.uint8:
                    return np.clip(array, 0, 255).astype(np.uint8)
                return array
            return np.zeros((10, 10, 3), dtype=np.uint8)
    
    # 使_normalize_array成为_enhance_sentinel_image的别名，保持代码向后兼容
    _normalize_array = _enhance_sentinel_image
    
    @staticmethod
    def get_diagnostic_info():
        """获取诊断信息，用于排查问题"""
        info = {
            'libraries': {
                'rasterio': {
                    'available': RASTERIO_AVAILABLE,
                    'version': rasterio.__version__ if RASTERIO_AVAILABLE else 'N/A'
                },
                'gdal': {
                    'available': GDAL_AVAILABLE,
                    'version': gdal.VersionInfo() if GDAL_AVAILABLE else 'N/A' 
                },
                'pil': {
                    'available': True,
                    'version': Image.__version__
                },
                'numpy': {
                    'available': True,
                    'version': np.__version__
                },
                'shapely': {
                    'available': 'shapely' in sys.modules,
                    'version': shapely.__version__ if 'shapely' in sys.modules else 'N/A'
                },
                'fiona': {
                    'available': 'fiona' in sys.modules,
                    'version': fiona.__version__ if 'fiona' in sys.modules else 'N/A'
                }
            },
            'env_vars': {
                'GDAL_DATA': os.environ.get('GDAL_DATA', '未设置'),
                'PROJ_LIB': os.environ.get('PROJ_LIB', '未设置')
            }
        }
        return info 