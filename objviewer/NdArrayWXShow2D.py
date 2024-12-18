# -*- coding: utf-8 -*-
"""
gui_wxpython
显示ndarray 平面2d 多维在SpinCtrl中选择
"""
from typing import List, Union

import numpy as np
import wx
from mywxwidgets.grid import COPY, gridnumpy
from numpy import ndarray
from pandas import DataFrame, Series

FONT0 = gridnumpy.gridbase.FONT0
FONT1 = (10, *FONT0[1:])


class Grid(gridnumpy.Grid):

    _MENU_ITEM = ((COPY, '复制  Ctrl+C'), )

    def __init__(self, parent, data=None):
        super().__init__(parent, gridnumpy.DataBaseNP(data, show_format='{:.6g}'))

    def onKeyDown(self, event: wx.KeyEvent):
        key_code = event.GetKeyCode()  # 获取按键编码
        modifiers = event.GetModifiers()  # 获取按键修饰符
        if modifiers == 2 and key_code == 67:  # 修饰符为ctrl并且按下的是c
            self._OnCopy(event)


def _line_h(parent):
    return wx.StaticLine(parent, style=wx.LI_HORIZONTAL)


def _line_v(parent):
    return wx.StaticLine(parent, style=wx.LI_VERTICAL)


class MainWin(wx.Frame):

    def __init__(self, parent, data: Union[ndarray, DataFrame, Series]):
        wx.Frame.__init__(self, parent, size=(800, 700))
        # self.setWindowTitle(title)
        if not isinstance(data, (ndarray, DataFrame, Series)):
            data = np.asarray(data)
        self.data = data
        self._colour = wx.Colour(230, 230, 230)
        self._init_ui()
        self.SetBackgroundColour(self._colour)
        # self.tab.SetDefaultCellBackgroundColour(self._colour)
        self.tab.SetGridLineColour(wx.Colour(10, 10, 10))

    def _init_ui(self):
        self.layout0 = wx.BoxSizer(wx.VERTICAL)
        self.lab_data_info = wx.StaticText(self)
        self.lab_data_info.SetFont(wx.Font(*FONT0))
        self.layout0.Add(self.lab_data_info, 0, wx.ALL | wx.EXPAND, 5)

        type_ = str(self.data.__class__).rpartition('.')[-1][:-2]
        if isinstance(self.data, (DataFrame, Series)):
            dtype = self.data.to_numpy().dtype
        else:
            dtype = self.data.dtype
        self.lab_data_info.SetLabel(
            'type = {}, dtype = {}, ndim = {}, shape = {}, size = {}'.format(
                type_, dtype, self.data.ndim, self.data.shape, self.data.size))

        self._init_tab()
        self._init_spin()
        self.SetSizer(self.layout0)

    def _init_tab(self):
        if self.data.ndim == 0:
            dat = np.asarray([[self.data]])
        elif self.data.ndim == 1:
            dat = np.asarray(self.data).reshape([self.data.size, 1])
        elif self.data.ndim == 2:
            dat = self.data
        else:
            dat = self.data[(0,)*(self.data.ndim - 2)]

        self.tab = Grid(self, data=dat)

        self.layout0.Add(self.tab, 1, wx.ALL | wx.EXPAND, 5)
        if isinstance(self.data, DataFrame):
            self.tab.dataBase.SetRowLabels(self.data.index)
            self.tab.dataBase.SetColLabels(self.data.columns)
        elif isinstance(self.data, Series):
            self.tab.dataBase.SetRowLabels(self.data.index)
        else:
            self.tab.dataBase.SetRowLabels(range(dat.shape[-2]))
            self.tab.dataBase.SetColLabels(range(dat.shape[-1]))
        self.tab.SetDefaultColSize(100, True)

    def _init_spin(self):
        font0 = wx.Font(*FONT0)
        self.layout_spin = wx.BoxSizer(wx.HORIZONTAL)
        self.lab_spin_begin = wx.StaticText(self, label='维度: ( ')
        self.lab_spin_begin.SetFont(font0)
        self.layout_spin.Add(self.lab_spin_begin, 0, wx.ALIGN_CENTER | wx.WEST,
                             5)
        self.spins: List[wx.SpinCtrl] = []
        ndim = self.data.ndim
        if ndim > 2:
            for id in range(ndim - 2):
                self._set_spin(id)
        if ndim == 0:
            tex = ')'
        elif ndim == 1:
            tex = '{}, )'.format(self.data.shape[-1])
        else:
            tex = '{}, {} )'.format(self.data.shape[-2], self.data.shape[-1])
        lab_spin_end = wx.StaticText(self, label=tex)
        lab_spin_end.SetFont(font0)
        lab_n = wx.StaticText(self, label='显示数位: ')
        lab_n.SetFont(font0)
        self.spin_n = wx.SpinCtrl(self, value='6')
        self.spin_n.SetFont(wx.Font(*FONT1))
        self.spin_n.SetBackgroundColour(self._colour)
        self.spin_n.Bind(wx.EVT_SPINCTRL, self._spin_type_change)
        lab_t = wx.StaticText(self, label='显示类型: ')
        lab_t.SetFont(font0)
        self.combo_t = wx.Choice(self, choices=['g', 'f', 'e', 'd'])
        self.combo_t.SetSelection(0)
        self.combo_t.Bind(wx.EVT_CHOICE, self._spin_type_change)
        self.combo_t.SetFont(wx.Font(*FONT1))

        self.layout_spin.Add(lab_spin_end, 0, wx.ALIGN_CENTER)
        self.layout_spin.Add(wx.StaticText(self, label=''), 1, wx.EXPAND)
        self.layout_spin.Add(_line_v(self), 0, wx.EXPAND | wx.EAST, 5)
        self.layout_spin.Add(lab_n, 0, wx.ALIGN_CENTER)
        self.layout_spin.Add(self.spin_n, 0, wx.ALIGN_CENTER | wx.EAST, 10)
        self.layout_spin.Add(lab_t, 0, wx.ALIGN_CENTER)
        self.layout_spin.Add(self.combo_t, 0, wx.ALIGN_CENTER | wx.EAST, 5)
        self.layout0.Add(self.layout_spin, 0, wx.ALL | wx.EXPAND, 5)

    def _set_spin(self, id: int):
        spin = wx.SpinCtrl(self,
                           value='0',
                           min=-self.data.shape[id],
                           max=self.data.shape[id] - 1)
        spin.SetFont(wx.Font(*FONT1))
        spin.Bind(wx.EVT_SPINCTRL, self._spin_data_change)
        self.layout_spin.Add(spin, 0, wx.ALIGN_CENTER)
        self.spins.append(spin)
        spin.SetBackgroundColour(self._colour)

        lab_spin = wx.StaticText(self, label=', ')
        lab_spin.SetFont(wx.Font(*FONT0))
        self.layout_spin.Add(lab_spin, 0, wx.ALIGN_CENTER)

    def _spin_data_change(self, event: wx.SpinEvent):
        index = tuple(spin.GetValue() for spin in self.spins)
        self.tab.SetData(self.data[index])

    def _spin_type_change(self, event: wx.CommandEvent):
        self.tab.dataBase.SetShowFormat('{:.' + str(self.spin_n.GetValue()) +
                                        self.combo_t.GetStringSelection() + '}')
        self.tab.dataBase.ValuesUpdated()
        self.Refresh()


def ndarray_wxshow_2d(data, title=''):
    """
    显示ndarray的wx实现

    :param data: numpy array or pandas DataFrame/Series
    :param title: str, 窗口标题
    :return: None
    """
    if isinstance(data, (ndarray, DataFrame, Series)):
        pass
    elif isinstance(data, (list, tuple, range)):
        data = np.asarray(data)
    elif isinstance(data, dict):
        data = Series(data)

    app = wx.App()
    win = MainWin(None, data)
    win.SetTitle(title)
    win.Show()
    app.MainLoop()


if __name__ == '__main__':
    a = np.random.rand(144)
    # a = np.arange(144)
    a1 = a.reshape([2, 3, 2, 3, 4])
    # a1 = a.reshape((36,4))
    # a1 = nar(['0,0', '1,0'])
    # a1 = DataFrame([[1, 2], [2, 3]], index=['a0', 'a1'], columns=['b1', 'b2'])
    # a1 = {'a0': [1, 2], 'a1': [2, 3]}
    ndarray_wxshow_2d(a1, 'a1')
