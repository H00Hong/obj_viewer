"""
gui tools
- objExplorer   对象查看器 可以显示对象属性，方法等
- varExplorer   变量查看器 输入 locals() 查看当前空间的所有变量
- ndarray_wxshow_2d  使用 wx 的 ndarray 查看器
"""
from .NdArrayWXShow2D import ndarray_wxshow_2d
from .obj_viewer import objviewer, varviewer

__all__ = ['objviewer', 'varviewer', 'ndarray_wxshow_2d']
__version__ = '0.0.8'
__updated__ = "2025-5-13"
