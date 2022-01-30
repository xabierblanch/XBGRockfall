# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 12:56:36 2020

@author: Kasbah
"""

import numpy as np
import os
import statistics as st
import matplotlib.pyplot as plt
import datetime

path = r'X:\3_PROCESSAT\11_HRCam_4D_2020'
mean_prec = np.empty((3,0))
all_date = np.empty([0])

folders = os.listdir(path)
for folder in folders:
    if folder[len(folders[1])-8:len(folders[1])] == 'HRCam_4D':        
        files = os.listdir(path + '/' + folder + '/2_results') 
        for file in files: 
            if file == 'HRCam_4D_pt_prec.txt':
                pt_prec = np.loadtxt(path + '/' + folder + '/2_results/' + file, skiprows=1)
                mean_x = st.median(pt_prec[:,3])
                mean_y = st.median(pt_prec[:,4])
                mean_z = st.median(pt_prec[:,5])
                date = (folder[9:17])
                mean_prec = np.append(mean_prec, ([mean_x],[mean_y],[mean_z]), axis=1)
                all_date = np.append(all_date, date)

date_format = np.empty([0])
for date in all_date:   
    date_format = np.append(date_format, datetime.datetime.strptime(date, '%Y%m%d'))


plt.plot(date_format, mean_prec[0], date_format,mean_prec[1],date_format,mean_prec[2])
plt.ylabel('some numbers')

plt.style.use('seaborn')
plt.plot(date_format,mean_prec[1],'o',date_format,mean_prec[1],'--')
plt.title('Precision estimation by Mike James (2020)')
plt.ylabel('sY (mm)')
plt.xlabel('Date')
