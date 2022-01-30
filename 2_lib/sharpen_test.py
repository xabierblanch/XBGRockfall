# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:41:14 2020

@author: XBG
"""

# Sharpen/Blur detection with OpenCV (tested using 4.2.0) inspired by Adrian Rosebrock
# (https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/)
# 100 is a good threshold to filter foggy/rainy days

#%% IMPORT FUNCTIONS AND INITIALIZATION

import cv2
import os
import shutil

#%% MAIN FUNCTION

def blur_detection(project_path):
# loop over the input images  
    list_images = project_path + "/3_data"
    fm=[]
    
    for path in os.listdir(list_images):
        for imagePath in os.listdir(list_images + "\\" + path):
            image = cv2.imread(list_images + "\\" + path+"\\"+imagePath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            value = cv2.Laplacian(gray, cv2.CV_64F).var()
            print("Quality estimation for {} is {}".format(imagePath,value))
            fm.append(value)
            if value < 100:
                directory = os.path.dirname(list_images + "\\unusable_images\\")
                try:
                    os.stat(directory)
                except:
                    os.mkdir(directory)  
                shutil.move(list_images + "\\" + path+"\\"+imagePath, directory + "\\" + imagePath)