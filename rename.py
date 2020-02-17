# 该程序为更改目录程序
import os
import sys

file_list = os.listdir('./downloads')
# 进程当前工作目录
current_path = os.getcwd()
# 更改进程工作目录
os.chdir(r"./downloads")
old_name = "女朋友、借我一下"
new_name = "租借女友"
# 遍历文件夹
for file_name in file_list:
    os.rename(file_name, file_name.replace(old_name, new_name))
# 改回当前工作目录
os.chdir(current_path)
# 刷新
sys.stdin.flush()
print('done')
