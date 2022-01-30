# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 17:17:29 2020

@author: XBG
"""
#%% AGISOFT METASHAPE 1.6.1 (API Python3 1.6.1)

import Metashape
import sys
import time

#Set variables
project_path = sys.argv[1]
label = sys.argv[2]
doc = Metashape.app.document
doc.read_only = False
doc.open(project_path + "/1_process_files/3_metashape/" + label + ".psx")
doc.read_only = False
chunk_original = doc.chunk

chunk_original.resetRegion()
    
chunk_copy = chunk_original.copy()

# prepare log file
stdoutOrigin=sys.stdout 
sys.stdout = open(project_path + "/1_process_files/3_metashape/DenseCloud.log", "w")

#%% STEP 6 -> Enable/Disable Cameras
                 
for i in range(0, len(chunk_original.cameras)):
    name_1 = chunk_original.cameras[1].label[7:15]
    if chunk_original.cameras[i].label[7:15] != name_1:
        name_2 = chunk_original.cameras[i].label[7:15]

for i in range(0,len(chunk_original.cameras)):   
    if chunk_original.cameras[i].label[7:15] == name_1:
        chunk_original.cameras[i].enabled = False

chunk_original.label = name_2

for i in range(0,len(chunk_copy.cameras)):   
    if chunk_copy.cameras[i].label[7:15] == name_2:
        chunk_copy.cameras[i].enabled = False

chunk_copy.label = name_1    
        
#%% STEP 7 -> DenseCloud Generation

t0 = time.time()

for chunk in doc.chunks:
    chunk.resetRegion()
    chunk.buildDepthMaps(downscale=1, filter_mode=Metashape.AggressiveFiltering, reuse_depth=False, subdivide_task=True)
    chunk.buildDenseCloud(point_colors=True, point_confidence=True, keep_depth=True, subdivide_task=True)

#%% STEP 8.1 -> Confidence Filter

chunk.dense_cloud.setConfidenceFilter(0,4)
chunk.dense_cloud.removePoints(list(range(128)))
chunk.dense_cloud.resetFilters()

#%% STEP 8 -> Dense Clouds color filtering
        
for chunk in doc.chunks:       
    chunk.image_brightness = 150
    chunk.image_contrast = 1200
    dense_cloud = chunk.dense_cloud
    dense_cloud.selectPointsByColor(color=[0,0,0], tolerance=100, channels='RGBHSV')
    dense_cloud.removeSelectedPoints()
    
     #%% STEP 9 -> Export Dense Clouds
        
export_path = project_path + '/2_results/1_DensePointClouds/{chunklabel}.xyz'

#export_path = "X:/3_PROCESSAT/3_XBG_Process/20200131_1312_Despreniment_mur/2_results/DensePointClouds/{chunklabel}.xyz"

for chunk in doc.chunks:  
    chunk.exportPoints(export_path, source_data = Metashape.DenseCloudData, binary=True, save_normals=True, save_colors=True, save_confidence=True, colors_rgb_8bit=True, format=Metashape.PointsFormatXYZ)
    
doc.save(project_path + "/1_process_files/3_metashape/" + label + ".psx")

t1 = time.time()    
        
print('Total Time Dense Cloud process: ' +  str((t1-t0)/60) + ' minutes')

sys.stdout.close()
sys.stdout=stdoutOrigin
Metashape.app.quit()

Metashape.app.quit()