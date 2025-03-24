import os
import sys
import traceback
import numpy as np
from osgeo import gdal, ogr, osr
import warnings

# 尝试导入矢量处理库
try:
    import shapely
    from shapely.geometry import Polygon, mapping
    import fiona
    from fiona.crs import from_epsg
    VECTOR_LIBS_AVAILABLE = True
except ImportError:
    VECTOR_LIBS_AVAILABLE = False

# 本地导入
from utils.geo.raster_loader import RasterData


class VectorUtils:
    """
    矢量数据处理工具类，提供栅格转矢量、矢量格式转换等功能
    """
    
    @staticmethod
    def grid_to_shapefile(raster_data, grid_result, output_path, attributes=None):
        """
        将分割网格结果转换为shapefile文件
        
        Args:
            raster_data: RasterData对象，包含原始栅格数据信息
            grid_result: 分割结果列表，每个元素为一个字典，包含位置信息
            output_path: 输出shapefile文件路径
            attributes: 额外属性字段，可选
            
        Returns:
            bool: 是否成功
            str: 错误消息或成功信息
        """
        if not VECTOR_LIBS_AVAILABLE:
            return False, "缺少必要的矢量库（shapely, fiona）"
        
        try:
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 定义shapefile模式（schema）
            schema = {
                'geometry': 'Polygon',
                'properties': {
                    'id': 'int',
                    'row': 'int',
                    'col': 'int',
                    'width': 'float',
                    'height': 'float'
                }
            }
            
            # 添加额外属性字段
            if attributes:
                for attr_name, attr_type in attributes.items():
                    schema['properties'][attr_name] = attr_type
            
            # 创建一个新的shapefile
            crs = None
            if raster_data.is_geotiff and raster_data.crs:
                # 使用栅格数据的坐标系
                if hasattr(raster_data.crs, 'to_wkt'):
                    crs = raster_data.crs.to_wkt()
                else:
                    crs = raster_data.crs
            
            # 如果没有获取到有效的CRS，使用默认的WGS84
            if not crs:
                crs = from_epsg(4326)  # WGS84
            
            with fiona.open(output_path, 'w', driver='ESRI Shapefile', crs=crs, schema=schema) as shp:
                for i, grid in enumerate(grid_result):
                    # 获取网格位置信息
                    x, y, grid_width, grid_height = grid['position']
                    row, col = grid['row'], grid['col']
                    
                    # 如果有地理参考信息，转换为地理坐标
                    if raster_data.is_geotiff and raster_data.geo_transform:
                        # 使用地理变换将像素坐标转换为地理坐标
                        transform = raster_data.geo_transform
                        
                        # 计算四个角点的地理坐标
                        geom = VectorUtils._pixel_to_geom(
                            transform, 
                            x, y, 
                            grid_width, grid_height
                        )
                    else:
                        # 没有地理参考信息，使用像素坐标
                        geom = Polygon([
                            (x, y),
                            (x + grid_width, y),
                            (x + grid_width, y + grid_height),
                            (x, y + grid_height),
                            (x, y)
                        ])
                    
                    # 创建要素属性
                    props = {
                        'id': i + 1,
                        'row': row,
                        'col': col,
                        'width': float(grid_width),
                        'height': float(grid_height)
                    }
                    
                    # 添加额外属性
                    if attributes:
                        for attr_name in attributes.keys():
                            if attr_name in grid:
                                props[attr_name] = grid[attr_name]
                            else:
                                props[attr_name] = None
                    
                    # 添加要素到shapefile
                    shp.write({
                        'geometry': mapping(geom),
                        'properties': props
                    })
            
            return True, f"成功导出矢量文件：{output_path}"
            
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            return False, f"导出矢量文件失败: {str(e)}\n{error_details}"
    
    @staticmethod
    def _pixel_to_geom(transform, pixel_x, pixel_y, pixel_width, pixel_height):
        """
        将像素坐标转换为地理坐标并创建多边形
        
        Args:
            transform: 地理变换（仿射变换矩阵）
            pixel_x, pixel_y: 像素坐标（左上角）
            pixel_width, pixel_height: 像素尺寸
        
        Returns:
            shapely.geometry.Polygon: 地理坐标下的多边形
        """
        # 计算四个角点的地理坐标
        if hasattr(transform, '__call__'):
            # rasterio风格的transform
            ul_x, ul_y = transform * (pixel_x, pixel_y)
            ur_x, ur_y = transform * (pixel_x + pixel_width, pixel_y)
            lr_x, lr_y = transform * (pixel_x + pixel_width, pixel_y + pixel_height)
            ll_x, ll_y = transform * (pixel_x, pixel_y + pixel_height)
        else:
            # GDAL风格的transform
            geo_transform = transform
            ul_x = geo_transform[0] + pixel_x * geo_transform[1]
            ul_y = geo_transform[3] + pixel_y * geo_transform[5]
            
            ur_x = geo_transform[0] + (pixel_x + pixel_width) * geo_transform[1]
            ur_y = geo_transform[3] + pixel_y * geo_transform[5]
            
            lr_x = geo_transform[0] + (pixel_x + pixel_width) * geo_transform[1]
            lr_y = geo_transform[3] + (pixel_y + pixel_height) * geo_transform[5]
            
            ll_x = geo_transform[0] + pixel_x * geo_transform[1]
            ll_y = geo_transform[3] + (pixel_y + pixel_height) * geo_transform[5]
        
        # 创建Polygon
        return Polygon([
            (ul_x, ul_y),
            (ur_x, ur_y),
            (lr_x, lr_y),
            (ll_x, ll_y),
            (ul_x, ul_y)
        ])
    
    @staticmethod
    def raster_to_vector(raster_data, output_path, band_index=1, threshold=0):
        """
        将栅格数据转换为矢量数据
        
        Args:
            raster_data: RasterData对象
            output_path: 输出矢量文件路径
            band_index: 波段索引，默认为1
            threshold: 阈值，大于该值的像素将被矢量化
            
        Returns:
            bool: 是否成功
            str: 错误消息或成功信息
        """
        if not VECTOR_LIBS_AVAILABLE:
            return False, "缺少必要的矢量库（shapely, fiona）"
        
        try:
            # 确保有GDAL数据集
            if not raster_data.gdal_dataset and raster_data.is_geotiff:
                # 尝试创建GDAL数据集
                raster_data.gdal_dataset = gdal.Open(raster_data.image_path, gdal.GA_ReadOnly)
                if not raster_data.gdal_dataset:
                    return False, "无法创建GDAL数据集"
            
            # 如果没有GDAL数据集但有数组，则从数组创建临时文件
            if not raster_data.gdal_dataset and raster_data.array is not None:
                temp_path = output_path + ".temp.tif"
                driver = gdal.GetDriverByName('GTiff')
                if len(raster_data.array.shape) == 3:
                    # 多波段
                    bands = raster_data.array.shape[2]
                    out_ds = driver.Create(temp_path, raster_data.width, raster_data.height, 
                                         bands, gdal.GDT_Byte)
                    for b in range(bands):
                        out_ds.GetRasterBand(b+1).WriteArray(raster_data.array[:,:,b])
                else:
                    # 单波段
                    out_ds = driver.Create(temp_path, raster_data.width, raster_data.height, 
                                         1, gdal.GDT_Byte)
                    out_ds.GetRasterBand(1).WriteArray(raster_data.array)
                
                out_ds = None  # 关闭并写入文件
                raster_data.gdal_dataset = gdal.Open(temp_path, gdal.GA_ReadOnly)
            
            # 如果还是无法获取GDAL数据集，返回错误
            if not raster_data.gdal_dataset:
                return False, "无法创建GDAL数据集"
            
            # 创建输出矢量文件
            driver = ogr.GetDriverByName('ESRI Shapefile')
            
            # 删除已存在的文件
            if os.path.exists(output_path):
                driver.DeleteDataSource(output_path)
            
            # 创建新文件
            out_ds = driver.CreateDataSource(output_path)
            
            # 创建空间参考
            srs = osr.SpatialReference()
            if raster_data.crs:
                if isinstance(raster_data.crs, str):
                    srs.ImportFromWkt(raster_data.crs)
                elif hasattr(raster_data.crs, 'to_wkt'):
                    srs.ImportFromWkt(raster_data.crs.to_wkt())
                else:
                    srs.ImportFromEPSG(4326)  # 默认WGS84
            else:
                srs.ImportFromEPSG(4326)  # 默认WGS84
            
            # 创建图层
            layer = out_ds.CreateLayer('polygonized', srs=srs)
            
            # 添加字段
            fd = ogr.FieldDefn('DN', ogr.OFTInteger)
            layer.CreateField(fd)
            
            # 执行栅格转矢量
            src_band = raster_data.gdal_dataset.GetRasterBand(band_index)
            
            # 使用GDAL的多边形化功能
            gdal.Polygonize(src_band, src_band.GetMaskBand(), layer, 0, [], 
                          callback=None)
            
            # 关闭资源
            out_ds = None
            
            # 删除临时文件（如果有）
            if os.path.exists(output_path + ".temp.tif"):
                os.remove(output_path + ".temp.tif")
            
            return True, f"成功导出矢量文件：{output_path}"
        
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            
            # 删除临时文件（如果有）
            if os.path.exists(output_path + ".temp.tif"):
                try:
                    os.remove(output_path + ".temp.tif")
                except:
                    pass
                
            return False, f"栅格转矢量失败: {str(e)}\n{error_details}"

    @staticmethod
    def merge_shapefiles(input_shps, output_shp):
        """
        合并多个shapefile文件
        
        Args:
            input_shps: 输入shapefile文件路径列表
            output_shp: 输出shapefile文件路径
            
        Returns:
            bool: 是否成功
            str: 错误消息或成功信息
        """
        if not VECTOR_LIBS_AVAILABLE:
            return False, "缺少必要的矢量库（fiona）"
            
        try:
            # 确保输入文件存在
            for shp in input_shps:
                if not os.path.exists(shp):
                    return False, f"文件不存在: {shp}"
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_shp)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 从第一个文件获取schema和crs
            with fiona.open(input_shps[0], 'r') as src:
                schema = src.schema
                crs = src.crs
                
                # 创建输出文件
                with fiona.open(output_shp, 'w', driver='ESRI Shapefile', schema=schema, crs=crs) as dst:
                    # 遍历所有输入文件并合并
                    for shp in input_shps:
                        with fiona.open(shp, 'r') as src_file:
                            for feature in src_file:
                                dst.write(feature)
            
            return True, f"成功合并矢量文件：{output_shp}"
            
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            return False, f"合并矢量文件失败: {str(e)}\n{error_details}" 