"""
gui tools
- objExplorer   对象查看器 可以显示对象属性，方法等
- varExplorer   变量查看器 输入 locals() 查看当前空间的所有变量
- cftool    拟合计算工具
- mplWXWindow   使用 wx 的 matplotlib 图形窗口
- ndarrayWXShow2D  使用 wx 的 ndarray 查看器
"""
from .NdArrayWXShow2D import ndarrayWXShow2D
from .obj_viewer import objviewer, varviewer

__all__ = ['objviewer', 'varviewer', 'ndarrayWXShow2D']
