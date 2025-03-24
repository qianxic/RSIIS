# 渔网分割模块API说明

## 模型层 API (Function/data/fishnet_seg.py)

### FishnetSegmentation 类

#### 初始化

```python
def __init__(self):
    """初始化渔网分割模型实例"""
```

#### 图像加载

```python
def load_image(self, image_path):
    """
    加载图像文件
    
    参数:
        image_path (str): 图像文件路径
        
    返回:
        bool: 加载是否成功
        dict: 图像信息 (宽度，高度，通道数等)
              失败时返回 {"error": 错误信息}
    """
```

#### 网格参数设置

```python
def set_grid_parameters(self, grid_count):
    """
    设置网格参数
    
    参数:
        grid_count (tuple): (rows, cols) 表示网格的行数和列数
        
    返回:
        bool: 设置是否成功
        dict: 计算出的网格信息，包含 grid_count, grid_size, image_size
              失败时返回 {"error": 错误信息}
    """
```

#### 网格生成

```python
def generate_grid(self):
    """
    生成网格分割
    
    返回:
        bool: 分割是否成功
        list: 分割结果列表，每个元素为一个字典，包含位置、行列信息和图像数据
              失败时返回 {"error": 错误信息}
    """
```

#### 结果导出

```python
def export_result(self, export_dir, create_subfolders=True):
    """
    导出分割结果
    
    参数:
        export_dir (str): 导出目录
        create_subfolders (bool): 是否创建子文件夹
        
    返回:
        bool: 导出是否成功
        dict: 导出信息，包含 save_dir, files_count, files
              失败时返回 {"error": 错误信息}
    """
```

#### 示意图创建

```python
def create_overview_image_for_ui(self):
    """
    创建分割示意图，用于UI显示
    
    返回:
        dict: 包含示意图图像数据和元数据的字典，可用于UI层创建预览图像
             失败时返回 None
    """
```

#### UI兼容结果获取

```python
def get_ui_compatible_results(self):
    """
    获取用于UI显示的兼容结果
    
    返回:
        list: 转换后的分割结果列表，适用于UI层
    """
```

## 控制器层 API (controller/event/fishnet_controller.py)

### FishnetController 类

#### 初始化

```python
def __init__(self, parent=None):
    """
    初始化渔网分割控制器
    
    参数:
        parent (QObject): 父对象
    """
```

#### 功能设置

```python
def setup(self, grid_generator=None):
    """
    设置功能层引用
    
    参数:
        grid_generator: 网格生成器实例（可选）
    """
```

#### 图像导入

```python
def import_image(self):
    """
    导入遥感影像
    
    返回:
        bool: 导入是否成功
    """
```

#### 参数设置

```python
def set_grid_params(self):
    """
    设置网格参数 - 使用对话框让用户以网格数量方式输入参数
    
    返回:
        bool: 参数设置是否成功
    """
```

#### 开始分割

```python
def start_fishnet(self):
    """
    开始渔网分割
    
    返回:
        bool: 分割是否成功
    """
```

#### 预览显示

```python
def show_preview(self):
    """
    显示渔网分割预览窗口
    """
```

```python
def show_detailed_preview(self):
    """
    显示带有详细分割预览的窗口
    """
```

#### 结果导出

```python
def export_result(self):
    """
    导出分割结果
    
    返回:
        bool: 导出是否成功
    """
```

## UI组件 API (ui/widgets/grid_dialogs.py)

### GridParamsDialog 类

```python
def __init__(self, parent=None, image_size=(0, 0), current_rows=4, current_cols=4):
    """
    网格参数设置对话框
    
    参数:
        parent: 父窗口
        image_size (tuple): 图像尺寸 (宽, 高)
        current_rows (int): 当前行数设置
        current_cols (int): 当前列数设置
    """
```

```python
def get_params(self):
    """
    获取设置的参数
    
    返回:
        dict: 包含设置的参数，格式为 {"grid_count": (rows, cols)}
    """
```

### ImageViewer 类

```python
def __init__(self, parent=None):
    """
    图像查看器控件，支持缩放
    
    参数:
        parent: 父窗口
    """
```

```python
def setPixmap(self, pixmap):
    """
    设置要显示的图像
    
    参数:
        pixmap (QPixmap): 要显示的图像
    """
```

### GridOverviewWindow 类

```python
def __init__(self, image_path, grid_result, fishnet_model=None, parent=None):
    """
    渔网分割示意图窗口
    
    参数:
        image_path (str): 原始图像路径
        grid_result (list): 分割结果列表
        fishnet_model (FishnetSegmentation): 模型实例（可选）
        parent: 父窗口
    """
```

### GridPreviewWindow 类

```python
def __init__(self, image_path, grid_result, fishnet_model=None, parent=None):
    """
    渔网分割预览窗口
    
    参数:
        image_path (str): 原始图像路径
        grid_result (list): 分割结果列表
        fishnet_model (FishnetSegmentation): 模型实例（可选）
        parent: 父窗口
    """
```

### GridImagesViewer 类

```python
def __init__(self, grid_result, fishnet_model=None, parent=None):
    """
    渔网分割图像浏览器
    
    参数:
        grid_result (list): 分割结果列表
        fishnet_model (FishnetSegmentation): 模型实例（可选）
        parent: 父窗口
    """
```

## 测试模块 API (test_fishnet.py)

```python
def test_fishnet_ui():
    """
    测试渔网分割UI和控制器
    
    返回:
        int: 应用程序退出代码
    """
```

## 数据结构

### 网格参数 (Grid Parameters)

```python
{
    "grid_count": (rows, cols)  # 网格行数和列数
}
```

### 图像信息 (Image Info)

```python
{
    "width": width,          # 图像宽度
    "height": height,        # 图像高度
    "mode": image.mode,      # 图像模式（如"RGB"）
    "format": image.format   # 图像格式（如"JPEG"）
}
```

### 网格信息 (Grid Info)

```python
{
    "grid_count": (rows, cols),   # 网格行数和列数
    "grid_size": (width, height), # 每个网格的像素尺寸
    "image_size": (width, height) # 原始图像尺寸
}
```

### 分割结果 (Grid Result)

```python
{
    'position': (x, y, width, height),  # 网格在原图中的位置和尺寸
    'image_data': PIL_Image_Object,     # 模型层中的网格图像（PIL对象）
    'row': row_number,                  # 行号（从1开始）
    'col': col_number                   # 列号（从1开始）
}
```

### UI兼容的分割结果 (UI Compatible Result)

```python
{
    'position': (x, y, width, height),  # 网格在原图中的位置和尺寸
    'row': row_number,                  # 行号（从1开始）
    'col': col_number,                  # 列号（从1开始）
    'image': QImage_Object              # UI层的网格图像（QImage对象）
}
```

### 导出信息 (Export Info)

```python
{
    "save_dir": directory_path,  # 保存目录路径
    "files_count": number,       # 保存的文件数量
    "files": [file_paths]        # 所有保存的文件路径列表
}
```

### 错误信息 (Error Info)

```python
{
    "error": error_message  # 错误描述信息
}
```

## 模块间数据流

1. **用户 → FishnetPage → FishnetController**
   - UI事件（按钮点击）
   - 文件选择结果

2. **FishnetController → FishnetSegmentation**
   - 图像路径
   - 网格参数
   - 导出目录

3. **FishnetSegmentation → FishnetController**
   - 操作结果（成功/失败）
   - 图像信息
   - 网格信息
   - 分割结果列表
   - 导出信息
   - 错误信息

4. **FishnetController → UI组件**
   - 处理后的分割结果（UI兼容格式）
   - 成功/错误消息
   - 预览窗口配置 