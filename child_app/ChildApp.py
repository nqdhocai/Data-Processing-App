import os
import sklearn.impute
import wx
import webbrowser
import pandas as pd
import child_app.ModelingFrame

class DataProcessFrame(wx.Frame):
    def __init__(self, parent, title, data_path):
        super(DataProcessFrame, self).__init__(parent, title=title, size=(818, 400))

        self.data = pd.read_csv(data_path)
        self.html_path = 'E:\CODE-Codespace\Pycharm\Data-Processing-App-main\html_file'
        self.create_menu()
        self.create_widgets()
        self.display()

        self.AppConfig()

    def create_menu(self):
        pass

    def create_widgets(self):
        panel = wx.Panel(self)

        columns = wx.StaticText(panel, style=wx.BORDER_SUNKEN | wx.ALIGN_CENTER, label="Columns")
        heads = wx.StaticText(panel, style=wx.BORDER_SUNKEN | wx.ALIGN_CENTER, label="Data Head")
        null = wx.StaticText(panel, style=wx.BORDER_SUNKEN | wx.ALIGN_CENTER, label="Null Values")
        dtype = wx.StaticText(panel, style=wx.BORDER_SUNKEN | wx.ALIGN_CENTER, label="Dtypes")

        header = wx.BoxSizer(wx.HORIZONTAL)
        header.Add(columns, proportion=1, flag=wx.ALL | wx.ALIGN_BOTTOM)
        header.Add(heads, proportion=5, flag=wx.ALL | wx.ALIGN_BOTTOM)
        header.Add(null, proportion=1, flag=wx.ALL | wx.ALIGN_BOTTOM)
        header.Add(dtype, proportion=1, flag=wx.ALL | wx.ALIGN_BOTTOM)

        self.listbox = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_NO_HEADER)
        self.listbox.InsertColumn(0, 'Columns')
        self.listbox.InsertColumn(1, 'Head LB 1')
        self.listbox.InsertColumn(2, 'Head LB 2')
        self.listbox.InsertColumn(3, 'Head LB 3')
        self.listbox.InsertColumn(4, 'Head LB 4')
        self.listbox.InsertColumn(5, 'Head LB 5')
        self.listbox.InsertColumn(6, 'Null Values LB')
        self.listbox.InsertColumn(7, 'Dtypes LB')

        delete_button = wx.Button(panel, label="Save CSV")
        drop_button = wx.Button(panel, label="Drop")
        info_button = wx.Button(panel, label="Data Info")
        change_type_button = wx.Button(panel, label="Change Type")
        null_button = wx.Button(panel, label="Process Null")
        modeling_button = wx.Button(panel, label="Modeling")

        delete_button.Bind(wx.EVT_BUTTON, self.save_button)
        drop_button.Bind(wx.EVT_BUTTON, self.drop_button)
        info_button.Bind(wx.EVT_BUTTON, self.info_button)
        change_type_button.Bind(wx.EVT_BUTTON, self.change_type_button)
        null_button.Bind(wx.EVT_BUTTON, self.null_button)
        modeling_button.Bind(wx.EVT_BUTTON, self.modeling_button)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(delete_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(drop_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(info_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(change_type_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(null_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(modeling_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(header, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        sizer.Add(self.listbox, proportion=4, flag=wx.EXPAND | wx.ALL, border=0)
        sizer.Add(button_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

    def display(self):
        self.update_display()

    def update_display(self):
        self.listbox.DeleteAllItems()

        self.data_info = {
            'columns': self.data.columns.values.tolist(),
            'heads': self.data.head().to_dict(orient='list'),
            'dtypes': self.data.dtypes.apply(lambda x: x.name).to_dict(),
            'null_values': self.data.isnull().sum().to_dict(),
        }

        columns = self.data_info['columns']
        heads = self.data_info['heads']
        null_vals = self.data_info['null_values']
        dtypes = self.data_info['dtypes']

        items = []
        for i in range(len(columns)):
            column = str(columns[i])
            row = [column]
            row.extend([str(i) for i in heads[column]])
            row.extend([str(null_vals[column]), str(dtypes[column])])
            items.append(tuple(row))

        for item in items:
            index = self.listbox.InsertItem(self.listbox.GetItemCount(), item[0])
            for col, value in enumerate(item[1:], 1):
                self.listbox.SetItem(index, col, value)

    def save_button(self, event):
        with wx.FileDialog(self, "Chọn thư mục và tên file", wildcard="All files (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                chosen_path = dlg.GetPath()
                if not chosen_path.endswith(".csv"):  # Kiểm tra xem tệp có phần mở rộng không
                    chosen_path += ".csv"  # Nếu không có, thêm ".csv"
                print("Đường dẫn và tên file được chọn:", chosen_path)
                self.data.to_csv(chosen_path, index=False)

    def drop_button(self, event):
        selected_index = self.listbox.GetFirstSelected()
        column_name = self.listbox.GetItemText(selected_index, 0)
        self.data = self.data.drop(columns=[column_name])

        self.update_display()

    def info_button(self, event):
        files = os.listdir(self.html_path)
        try:
            html_file_path = os.path.join(self.html_path, files[0])
            webbrowser.open('file://' + html_file_path)
        except:
            print('Error !!!')

    def change_type_button(self, event):
        selected_index = self.listbox.GetFirstSelected()
        column_name = self.listbox.GetItemText(selected_index, 0)

        choices = ["int32", "int64", 'float32', "float64", "object", "datetime64", "category", "timedelta64"]

        dialog = ChoiceDialog(self, choices, 'Lua Chon')

        if dialog.ShowModal() == wx.ID_OK:
            selected_choice = dialog.get_selection()
            print("Bạn đã chọn:", selected_choice)

        dialog.Destroy()

        try:
            self.data[column_name] = self.data[column_name].astype(selected_choice)
        except Exception as e:
            wx.MessageBox( str(e), "Tiêu đề cảnh báo", wx.OK | wx.ICON_WARNING)

        self.update_display()



    def null_button(self, event):
        data_shape = self.data.shape

        selected_index = self.listbox.GetFirstSelected()
        column_name = self.listbox.GetItemText(selected_index, 0)

        count_null = self.data_info['null_values'][column_name]

        null_weight = (count_null / data_shape[0])*100

        if null_weight == 0:
            wx.MessageBox('Column not have Null Values', '', wx.ICON_WARNING)
        elif null_weight <= 10:
            self.data = self.data.dropna(subset= column_name)
            wx.MessageBox('Done !!', '', wx.ICON_WARNING)
        else:
            try:
                imputer = sklearn.impute.SimpleImputer(strategy='median')
                self.data[column_name] = imputer.fit(self.data[column_name])
                wx.MessageBox('Done !!', '', wx.ICON_WARNING)
            except Exception as e:
                wx.MessageBox(str(e), '', wx.ICON_WARNING)

        self.update_display()

    def modeling_button(self, event):
        self.Close()
        modelingframe = child_app.ModelingFrame.ModellingFrame(None, '', self.data)
        modelingframe.Show()

    def on_close(self, event):
        if self.html_path:
            files = os.listdir(self.html_path)
            for i in files:
                path = os.path.join(self.html_path, i)
                os.remove(path)
        self.Close()

    def AppConfig(self):
        # Tắt điều chỉnh cửa sổ
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

        # Ngăn thay đổi kích thước cột trong listbox
        for i in range(8):
            self.listbox.SetColumnWidth(i, 100)

        self.Bind(wx.EVT_WINDOW_DESTROY, self.on_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

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

