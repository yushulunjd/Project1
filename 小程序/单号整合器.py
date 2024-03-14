import os
import pandas as pd
import glob

folder_path = input("请输入Excel文件所在的文件夹路径: ")
output_path = os.path.expanduser('~/Desktop/merged_excel.xlsx')

all_data = []

# 打印文件夹中找到的所有Excel文件
print(f"在文件夹 {folder_path} 中找到的Excel文件：")
for file in glob.glob(os.path.join(folder_path, "*.xlsx")):
    print(file)
    df = pd.read_excel(file)
    all_data.append(df)

    print("成功读取Excel文件，准备合并。")
    merged_data = pd.concat(all_data, ignore_index=True)
    merged_data.to_excel(output_path, index=False)
    print(f"所有文件已合并，合并后的文件已保存到 {output_path}")