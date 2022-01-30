# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:35:25 2019

@author: XBG
"""

#%% AGISOFT METASHAPE 1.6.1 (API Python3 1.6.1)

import Metashape
import os
import sys
import numpy as np
import time
import math
import statistics

#Set variables
project_path = sys.argv[1]
label = sys.argv[2]
dirpath = sys.argv[3]

stdoutOrigin=sys.stdout 
sys.stdout = open(project_path + "/1_process_files/3_metashape/log_metashape.log", "w")

doc = Metashape.app.document
# doc.remove(doc.chunks[0])
doc.read_only = False
doc.save(project_path + "/1_process_files/3_metashape/" + label + ".psx")
doc.read_only = False

reprojection_rmse = 0
error_pix = 0

for y in range(2):
    
    if y == 0:
        doc.read_only = False
        doc.save(project_path + "/1_process_files/3_metashape/" + label + ".psx")
        doc.read_only = False
        doc.chunk = doc.chunk

    else:
        # chunk_copy = doc.chunk.copy()
        doc.remove(doc.chunk)
        chunk = Metashape.app.document.addChunk()
        doc.chunk.tiepoint_accuracy = reprojection_rmse
        doc.chunk.marker_projection_accuracy = error_pix
        
    Metashape.app.cpu_enable = True
    Metashape.app.gpu_mask = 1
    Metashape.app.update()
    
    #%%STEP0 -> Load images in camera groups
    
    path_master = project_path + "/3_data"
    
    sub_folders = os.listdir(path_master)
    for folder in sub_folders:
    	folder = os.path.join(path_master, folder)
    	if not os.path.isdir(folder):
    		continue
    
    	image_list = os.listdir(folder)
    	if len(image_list)>0:
    		print("Creating a new camera group")
    		photo_list = list()
    		new_group = doc.chunk.addCameraGroup()
    		new_group.label = os.path.basename(folder)
    		for photo in image_list:
    			if photo.rsplit(".",1)[1].lower() in  ["jpg", "jpeg", "tif", "tiff"]:
    				photo_list.append(os.path.join(folder, photo))
    		doc.chunk.addPhotos(photo_list)
    			   
    		for camera in doc.chunk.cameras:
    			if not camera.group:
    				camera.group = new_group
    	else: 		
    		print("Empty folder")
            
    for groups in doc.chunk.camera_groups:
    	  if groups.label == 'unusable_images':
    		  del_group = groups
    
    try:    
    	doc.chunk.remove(del_group)
    except:
    	print("")
    
    print("Image upload finished")
    
    #%% STEP 1 -> Calibration Camera Groups (Create as many groups as systems are installed)
                
    for camera in doc.chunk.cameras:   
        if camera.label[0:6] == "HRCam1":      
            sensor1 = doc.chunk.addSensor()
            sensor1.label = camera.label
            sensor1.type = camera.sensor.type
            sensor1.calibration = camera.sensor.calibration
            sensor1.width = camera.sensor.width
            sensor1.height = camera.sensor.height
            sensor1.focal_length = camera.sensor.focal_length
            sensor1.pixel_height = camera.sensor.pixel_height
            sensor1.pixel_width = camera.sensor.pixel_width
            camera.sensor = sensor1
        
        elif camera.label[0:6] == "HRCam2":
            sensor2 = doc.chunk.addSensor()
            sensor2.label = camera.label
            sensor2.type = camera.sensor.type
            sensor2.calibration = camera.sensor.calibration
            sensor2.width = camera.sensor.width
            sensor2.height = camera.sensor.height
            sensor2.focal_length = camera.sensor.focal_length
            sensor2.pixel_height = camera.sensor.pixel_height
            sensor2.pixel_width = camera.sensor.pixel_width
            camera.sensor = sensor2
            
        elif camera.label[0:6] == "HRCam3": 
            sensor3 = doc.chunk.addSensor()
            sensor3.label = camera.label
            sensor3.type = camera.sensor.type
            sensor3.calibration = camera.sensor.calibration
            sensor3.width = camera.sensor.width
            sensor3.height = camera.sensor.height
            sensor3.focal_length = camera.sensor.focal_length
            sensor3.pixel_height = camera.sensor.pixel_height
            sensor3.pixel_width = camera.sensor.pixel_width
            camera.sensor = sensor3
            
        elif camera.label[0:6] == "HRCam4": 
            sensor4 = doc.chunk.addSensor()
            sensor4.label = camera.label
            sensor4.type = camera.sensor.type
            sensor4.calibration = camera.sensor.calibration
            sensor4.width = camera.sensor.width
            sensor4.height = camera.sensor.height
            sensor4.focal_length = camera.sensor.focal_length
            sensor4.pixel_height = camera.sensor.pixel_height
            sensor4.pixel_width = camera.sensor.pixel_width
            camera.sensor = sensor4
            
        elif camera.label[0:6] == "HRCam5": 
            sensor5 = doc.chunk.addSensor()
            sensor5.label = camera.label
            sensor5.type = camera.sensor.type
            sensor5.calibration = camera.sensor.calibration
            sensor5.width = camera.sensor.width
            sensor5.height = camera.sensor.height
            sensor5.focal_length = camera.sensor.focal_length
            sensor5.pixel_height = camera.sensor.pixel_height
            sensor5.pixel_width = camera.sensor.pixel_width
            camera.sensor = sensor5
    
    for camera in doc.chunk.cameras:   
        if camera.label[0:6] == "HRCam1":
            camera.sensor = sensor1
        if camera.label[0:6] == "HRCam2":
            camera.sensor = sensor2
        if camera.label[0:6] == "HRCam3":
            camera.sensor = sensor3
        if camera.label[0:6] == "HRCam4":
            camera.sensor = sensor4
        if camera.label[0:6] == "HRCam5":
            camera.sensor = sensor5
    
    print("Calibration groups performed successfully")
    
    #%% STEP 2 -> Create and load masks
                
    pathToMasks =  project_path + '/1_process_files/2_masks/{filename}.JPG'    
            
    
    for f in doc.chunk.frames:
        try:
            f.importMasks(path=pathToMasks, source=Metashape.MaskSource.MaskSourceFile)
        except: 
            print("Error en la mascara")
            
    #%% STEP 3 -> Markers 
    
    marker1=doc.chunk.addMarker()
    marker2=doc.chunk.addMarker()
    marker3=doc.chunk.addMarker()
    marker4=doc.chunk.addMarker()
    marker5=doc.chunk.addMarker()
    # marker6=doc.chunk.addMarker()
    
    markers_reference=np.loadtxt(dirpath + '/3_reference/1_reference_GCP/reference_markers_LiDAR.txt', delimiter='\t')
    
    for marker in doc.chunk.markers:
         marker.reference.accuracy = [0.05,  0.05,   0.05] #Marker Accuracy [m]
    
    marker1.reference.location = [markers_reference[0,0], markers_reference[0,1], markers_reference[0,2]]
    marker2.reference.location = [markers_reference[1,0], markers_reference[1,1], markers_reference[1,2]]
    marker3.reference.location = [markers_reference[2,0], markers_reference[2,1], markers_reference[2,2]]
    marker4.reference.location = [markers_reference[3,0], markers_reference[3,1], markers_reference[3,2]]
    marker5.reference.location = [markers_reference[4,0], markers_reference[4,1], markers_reference[4,2]]
    # marker6.reference.location = [markers_reference[5,0], markers_reference[5,1], markers_reference[5,2]]
    
    for camera in doc.chunk.cameras:  
        markers_track=np.loadtxt(project_path + "/1_process_files/1_markers_GCP/markers_" + camera.label + ".JPG.txt")   
        for i in range(len(markers_track)):         
            new_marker=doc.chunk.markers[i]
            if markers_track[i,0] == markers_track[i,0] and markers_track[i,1] == markers_track[i,1]:
                new_marker.projections[camera] = Metashape.Marker.Projection(markers_track[i], True)
                #new_marker.projections[camera] = Metashape.Marker.Projection([0,0], False)           
            else:
                print("No marquer")
                
    doc.chunk.marker_location_accuracy=[0.05,0.05,0.05] #Measurement Accuracy - Marker Accuracy [m]
            
    print("Ground control points added correctly")

#%% STEP 4 -> Align and optimization Cameras (Loop inspired by Mike James 2017)
 
    Metashape.app.update()           
 
    t0 = time.time()
    print(t0)
    
    doc.chunk.matchPhotos(downscale=0, generic_preselection=False, reference_preselection=False, reference_preselection_mode="ReferencePreselectionSource", filter_mask=True, mask_tiepoints=False, keypoint_limit=0, tiepoint_limit=0, keep_keypoints=False, guided_matching=False, reset_matches=True, subdivide_task=True)
    
    doc.chunk.alignCameras()
    print("Camera aligment performed")
    
    #doc.save(project_path+"/3_metashape/"+label + ".psx")    
    
    t1 = time.time()    
    print(t1)
    
    print('Total Time aligment  : ' +  str(t1-t0) + 's')
    #Optimize Cameras
    
    doc.chunk.optimizeCameras(fit_f=True,fit_cx=True,fit_cy=True,fit_b1=True,fit_b2=True,fit_k1=True,fit_k2=True,fit_k3=True,fit_k4=False,fit_p1=True,fit_p2=True,fit_corrections=False,adaptive_fitting=False,tiepoint_covariance=False)
    
    #Update Transform
    doc.chunk.updateTransform()
    #doc.save(project_path + '/1_process_files/3_metashape/' + label + '.psx')     
    
#%% STEP 5 -> Compute RMS reprojection Error (AGISOFT FORUM)
    
    if y == 1:
        break
    
    else:
        point_cloud = doc.chunk.point_cloud
        points = point_cloud.points
        error, tie_points = [], []
        
        for camera in [cam for cam in doc.chunk.cameras if cam.transform]:
            point_index = 0
            photo_num = 0
            for proj in doc.chunk.point_cloud.projections[camera]:
                track_id = proj.track_id
                while point_index < len(points) and points[point_index].track_id < track_id:
                    point_index += 1
                if point_index < len(points) and points[point_index].track_id == track_id:
                    if not points[point_index].valid:
                        continue
        
                    dist = camera.error(points[point_index].coord, proj.coord).norm() ** 2
                    error.append(dist)
                    photo_num += 1
        
            tie_points.append(photo_num)
        
        reprojection_rmse = round(math.sqrt(sum(error) / len(error)), 2)
        reprojection_max = round(max(error) , 2)
        reprojection_std = round(statistics.stdev(error), 2)
        tie_points_per_image = round(sum(tie_points) / len(tie_points), 0)
        
        print("Average tie point residual error: " + str(reprojection_rmse))
        print("Maxtie point residual error: " + str(reprojection_max))
        print("Standard deviation for tie point residual error: " + str(reprojection_std))
        
    #%% STEP 6 -> Compute Markers error (AGISOFT FORUM)
        
        total_error = []
        
        for marker in doc.chunk.markers:
            diff, error = [],[]
            for camera in doc.chunk.cameras:
                try:
                    v_proj = marker.projections[camera].coord #2 dimensional vector of the marker projection on the photo
                    v_reproj = camera.project(marker.position) #2 dimensional vector of projected 3D marker position
                    error = (v_proj - v_reproj).norm() #reprojection error for current photo
                    diff.append(error)
                except:
                    print("No hi ha Marker identificat")
                    
            marker_error = round(sum(diff)/len(diff),2)
            total_error.append(marker_error)
        error_pix =  round(sum(total_error)/len(total_error),2)   
    
#%% STEP 7 -> Update accuracies and loop again aligment (Loop inspired by Mike James 2017)
    
        # doc.chunk.tiepoint_accuracy = reprojection_rmse
        # doc.chunk.marker_projection_accuracy = error_pix

#%% STEP 8 -> Point Filter (based on reprojection error)
    
threshold_reprojection = 0.7 #0.5 It's a good first approach
threshold_reconstruction = 16
threshold_projection = 5

f = Metashape.PointCloud.Filter()
f.init(doc.chunk, criterion = Metashape.PointCloud.Filter.ReprojectionError)
f.removePoints(threshold_reprojection)

f = Metashape.PointCloud.Filter()
f.init(doc.chunk, criterion = Metashape.PointCloud.Filter.ReconstructionUncertainty)
f.removePoints(threshold_reconstruction)

f = Metashape.PointCloud.Filter()
f.init(doc.chunk, criterion = Metashape.PointCloud.Filter.ProjectionAccuracy)
f.removePoints(threshold_projection)

#%% STEP 8 -> Cameras optimization after last loop iteration and point filter. Tie Point Covariance exported!

doc.chunk.optimizeCameras(fit_f=True,fit_cx=True,fit_cy=True,fit_b1=True,fit_b2=True,fit_k1=True,fit_k2=True,fit_k3=True,fit_k4=False,fit_p1=True,fit_p2=True,fit_corrections=False,adaptive_fitting=False,tiepoint_covariance=True)

#Update Transform
doc.chunk.updateTransform()
doc.save(project_path + '/1_process_files/3_metashape/' + label + '.psx')   

#%% CLOSE LOG FILE

sys.stdout.close()
sys.stdout=stdoutOrigin
Metashape.app.quit()