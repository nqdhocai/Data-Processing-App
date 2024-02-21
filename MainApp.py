import os
import shutil
import wx
import wx.lib.newevent
from child_app.data_process_app_func import data_report
from child_app import ChildApp
from threading import Thread

# Sự kiện tạo ra để xử lý việc chọn tệp
FileSelectedEvent, EVT_FILE_SELECTED = wx.lib.newevent.NewEvent()


class MyApp(wx.App):
    def OnInit(self):
        main_frame = MainFrame(None, title="Ứng dụng wxPython")
        self.SetTopWindow(main_frame)
        main_frame.Show(True)
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 400))

        self.data_directory = './saved_file'
        self.html_directory = './html_file'
        self.create_menu()
        self.create_widgets()

        self.AppConfig()

    def create_menu(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)

    def create_widgets(self):
        panel = wx.Panel(self)

        # Tạo danh sách
        self.file_listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.update_listbox()

        # Sự kiện khi chọn tệp
        self.Bind(wx.EVT_LISTBOX, self.on_select, self.file_listbox)

        # Tạo các nút
        input_button = wx.Button(panel, label="Input file")
        delete_button = wx.Button(panel, label="Delete")
        select_button = wx.Button(panel, label="Select")

        input_button.Bind(wx.EVT_BUTTON, self.input_file)
        delete_button.Bind(wx.EVT_BUTTON, self.delete_file)
        select_button.Bind(wx.EVT_BUTTON, self.select_button)

        # Bố cục nút
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(input_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=20)
        button_sizer.Add(delete_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=20)
        button_sizer.Add(select_button, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=20)

        # Bố cục chung
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.file_listbox, proportion=5, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(button_sizer, proportion=1, flag=wx.EXPAND | wx.ALL)

        panel.SetSizer(sizer)

    def update_listbox(self):
        self.file_listbox.Clear()
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        files = os.listdir(self.data_directory)
        for file in files:
            self.file_listbox.Append(file)

    def on_select(self, event):
        selected_items = self.file_listbox.GetSelections()
        max_selected = 1
        if len(selected_items) > max_selected:
            last_selected_item = selected_items[-1]
            self.file_listbox.Deselect(last_selected_item)

    def input_file(self, event):
        # Chọn tệp để sao chép
        with wx.FileDialog(self, "Choose files to copy", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            file_paths = fileDialog.GetPaths()

        # Chọn thư mục để lưu bản sao
        destination_folder = self.data_directory
        if destination_folder:
            for file_path in file_paths:
                # Lấy tên tệp từ đường dẫn đầy đủ
                file_name = os.path.basename(file_path)
                # Tạo đường dẫn cho bản sao
                destination_path = os.path.join(destination_folder, file_name)

                # Sao chép tệp vào thư mục đích
                shutil.copy(file_path, destination_path)
            self.update_listbox()

    def delete_file(self, event):
        selection = self.file_listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.file_listbox.GetString(selection)
            file_path = os.path.join(self.data_directory, file_name)
            os.remove(file_path)
            self.file_listbox.Delete(selection)

    def select_button(self, event):
        self.Close()

        selection = self.file_listbox.GetSelection()
        if selection != wx.NOT_FOUND:
            file_name = self.file_listbox.GetString(selection)
            file_path = os.path.join(self.data_directory, file_name)

        data_processing_frame = ChildApp.DataProcessFrame(None, '', file_path)
        data_processing_frame.Show()

        if not os.path.exists(self.html_directory):
            os.makedirs(self.html_directory)
        def make_report():
            data_report(file_path, self.html_directory)
        thread = Thread(target=make_report)
        thread.start()

    def AppConfig(self):
        # Tắt điều chỉnh cửa sổ
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
