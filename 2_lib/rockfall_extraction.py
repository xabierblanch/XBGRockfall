# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 23:52:44 2020

@author: XBG
"""

#%% DBSCAN ROCKFALL EXTRACTION

# def dbscan(path_M3C2_file, eps1, min_samples1, project_path):   
    
from sklearn.cluster import DBSCAN
import numpy as np
import statistics
from scipy.spatial import Delaunay
import scipy.spatial as ss                  
# import matplotlib.pyplot as plt
import os
import pandas as pd

subfolders = [ f.path for f in os.scandir(r'X:\3_PROCESSAT\11_HRCam_4D_2020') if f.is_dir() ]
    
for test in subfolders:
    if len(test)==58:
        # test = r'X:\3_PROCESSAT\7_HRCam_test_4D\20200109_20200112_HRCam_4D_test'

        path_M3C2_file= test + r"\2_results\2_M3C2\\" + test[32:49] + '.xyz'      
        project_path=test
        
        try:
            os.mkdir(project_path + "/2_results/3_Rockfalls")
        except:
            print("La carpeta ja existeix")
            
        print("Loading M3C2 Point Cloud -> " + test[32:49])
        m3c2_pc = np.loadtxt(path_M3C2_file)
        
        print("NaN and minimum difference filter")    
        isnan = np.isnan(m3c2_pc)   
        m3c2 = np.delete(m3c2_pc, np.argwhere(isnan == 1),0)   
        m3c2 = np.delete(m3c2, np.argwhere(m3c2[:,5] < 0.04),0)
        
        ## DBSCAN 
        print("DBSCAN process started")
        x=np.array([m3c2[:,0],m3c2[:,1],m3c2[:,2]])
        X=x.transpose()
        
        db = DBSCAN(eps=0.06, min_samples=70).fit(X)
        #db = DBSCAN(eps, min_samples).fit(X)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        
        m3c2 = np.delete(m3c2, np.argwhere(labels == -1),0)
        labels = np.delete(labels, np.argwhere(labels == -1),0)
        
        rockfalls=np.vstack([m3c2[:,0],m3c2[:,1],m3c2[:,2],m3c2[:,5],m3c2[:,6],m3c2[:,7],m3c2[:,8],labels])
        rockfalls=rockfalls.transpose()
        
        print("Saving rockfall list")
        path_file_1 = project_path + "/2_results/3_Rockfalls/" + path_M3C2_file[len(path_M3C2_file)-21:len(path_M3C2_file)-4]
        np.savetxt(path_file_1 + '_rockfalls.xyz', rockfalls, fmt='%10.4f') 
    else:
        print(len(test))
        
        
    # # %% VOLUME CALCULATION    
    
    #     volum = np.array([['Label','Volum','Area','Points','Density','AreaXZ','DensityXZ','Nx','Ny','Nz','Median Diff','Despreniment','precision_X','precision_Y','precision_Z']])
        
    #     path_prec_file= test + r'\2_results\HRCam_4D_test_pt_prec.txt'
    #     prec_file = np.loadtxt(path_prec_file,skiprows =1)
        
    #     for j in range (0, int(max(rockfalls[:,7])+1)):
            
    #         ky=np.argwhere(rockfalls[:,7]==j)    
    #         x=rockfalls[ky,0];
    #         y=rockfalls[ky,1];
    #         diff=rockfalls[ky,1]-rockfalls[ky,3];
    #         z=rockfalls[ky,2];
            
    #         meanx = statistics.stdev(rockfalls[rockfalls[:, 7] == j][:,4])
    #         meany = statistics.stdev(rockfalls[rockfalls[:, 7] == j][:,5])
    #         meanz = statistics.stdev(rockfalls[rockfalls[:, 7] == j][:,6])           
    #         mediandiff = statistics.median(rockfalls[ky,3])
                                      
    #         points=np.append(x,z, axis=1)
            
    #         rock_x = rockfalls[rockfalls[:, 7] == j][:,0]
    #         rock_z = rockfalls[rockfalls[:, 7] == j][:,2]
            
    #         heightXZ = max(rock_z)-min(rock_z)
    #         widthXZ = max(rock_x)-min(rock_x)
    #         areaXZ=heightXZ*widthXZ
    #         densitatXZ=len(points)/areaXZ
            
    #         #Rockfall Validation Precision
            
    #         maxX=max(rock_x)+0.15
    #         minX=min(rock_x)-0.15
    #         maxZ=max(rock_z)+0.15
    #         minZ=min(rock_z)-0.15
            
    #         nearest_point_X=prec_file[prec_file[:, 0]>minX][prec_file[prec_file[:, 0]>minX][:, 0]<maxX]          
    #         nearest_point = nearest_point_X[nearest_point_X[:, 2]>minZ][nearest_point_X[nearest_point_X[:, 2]>minZ][:, 2]<maxZ]
            
    #         try:
    #             median_precision_X = len(nearest_point[:,3])
    #         except:
    #               median_precision_X = 0
                 
    #         try:                 
    #             median_precision_Y = statistics.mean(nearest_point[:,3])*statistics.mean(nearest_point[:,4])*statistics.mean(nearest_point[:,5])
    #         except:
    #               median_precision_Y = 0
            
    #         try:
    #             median_precision_Z = statistics.median(nearest_point[:,3])*statistics.median(nearest_point[:,4])*statistics.median(nearest_point[:,5])
    #         except:
    #               median_precision_Z = 0
            
    #         if mediandiff > 0.04 and meany < 0.15 and areaXZ > 0.06 or areaXZ > 0.15 and mediandiff > 0.10:
    #         # if mediandiff > 0.03:
    #             try:
    #                 tri=Delaunay(points);
                    
    #                 # Separating small and large edges:
    #                 thresh = 0.1  # user defined threshold
    #                 small_edges = set()
    #                 large_edges = set()
                    
    #                 # vertexs = np.array([[[],[],[]]])
    #                 vertexs = []
                    
    #                 for tr in tri.simplices:
    #                     for i in range(3):
    #                         edge_idx0 = tr[i]
    #                         edge_idx1 = tr[(i+1)%3]
    #                         if (edge_idx1, edge_idx0) in small_edges:
    #                             continue  # already visited this edge from other side
    #                         if (edge_idx1, edge_idx0) in large_edges:
    #                             continue
    #                         p0 = points[edge_idx0]
    #                         p1 = points[edge_idx1]
    #                         if np.linalg.norm(p1 - p0) <  thresh:
    #                             small_edges.add((edge_idx0, edge_idx1))
    #                             # vertexs=np.append(vertexs,[[tr[0],tr[1],tr[2]]], axis=0)
    #                         else:
    #                             large_edges.add((edge_idx0, edge_idx1))
    #                             vertexs.append([tr[0],tr[1],tr[2]])
                                
    #                 bo = np.array(vertexs)
    #                 bo = np.unique(bo, axis=0)   
                          
    #                 conect=tri.vertices;
                            
    #                 vol_total=0;
    #                 area_total=0;
                    
    #                 delete_lines=[]
    #                 for h in range(0,len(bo)):
    #                     for l in range(0,len(conect)):
    #                         if np.all(bo[h]==conect[l]) == True:                    
    #                             delete_lines.append(l)
                               
    #                 conect=np.delete(conect,delete_lines,0)               
                                             
    #                 for k in range(0,len(conect)):            
    #                     #PUNTS QUE FORMEN LES TRIANGULACIONS VALIDES
    #                     x_point=np.array([x[conect[k,0]],x[conect[k,1]],x[conect[k,2]],x[conect[k,0]],x[conect[k,1]],x[conect[k,2]]])
    #                     z_point=np.array([z[conect[k,0]],z[conect[k,1]],z[conect[k,2]],z[conect[k,0]],z[conect[k,1]],z[conect[k,2]]])
    #                     y_point=np.array([y[conect[k,0]],y[conect[k,1]],y[conect[k,2]],diff[conect[k,0]],diff[conect[k,1]],diff[conect[k,2]]])
    #                     result=np.append(x_point,z_point,axis=1)
    #                     result=np.append(result, y_point, axis=1)
    #                     #CALCUL DEL VOLUM 3D
    #                     hull = ss.ConvexHull(result)
    #                     vol=hull.volume
    #                     vol_total=vol_total+vol
    #                     #CALCUL ÀREA 2D EN L'EIX Y
    #                     y_list = [result[0][1], result[1][1], result[2][1]]
    #                     x_list = [result[0][0], result[1][0], result[2][0]]
    #                     height = max(y_list) - min(y_list)
    #                     width = max(x_list) - min(x_list)
    #                     area = height * width / 2        
    #                     area_total=area_total+area
                                 
    #                 density = len(points)/area_total            
                    
    #                 if vol_total > 0.002 and mediandiff > 0.04 and meany < 0.15 and areaXZ > 0.05 or areaXZ > 0.25 and vol_total > 0.02: 
    #                     despreniment = 1
    #                 else:
    #                     despreniment = 0
    #                 volum = np.append(volum,[[j,vol_total,area_total,len(points),density,areaXZ,densitatXZ,meanx,meany,meanz,mediandiff,despreniment,median_precision_X,median_precision_Y,median_precision_Z]], axis=0)
    #                 print("Rockfall triangulated. Number of points: " + str(len(points)) + " XZ Density: " + str(densitatXZ) + " Median Diff: " + str(mediandiff[0]))
                    
    #             except:
    #                 print("Rockfall not triangulated. Number of points: " + str(len(points)) + " XZ Density: " + str(densitatXZ) + " Median Diff: " + str(mediandiff[0]))
                                                                
    #     np.savetxt(path_file_1 + '_volumes.xyz', volum, delimiter="\t", fmt='%s')                        
                    
    #     # TOTAL ROCKFALL FILE
    #     try:
    #         rockfall_dataset = pd.DataFrame({'X': rockfalls[:, 0], 'Y': rockfalls[:, 1],'Z': rockfalls[:, 2], 'DIFF': rockfalls[:, 3],'id': rockfalls[:, 7]})              
    #         volume_dataset = pd.DataFrame({'id': volum[:, 0], 'Volum': volum[:, 1],'Area': volum[:, 2], 'Points': volum[:, 3],'Density': volum[:, 4],'areaXZ': volum[:, 5],'densitatXZ': volum[:, 6],'Nx': volum[:, 7],'Ny': volum[:, 8],'Nz': volum[:, 9],'Median Diff': volum[:, 10] ,'Rockfall': volum[:, 11],'precision_X': volum[:, 12],'precision_Y': volum[:, 13] ,'precision_Z': volum[:, 14]})                      
    #         volume_dataset=volume_dataset.drop(0)
    #         volume_dataset = volume_dataset.astype(float)
    #         result = pd.merge(rockfall_dataset, volume_dataset, on='id')    
    #         np.savetxt(path_file_1 + '_total.xyz', result.values, fmt='%10.5f')
    #         print("File with all rockfalls information saved")                                                      
    #     except:
    #         print("The file with all rockfalls information could not be created")                                                      