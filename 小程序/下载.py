import pandas as pd
import requests
from pathlib import Path

# 提示用户输入Excel文件路径
excel_path = input('请输入Excel文件的完整路径：').strip('\'"')

# 尝试读取Excel文件
try:
    df = pd.read_excel(excel_path)
except Exception as e:
    print(f"读取Excel文件失败：{str(e)}")
    exit()

# 桌面上的“导出”文件夹路径
export_folder_path = Path.home() / 'Desktop' / '导出'

# 确保导出文件夹存在
export_folder_path.mkdir(parents=True, exist_ok=True)

# 遍历DataFrame中的第一列中的每个URL
for url in df.iloc[:, 0]:  # iloc[:, 0] 表示选取第一列的所有行
    try:
        # 下载URL内容
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 获取文件名
            filename = url.split('/')[-1]
            # 确保文件名是有效的
            filename = filename if filename else f'file_{df.index(df[url])}'
            # 完整的导出路径
            file_path = export_folder_path / filename
            # 保存内容到文件
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"下载成功并保存到：{file_path}")
        else:
            print(f"下载失败：{url}")
    except Exception as e:
        print(f"下载异常：{url}，错误：{str(e)}")

