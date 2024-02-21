import os
import pandas as pd
from ydata_profiling import ProfileReport
import webbrowser


def data_report(file_path, directory):
    file_name = file_path.split('\\')[-1].split('.')[-2]
    data = pd.read_csv(file_path)
    profile = ProfileReport(data, title="Report", explorative=True)
    profile.to_file(f'{directory}\{file_name}.html')


def data_type(file_path):
    return os.path.splitext(os.path.basename(file_path))[1]

