# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:56:36 2020

@author: Kasbah
"""

import numpy as np
import os
import statistics as st
import matplotlib.pyplot as plt

path = r'D:\3_PROCESSAT\3_PROCESSAT_4D_2019'
mean_prec = np.empty((6,0))

folders = os.listdir(path)
for folder in folders:
    if folder[18:35] == 'Alhambra_4D':        
        files = os.listdir(path + '/' + folder + '/1_process_files/1_markers_GCP') 
        for file in files: 
            if file[0:7] == 'markers':
                pt_prec = np.loadtxt(path + '/' + folder + '/1_process_files/1_markers_GCP/' + file)
                date=np.array([[int(file[12:29]),int(file[12:29])]])
                pt_prec = np.append(pt_prec, date, axis=0)
                mean_prec = np.append(mean_prec, pt_prec, axis=1)
                
                
plt.plot(mean_prec[1])

array_has_nan = np. isnan(mean_prec)
print(array_has_nan)

trues = np.argwhere(array_has_nan==True)



