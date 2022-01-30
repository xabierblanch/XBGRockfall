# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:24:09 2020

@author: XBG
"""
import os
import statistics
import numpy as np

from sklearn.neighbors import NearestNeighbors

dirpath=r'X:\3_PROCESSAT\7_HRCam_test_4D'

paths=[dirpath + '/4_TEST_DATA/HRCam1_Puigcercos',dirpath + '/4_TEST_DATA/HRCam2_Puigcercos',dirpath + '/4_TEST_DATA/HRCam3_Puigcercos',dirpath + '/4_TEST_DATA/HRCam4_Puigcercos',dirpath + '/4_TEST_DATA/HRCam5_Puigcercos']

files = [os.listdir(paths[0]),os.listdir(paths[1]),os.listdir(paths[2]),os.listdir(paths[3]),os.listdir(paths[4])]
subfolders = [ f.path for f in os.scandir(r'X:\3_PROCESSAT\7_HRCam_test_4D') if f.is_dir() ]


dates = []
for i in range (len(files[1])):
    dates.append(files[1][i][7:15])  

dates = list(dict.fromkeys(dates))
                
for i in range (1,len(dates)-3):
       
    for test in subfolders:
        if len(test)==62:
            if test[31:48]==dates[i] + '_' + dates[i+1]:
                print('Validant els despreniments del fitxer :' + dates[i] + '_' + dates[i+1])               
                rockfall_conf = np.array([['x','y','z','diff','label','volum','median_diff','value','distance_1','distance_2','confidence']])                   
                try:
                    rockfall_previous = np.loadtxt(r'X:\3_PROCESSAT\7_HRCam_test_4D/' + dates[i-1] + '_' + dates[i+2] + r"_HRCam_4D_test/2_results/3_Rockfalls/" + dates[i-1] + '_' + dates[i+2] + "_total.xyz")                                                 
                    rockfall_previous_centroids = np.empty((0, 3)) 
                      
                    for j in range (0, int(max(rockfall_previous[:,4]))+1):
                        ky=np.argwhere(rockfall_previous[:,4]==j)
                                                                                             
                        if len(ky) > 0:
                            meanx = float(statistics.median(rockfall_previous[ky,0]))
                            meany = float(statistics.median(rockfall_previous[ky,1]))
                            meanz = float(statistics.median(rockfall_previous[ky,2]))                          
                            rockfall_previous_centroids = np.append(rockfall_previous_centroids, [(meanx, meany, meanz)], axis=0)
                            rockfall_previous_centroids= np.delete(rockfall_previous_centroids,np.where(~rockfall_previous_centroids.any(axis=1))[0], axis=0)                 
                    
                except:
                    print('file: ' + dates[i-1] + '_' + dates[i+2] + "_total.xyz not found!")           
                    
                try:
                    rockfall_next = np.loadtxt(r'X:\3_PROCESSAT\7_HRCam_test_4D/' + dates[i] + '_' + dates[i+3] + r"_HRCam_4D_test/2_results/3_Rockfalls/" + dates[i] + '_' + dates[i+3] + "_total.xyz")                                                  
                    rockfall_next_centroids = np.empty((0, 3))
                    
                    for j in range (0, int(max(rockfall_next[:,4]))+1):
                        ky=np.argwhere(rockfall_next[:,4]==j)
                                                                                             
                        if len(ky) > 0:                         
                            meanx = float(statistics.median(rockfall_next[ky,0]))
                            meany = float(statistics.median(rockfall_next[ky,1]))
                            meanz = float(statistics.median(rockfall_next[ky,2]))                          
                            rockfall_next_centroids = np.append(rockfall_next_centroids, [(meanx, meany, meanz)], axis=0)
                            rockfall_next_centroids= np.delete(rockfall_next_centroids,np.where(~rockfall_next_centroids.any(axis=1))[0], axis=0)                                                       
                    
                except:
                    print('file: ' + dates[i] + '_' + dates[i+3] + "_total.xyz not found!")                        
                
                if os.path.getsize(test + r"/2_results/3_Rockfalls/" + dates[i] + '_' + dates[i+1] + "_total.xyz") > 0:
                    rockfall = np.loadtxt(test + r"/2_results/3_Rockfalls/" + dates[i] + '_' + dates[i+1] + "_total.xyz")
                    
                    for j in range (0, int(max(rockfall[:,7])+1)):
                        ky=np.argwhere(rockfall[:,4]==j)
                                                                       
                        x=rockfall[ky,0]
                        y=rockfall[ky,1]
                        z=rockfall[ky,2]
                        diff=rockfall[ky,3]
                        label=rockfall[ky,4]
                        volum=rockfall[ky,5] 
                        median_diff=rockfall[ky,14]
                        value=rockfall[ky,15]
                        
                        if len(x) > 0:
                            meanx = float(statistics.median(x))
                            meany = float(statistics.median(y))
                            meanz = float(statistics.median(z))
                            rockfall_value = max(value)
                            
                            if rockfall_value == 1 and len(rockfall_previous_centroids) > 0 and len(rockfall_next_centroids) > 0:
                                rockfall_centroid = meanx,meany,meanz
                                rockfall_previous_centroids_check = np.append(rockfall_previous_centroids, [(meanx, meany, meanz)], axis=0)
                                rockfall_next_centroids_check = np.append(rockfall_next_centroids, [(meanx, meany, meanz)], axis=0)
                                
                                nbrs_previous = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(rockfall_previous_centroids_check[:,[0,2]])
                                distances_previous, indices_previous = nbrs_previous.kneighbors(rockfall_previous_centroids_check[:,[0,2]])
                                
                                nbrs_next = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(rockfall_next_centroids_check[:,[0,2]])
                                distances_next, indices_next = nbrs_next.kneighbors(rockfall_next_centroids_check[:,[0,2]])
                                
                                if distances_previous[len(distances_previous)-1,1] < 0.05 or distances_next[len(distances_next)-1,1] < 0.05:                                   
                                    confidence=1
                                    if distances_previous[len(distances_previous)-1,1] < 0.05 and distances_next[len(distances_next)-1,1] < 0.05:
                                        confidence=2   
                                    print("Despreniment número " + str(j) + " confirmat")  
                                    for point in range(len(x)):
                                        rockfall_conf = np.append(rockfall_conf, [(x[point][0], y[point][0], z[point][0], diff[point][0], label[point][0], volum[point][0], median_diff[point][0], value[point][0], distances_previous[len(distances_previous)-1,1], distances_next[len(distances_next)-1,1],confidence)], axis=0)
             
                path_file_1 = r'X:\3_PROCESSAT\7_HRCam_test_4D/' + dates[i] + '_' + dates[i+1] + r"_HRCam_4D_test/2_results/3_Rockfalls/" + dates[i] + '_' + dates[i+1]
                rockfall_conf = np.delete(rockfall_conf, (0), axis=0)
                rockfall_conf = rockfall_conf.astype(float)
                np.savetxt(path_file_1 + '_confirmed.xyz', rockfall_conf, fmt='%10.5f')
                    
                    
