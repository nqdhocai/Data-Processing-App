import wx
import pandas as pd

class ModellingFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ModellingFrame, self).__init__(parent, title=title, size=(470, 400))

        self.data = pd.read_csv()
        self.create_widget()

        self.FrameConfig()
    def create_widget(self):
        self.panel = wx.Panel(self)

        # Tạo frame con thứ nhất
        self.frame1 = wx.Panel(self.panel)

        # Tạo frame con thứ hai
        self.frame2 = wx.Panel(self.panel)

        # Sắp xếp frame con
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.frame1, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.frame2, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizer(hbox)

        # Thành phần trong frame 1
        self.listctrl = wx.ListCtrl(self.frame1, style = wx.LC_REPORT)
        self.listctrl.InsertColumn(0, 'Columns')
        self.listctrl.InsertColumn(1, 'Models')
        self.listctrl.InsertColumn(2, 'Performance')

        frame1_box = wx.BoxSizer()
        frame1_box.Add(self.listctrl, flag = wx.EXPAND)
        self.frame1.SetSizer(frame1_box)

        # Thành phần trong frame 2
        child_frame_21 = wx.Panel(self.frame2)
        child_frame_22 = wx.Panel(self.frame2)

        label = wx.StaticText(child_frame_21, label="Test Size:")
        self.text_ctrl = wx.TextCtrl(child_frame_21)
        lazy_predict_button = wx.Button(child_frame_22, label = 'Lazy Predict')
        lazy_predict_button.Bind(wx.EVT_BUTTON, self.lazy_predict,)

        frame21_box = wx.BoxSizer(wx.HORIZONTAL)
        frame21_box.Add(label, 1, flag = wx.ALIGN_CENTER|wx.ALL, border = 5)
        frame21_box.Add(self.text_ctrl, 1, flag = wx.ALIGN_CENTER|wx.ALL, border = 5)
        child_frame_21.SetSizer(frame21_box)

        frame22_box = wx.BoxSizer(wx.HORIZONTAL)
        frame22_box.Add(lazy_predict_button, 1, flag = wx.ALIGN_CENTER|wx.ALL, border = 5)
        child_frame_22.SetSizer(frame22_box)

        frame2_box = wx.BoxSizer(wx.VERTICAL)
        frame2_box.Add(child_frame_21, 1, flag = wx.EXPAND)
        frame2_box.Add(child_frame_22, 1, flag = wx.EXPAND)

        self.frame2.SetSizer(frame2_box)
    def lazy_predict(self, event):
        test_size = self.text_ctrl.GetValue()
        pass
    def FrameConfig(self):
        # Tắt điều chỉnh cửa sổ
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

        # Set ColumnWidth
        for i in range(3):
            self.listctrl.SetColumnWidth(i, self.listctrl.GetSize().GetWidth() // 3)


myapp = wx.App()
frame = ModellingFrame(None, '')
frame.Show()
myapp.MainLoop()