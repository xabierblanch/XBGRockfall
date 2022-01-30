# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:58:14 2020

@author: XBG
"""

import ctypes  # An included library with Python install.
import fnmatch
import os
import shutil


#%% FIND IMAGES WITH SAME NUMERATION

def find_all(date,path,project_path):                     
    pattern = '*' + date + '*' 
    files = os.listdir(path) 
    for file in files: 
        if fnmatch.fnmatch(file, pattern):           
            file_path = project_path + "/3_data/" + path[len(path)-17:len(path)] + "/"
            directory = os.path.dirname(file_path)
            try:
                os.stat(directory)
            except:
                os.mkdir(directory)           
            shutil.copy(path + "\\" + file, project_path + "/3_data/" + path[len(path)-17:len(path)])          


#%% NUMBER COUNTER FOR EVERY IMAGE FOLDER
            
def check_number(project_path):
    paths_check=os.listdir(project_path + "/3_data/")
    num_img=[]
    for folder in paths_check:
        num_img.append(len(os.listdir(project_path + "/3_data/" + folder)))
    
    if len(set(num_img)) == 1:
        print("There are the same number of images in every folder")
        option=1
    else:
        option=ctypes.windll.user32.MessageBoxW(0, "ATTENTION! THE NUMBER OF IMAGES IS NOT CONSISTENT", "WARNING", 1)
    return option