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
            if file[len(file)-20:len(file)] == 'HRCam_4D_pt_prec.txt':
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


precipitacio = np.loadtxt(r'X:\3_PROCESSAT\11_HRCam_4D_2020\Meteoblue_precipitacio.txt')

date_format2 = np.empty([0])
for date2 in precipitacio[:,0]:   
    date_format2 = np.append(date_format2, datetime.datetime.strptime(str(date2), '%Y%m%d.0'))


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(date_format, mean_prec[1],color='orange')
plt.ylabel("Estimate Precision [mm]")

ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
ax2.bar(date_format2, precipitacio[:,1], align='center', alpha=0.5)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
ax2.grid(False)
plt.ylabel("Rainfall [mm/day]")

ax1.set_title('Estimate Precision vs Rainfall (2 months)')
