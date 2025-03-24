"""
地理空间数据处理工具示例
演示如何使用栅格加载和矢量处理工具
"""

import os
import sys
import argparse
from pathlib import Path

# 导入地理空间数据处理工具
from utils.geo import RasterLoader, VectorUtils
from utils.geo import RASTERIO_AVAILABLE, GDAL_AVAILABLE, VECTOR_LIBS_AVAILABLE


def show_diagnostics():
    """显示诊断信息"""
    from utils.geo.raster_loader import RasterLoader
    diag_info = RasterLoader.get_diagnostic_info()
    
    print("\n=== 环境诊断信息 ===")
    print(f"GDAL可用: {diag_info['libraries']['gdal']['available']}, 版本: {diag_info['libraries']['gdal']['version']}")
    print(f"rasterio可用: {diag_info['libraries']['rasterio']['available']}, 版本: {diag_info['libraries']['rasterio']['version']}")
    print(f"shapely可用: {diag_info['libraries']['shapely']['available']}, 版本: {diag_info['libraries']['shapely']['version']}")
    print(f"fiona可用: {diag_info['libraries']['fiona']['available']}, 版本: {diag_info['libraries']['fiona']['version']}")
    print(f"PIL版本: {diag_info['libraries']['pil']['version']}")
    print(f"NumPy版本: {diag_info['libraries']['numpy']['version']}")
    
    print("\n环境变量:")
    print(f"GDAL_DATA: {diag_info['env_vars']['GDAL_DATA']}")
    print(f"PROJ_LIB: {diag_info['env_vars']['PROJ_LIB']}")


def load_and_display_info(image_path):
    """加载栅格数据并显示信息"""
    print(f"\n=== 加载图像 {image_path} ===")
    
    # 加载栅格数据
    raster, success = RasterLoader.load(image_path)
    
    if not success:
        print(f"加载失败: {raster.error_message}")
        return None
    
    # 显示基本信息
    print(f"图像大小: {raster.width} x {raster.height}")
    print(f"波段数: {raster.bands_count}")
    print(f"是否GeoTIFF: {raster.is_geotiff}")
    
    if raster.is_geotiff:
        print(f"坐标系: {raster.crs}")
        print(f"是否Sentinel: {raster.is_sentinel}")
        if raster.band_names:
            print("波段信息:")
            for i, name in enumerate(raster.band_names):
                print(f"  波段 {i+1}: {name}")
    
    # 保存为PNG（无论输入格式如何）
    output_dir = os.path.join(os.path.dirname(image_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    png_path = os.path.join(output_dir, f"{base_name}_preview.png")
    
    print(f"\n保存预览图像: {png_path}")
    raster.image.save(png_path)
    
    return raster


def grid_split_and_vectorize(raster, rows=2, cols=2):
    """分割栅格并创建矢量数据"""
    if not raster:
        return
        
    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(raster.image_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(raster.image_path))[0]
    
    print(f"\n=== 分割图像 {rows}x{cols} ===")
    
    # 计算网格尺寸
    width, height = raster.width, raster.height
    grid_width = width // cols
    grid_height = height // rows
    
    print(f"网格大小: {grid_width} x {grid_height} 像素")
    
    # 生成网格
    grid_results = []
    for row in range(rows):
        for col in range(cols):
            x = col * grid_width
            y = row * grid_height
            actual_width = grid_width
            actual_height = grid_height
            
            # 处理边缘情况
            if col == cols - 1:
                actual_width = width - x
            if row == rows - 1:
                actual_height = height - y
                
            # 裁剪图像
            box = (x, y, x + actual_width, y + actual_height)
            grid_img = raster.image.crop(box)
            
            # 保存到结果中
            grid_results.append({
                'position': (x, y, actual_width, actual_height),
                'image_data': grid_img,
                'row': row + 1,
                'col': col + 1
            })
            
            # 保存裁剪图像
            grid_png = os.path.join(output_dir, f"{base_name}_grid_{row+1}_{col+1}.png")
            grid_img.save(grid_png)
            print(f"保存网格 ({row+1},{col+1}): {grid_png}")
    
    # 导出网格边界为矢量文件
    if VECTOR_LIBS_AVAILABLE:
        print("\n=== 导出矢量数据 ===")
        shp_path = os.path.join(output_dir, f"{base_name}_grid_vector.shp")
        success, message = VectorUtils.grid_to_shapefile(raster, grid_results, shp_path)
        if success:
            print(f"成功导出矢量文件: {shp_path}")
        else:
            print(f"矢量导出失败: {message}")
    else:
        print("\n矢量库不可用，跳过矢量数据导出")


def example_raster_to_vector(raster):
    """将整个栅格转换为矢量（栅格矢量化示例）"""
    if not raster:
        return
        
    if not GDAL_AVAILABLE:
        print("\n栅格转矢量需要GDAL库，跳过此示例")
        return
        
    output_dir = os.path.join(os.path.dirname(raster.image_path), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(raster.image_path))[0]
    
    print(f"\n=== 栅格转矢量示例 ===")
    shp_path = os.path.join(output_dir, f"{base_name}_vector.shp")
    success, message = VectorUtils.raster_to_vector(raster, shp_path)
    
    if success:
        print(f"成功将栅格转换为矢量: {shp_path}")
    else:
        print(f"栅格转矢量失败: {message}")


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="地理空间数据处理工具示例")
    parser.add_argument("image", nargs='?', help="输入图像文件路径")
    parser.add_argument("--diag", action="store_true", help="显示诊断信息")
    parser.add_argument("--rows", type=int, default=2, help="网格行数")
    parser.add_argument("--cols", type=int, default=2, help="网格列数")
    parser.add_argument("--vector", action="store_true", help="执行栅格转矢量示例")
    
    args = parser.parse_args()
    
    # 显示诊断信息
    if args.diag:
        show_diagnostics()
    
    # 如果提供了图像路径，执行处理流程
    if args.image:
        # 检查文件是否存在
        if not os.path.exists(args.image):
            print(f"错误: 文件不存在 - {args.image}")
            return
            
        # 加载并显示图像信息
        raster = load_and_display_info(args.image)
        
        if raster:
            # 执行网格分割和矢量化
            grid_split_and_vectorize(raster, args.rows, args.cols)
            
            # 可选：执行栅格转矢量示例
            if args.vector:
                example_raster_to_vector(raster)
    else:
        if not args.diag:
            print("请提供图像文件路径或使用 --diag 查看诊断信息")
            parser.print_help()


if __name__ == "__main__":
    main() 