import os
import sys
import subprocess

path = "C:/Users/User/Desktop/uhasselt/Basic Networc Security/code/remove self/dir"
dir_list = os.listdir(path)

print(sys.argv[0])

for file in dir_list:
    os.remove(path + "/" + file)
os.removedirs(path)