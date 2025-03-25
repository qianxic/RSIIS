#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试修改后的渔网分割功能
确保它能在控制台输出裁剪信息而不显示示意图窗口
"""

import os
import sys
import traceback

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 导入必要的模块
try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from controller.event.fishnet_controller import FishnetController
    print("成功导入必要模块")
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

def test_fishnet_segmentation():
    """测试渔网分割功能"""
    print("=" * 50)
    print("开始测试渔网分割功能")
    print("=" * 50)
    
    # 创建QApplication实例
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建控制器实例
    controller = FishnetController()
    print("创建FishnetController实例成功")
    
    # 指定测试图像路径
    image_path = r"C:\Users\qianx\Desktop\Xindu_Sentinel2_clip_2020_float32_scaled.tif"
    if not os.path.exists(image_path):
        print(f"警告: 测试图像不存在 ({image_path})")
        print("请修改脚本中的图像路径为您系统上有效的图像路径")
        return False
    
    # 导入图像
    print(f"\n导入图像: {image_path}")
    # 模拟导入图像
    controller.current_image_path = image_path
    success, _ = controller.fishnet_model.load_image(image_path)
    if success:
        print(f"图像导入成功")
    else:
        print(f"图像导入失败")
        return False
    
    # 设置网格参数
    print("\n设置网格参数 (2x2)")
    success, grid_info = controller.fishnet_model.set_grid_parameters((2, 2))
    if success:
        print(f"网格参数设置成功: {grid_info}")
    else:
        print(f"网格参数设置失败")
        return False
    
    # 开始渔网分割
    print("\n开始渔网分割")
    try:
        result = controller.start_fishnet()
        print(f"渔网分割结果: {result}")
    except Exception as e:
        print(f"渔网分割出错: {e}")
        traceback.print_exc()
        return False
    
    print("\n测试完成")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_fishnet_segmentation()
    sys.exit(0 if success else 1) 