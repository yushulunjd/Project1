# split_excel.py
import pandas as pd
import os

def clean_path(path):
    path = path.strip().strip('\'"')
    return r'{}'.format(path)

def create_export_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 {folder_path} 已创建。")

def split_excel(file_path, rows_per_file, export_folder):
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请确保文件路径正确。")
        return
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return

    total_rows = df.shape[0]
    num_files = total_rows // rows_per_file + (1 if total_rows % rows_per_file else 0)

    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = start_row + rows_per_file
        df_subset = df.iloc[start_row:end_row]

        output_file = os.path.join(export_folder, f'exported_{i+1}.xlsx')
        df_subset.to_excel(output_file, index=False)

        print(f"文件 {output_file} 已生成。")

if __name__ == "__main__":
    original_file = input("请输入原始Excel文件的完整路径: ")
    original_file = clean_path(original_file)

    rows = 1020

    # 直接设置导出文件夹为桌面上的"导出"文件夹
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    export_dir = os.path.join(desktop, '导出')

    create_export_folder(export_dir)
    split_excel(original_file, rows, export_dir)
