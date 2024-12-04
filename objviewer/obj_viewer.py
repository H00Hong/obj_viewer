# -*- coding: utf-8 -*-
import ctypes
from typing import Dict, Sequence

import wx
from mywxwidgets.dataview import DataRow, DataViewModel, dv

from .NdArrayWXShow2D import MainWin

FONT0 = (14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
         False, 'JetBrains Mono')


class _ShowWin(wx.Frame):

    def __init__(self, parent, val=['name', 'type', 'size', 'value', 'obj']):
        wx.Frame.__init__(self, parent, title=val[0], size=(800, 500))
        self._val = val
        self.lab00 = wx.StaticText(self, label='name:')
        self.lab10 = wx.StaticText(self, label=val[0])
        self.lab01 = wx.StaticText(self, label='type:')
        self.lab11 = wx.StaticText(self, label=val[1])
        self.lab02 = wx.StaticText(self, label='size:')
        self.lab12 = wx.StaticText(self, label=val[2])
        self.lab2 = wx.StaticText(self, label='value:')
        self.lab = wx.TextCtrl(self,
                               value=val[3],
                               style=wx.TE_MULTILINE | wx.TE_READONLY
                               | wx.TE_PROCESS_ENTER)
        self.lab.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        # self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self._set_layout()
        self.Show()

    def on_enter(self, event) -> None:
        # print('on_enter')
        b = [i in self._val[1] for i in ('ndarray', 'DataFrame', 'Series')]
        obj = self._val[-1]
        name_ = self._val[0]
        if any(b):
            win_obj = MainWin
            name = name_
        elif self._val[2] == '0':
            win_obj = ObjectViewerFrame
            name = '对象查看器    ' + name_
        elif isinstance(obj, Sequence):
            win_obj = SeqViewerFrame
            name = '序列查看器    ' + name_
        elif isinstance(obj, dict):
            win_obj = DictViewerFrame
            name = '字典查看器    ' + name_
        else:
            win_obj = ObjectViewerFrame
            name = '对象查看器    ' + name_

        win = win_obj(self, obj)  # type: ignore
        win.SetTitle(name)
        win.Show()

    def _line_v(self):
        line = wx.StaticLine(self, style=wx.LI_VERTICAL)
        # line.SetBackgroundColour(wx.Colour(0, 0, 0))
        # line.SetForegroundColour(wx.Colour(0, 0, 0))
        return line

    def _line_h(self):
        line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        # line.SetBackgroundColour(wx.Colour(0, 0, 0))
        # line.SetForegroundColour(wx.Colour(0, 0, 0))
        return line

    def _set_layout(self):
        font = wx.Font(*FONT0)
        self.lab.SetFont(font)
        self.lab00.SetFont(font)
        self.lab01.SetFont(font)
        self.lab02.SetFont(font)
        self.lab10.SetFont(font)
        self.lab11.SetFont(font)
        self.lab12.SetFont(font)
        self.lab2.SetFont(font)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer01 = wx.BoxSizer(wx.VERTICAL)
        sizer02 = wx.BoxSizer(wx.VERTICAL)
        sizer03 = wx.BoxSizer(wx.VERTICAL)
        sizer01.Add(self.lab00, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        # sizer01.Add(self._line_h(), 1, wx.ALL|wx.EXPAND)
        sizer01.Add(self.lab10, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        sizer02.Add(self.lab01, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        # sizer02.Add(self._line_h(), 1, wx.ALL|wx.EXPAND)
        sizer02.Add(self.lab11, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        sizer03.Add(self.lab02, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        # sizer03.Add(self._line_h(), 1, wx.ALL|wx.EXPAND)
        sizer03.Add(self.lab12, 0, wx.ALL | wx.ALIGN_CENTER, 3)

        sizer1.Add(self._line_v(), 0, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(sizer01, 1, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(self._line_v(), 0, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(sizer02, 1, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(self._line_v(), 0, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(sizer03, 1, wx.ALL | wx.EXPAND, 5)
        sizer1.Add(self._line_v(), 0, wx.ALL | wx.EXPAND, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer1, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self._line_h(), 0, wx.SOUTH | wx.EXPAND, 5)
        sizer.Add(self.lab2, 0, wx.WEST | wx.EXPAND, 12)
        sizer.Add(self.lab, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)


class ViewerFrame(wx.Frame):

    def __init__(self,
                 parent=None,
                 dr=(),
                 col=[('name', 210), ('type', 280), ('size', ), ('value', )]):
        wx.Frame.__init__(self, parent=parent, title='对象查看器', size=(1200, 700))

        self.dvc = dv.DataViewCtrl(self,
                                   style=dv.DV_SINGLE | dv.DV_VERT_RULES
                                   | dv.DV_HORIZ_RULES | dv.DV_ROW_LINES)

        self.model = DataViewModel(dr)
        self.dvc.AssociateModel(self.model)
        for i, v in enumerate(col):
            self.dvc.AppendTextColumn(
                v[0], i, dv.DATAVIEW_CELL_ACTIVATABLE,
                v[1] if len(v) > 1 else wx.COL_WIDTH_DEFAULT)

        self.dvc.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED, self.OnLeftDoubleClick)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND | wx.ALL, 5)
        self.dvc.SetFont(wx.Font(*FONT0))
        self.Centre()

    def OnLeftDoubleClick(self, event: dv.DataViewEvent) -> None:
        raise NotImplementedError


def get_len(o):
    try:
        if 'shape' in dir(o):
            len_ = getattr(o, 'shape')
        else:
            len_ = len(o)
    except Exception:
        len_ = 1
    return len_


def set_dr_list(obj, name):
    res = [
        name,
        str(type(obj))[8:-2],
        str(get_len(obj)), obj if isinstance(obj, str) else str(obj), obj
    ]
    return res


def get_drs(lists=[('魔术方法和属性', []), ('方法', []), ('属性', [])], header=None):
    if header:
        dat, ds = [DataRow((0, ), header)], 1
    else:
        ds, dat = 0, []
    for i, v in enumerate(lists):
        # data = [name, type, size, value]
        dat.append(DataRow(
            (i + ds, ), [v[0], '', str(len(v[1])), '', None]))  # type: ignore
        for j, vv in enumerate(v[1]):
            dat.append(DataRow((i + ds, j), vv))
    return dat


class ObjectViewerFrame(ViewerFrame):

    def __init__(
            self,
            parent=None,
            obj=None,
            name: str = '',
            col=[('name', 210), ('type', 280), ('size', ),
                 ('value', )]) -> None:
        ViewerFrame.__init__(self, parent, self._set(obj, name), col)
        self.SetTitle('对象查看器    ' + name)

    def OnLeftDoubleClick(self, event) -> None:
        # print('OnLeftDoubleClick')
        item = event.GetItem()
        _ShowWin(self, self.model.GetDataRow(item).data)

    def _set(self, _obj: object, name: str = ''):
        dirs = dir(_obj)

        dirs_var, dirs_method, dirs_magic = [], [], []
        for v in dirs:
            try:
                obj_ = getattr(_obj, v)
            except:
                continue

            res = set_dr_list(obj_, v)

            if v.startswith('__'):
                dirs_magic.append(res)
            elif 'function' in res[1] or 'method' in res[1]:
                dirs_method.append(res)
            else:
                try:
                    b = isinstance(getattr(_obj.__class__, v), property)
                    t = '——@property' if b else ''
                except Exception:
                    t = ''
                res[1] += t
                dirs_var.append(res)

        return get_drs([('魔术方法和属性', dirs_magic), ('方法', dirs_method),
                        ('属性', dirs_var)], set_dr_list(_obj, name))


class DictViewerFrame(ObjectViewerFrame):

    def __init__(self, parent=None, obj={}) -> None:
        ObjectViewerFrame.__init__(self,
                                   parent,
                                   obj,
                                   col=[('name', 210), ('value_type', 280),
                                        ('size', ), ('value', )])

    def _set(self, _obj: dict, name: str = ''):
        drs = []
        for i, (k, v) in enumerate(_obj.items()):
            if not isinstance(k, str):
                k = str(k)
            drs.append(DataRow((i, ), set_dr_list(v, k)))
        return drs


class SeqViewerFrame(ObjectViewerFrame):

    def __init__(self, parent=None, obj=()):
        ObjectViewerFrame.__init__(self,
                                   parent,
                                   obj,
                                   col=[('index', ), ('type', 180), ('size', ),
                                        ('value', )])

    def _set(self, _obj: Sequence, name: str = ''):
        return [
            DataRow((i, ), set_dr_list(v, str(i))) for i, v in enumerate(_obj)
        ]


class VariableViewerFrame(ViewerFrame):

    def __init__(self, args: Dict[str, object]):
        ViewerFrame.__init__(self, None, self._set(args), [('name', 210),
                                                           ('type', 280),
                                                           ('size', ),
                                                           ('value', )])
        self.SetTitle('变量查看器')
        self.dvc.Expand(self.model.GetItemWithIndex((4, )))

    def OnLeftDoubleClick(self, event):
        # print('OnLeftDoubleClick')
        item = event.GetItem()
        dat = self.model.GetDataRow(item).data
        win = ObjectViewerFrame(self, dat[-1], dat[0])
        win.Show()

    def _set(self, _args: dict):
        dirs_mod, dirs_func, dirs_var, dirs_private, dirs_cls = [], [], [], [], []
        for k, v in _args.items():
            if not isinstance(k, str):
                continue
            res = set_dr_list(v, k)

            _type = res[1].lower()
            if 'module' in _type:
                dirs_mod.append(res)
            elif 'function' in _type or 'ufunc' in _type or 'method' in _type:
                dirs_func.append(res)
            elif 'typ' in _type:
                dirs_cls.append(res)
            elif k.startswith('_'):
                dirs_private.append(res)
            else:
                dirs_var.append(res)

        # [('模块', dirs_mod), ('类', dirs_cls), ('函数', dirs_func), ('私有变量', dirs_private), ('变量', dirs_var)]
        return get_drs([('模块', dirs_mod), ('类', dirs_cls), ('函数', dirs_func),
                        ('私有变量', dirs_private), ('变量', dirs_var)])


# %% 对外接口
def objviewer(obj, name: str = '') -> None:
    """
    对象查看器
    -----
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    app = wx.App()
    frame = ObjectViewerFrame(None, obj, name)
    frame.Show()
    app.MainLoop()


def varviewer(kwargs: Dict[str, object] = locals()) -> None:
    """
    变量空间查看器
    -----
    不可以使用默认参数直接 varViewer(), 需要在所需空间下执行 varViewer(locals())
    """
    if not isinstance(kwargs, dict):
        raise TypeError('kwargs must be dict')
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    app = wx.App()
    frame = VariableViewerFrame(kwargs)
    frame.Show()
    app.MainLoop()
