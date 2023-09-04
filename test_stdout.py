#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os

def generate_and_save_data(dest_path):
    # 生成一些示例数据
    data = """This is some example data that we want to save as a file.
    You can replace this with your own data."""

    try:
        # 创建目标目录（如果不存在）
        os.makedirs(dest_path, exist_ok=True)

        # 构建目标文件的完整路径
        dest_file = os.path.join(dest_path, "output.txt")

        # 打开目标文件并写入数据
        with open(dest_file, 'w') as file:
            file.write(data)

        print(f"成功将数据保存到文件 '{dest_file}'")
    except Exception as e:
        print(f"保存文件时发生错误: {e}")

if __name__ == "__main__":
    # 定义目标路径
    destination_path = ".."  # 将此处的路径替换为你要保存文件的目标文件夹路径

    # 调用函数生成并保存数据
    generate_and_save_data(destination_path)

