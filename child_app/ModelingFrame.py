import wx
import pandas as pd
from sklearn.model_selection import train_test_split
from lazypredict.Supervised import LazyClassifier, LazyRegressor
class ModellingFrame(wx.Frame):
    def __init__(self, parent, title, data):
        super(ModellingFrame, self).__init__(parent, title=title, size=(470, 400))

        self.data = data
        self.display()

        self.FrameConfig()

    def display(self):
        self.create_widget()

        columns = self.data.columns.tolist()
        for i in range(len(columns)):
            self.listctrl.InsertItem(i, columns[i])

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
        try:
            test_size = float(self.text_ctrl.GetValue())

            choises1 = self.data.columns.tolist()
            dialog1 = ChoiceDialog(self, choises1, "Target")

            if dialog1.ShowModal() == wx.ID_OK:
                selected_choice1 = dialog1.get_selection()
                print("Bạn đã chọn:", selected_choice1)
            dialog1.Destroy()

            choises2 = ['Regression', 'Clasification']
            dialog2 = ChoiceDialog(self, choises2, "Type Of Target")

            if dialog2.ShowModal() == wx.ID_OK:
                selected_choice2 = dialog2.get_selection()
                print("Bạn đã chọn:", selected_choice2)
            dialog2.Destroy()

            x = self.data.drop(columns = [selected_choice1])
            y = self.data[selected_choice1]

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=1508)

            if selected_choice2 == 'Regression':
                rgs = LazyRegressor()
                models, predictions = rgs.fit(x_train, x_test, y_train, y_test)
                models_name = models['Model'].tolist()
                r2_scores = models['R-Squared'].tolist()

                for i in range(len(models_name)):
                    if i <= self.listctrl.GetItemCount():
                        self.listctrl.SetItem(i, 1, models_name[i])
                        self.listctrl.SetItem(i, 2, str(r2_scores[i]))
                    else:
                        self.listctrl.InsertItem(i, '')
                        self.listctrl.SetItem(i, 1, models_name[i])
                        self.listctrl.SetItem(i, 2, str(r2_scores[i]))
            else:
                clf = LazyClassifier()
                models, predictions = clf.fit(x_train, x_test, y_train, y_test)
                models_name = models['Model'].tolist()
                accuracy_scores = models['Accuracy'].tolist()

                for i in range(len(models_name)):
                    if i <= self.listctrl.GetItemCount():
                        self.listctrl.SetItem(i, 1, models_name[i])
                        self.listctrl.SetItem(i, 2, str(accuracy_scores[i]))
                    else:
                        self.listctrl.InsertItem(i, '')
                        self.listctrl.SetItem(i, 1, models_name[i])
                        self.listctrl.SetItem(i, 2, str(accuracy_scores[i]))
        except Exception as e:
            if str(e) == 'could not convert string to float: \'\'':
                wx.MessageBox('Type of Test Size must be Float', 'Error !!!')
            else:
                wx.MessageBox(str(e), 'Error !!!')

    def FrameConfig(self):
        # Tắt điều chỉnh cửa sổ
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

        # Set ColumnWidth
        for i in range(3):
            self.listctrl.SetColumnWidth(i, self.listctrl.GetSize().GetWidth() // 3)

class ChoiceDialog(wx.Dialog):
    def __init__(self, parent, choices, title):
        super().__init__(parent, title=title, size=(200, 150))

        self.choices = choices

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.choice = wx.Choice(self, choices=choices)
        sizer.Add(self.choice, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        btn_ok = wx.Button(self, wx.ID_OK, "OK")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_ok, 0, wx.ALL, 5)
        btn_sizer.Add(btn_cancel, 0, wx.ALL, 5)

        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)

    def get_selection(self):
        return self.choices[self.choice.GetSelection()]


