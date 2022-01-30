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

def calc_reprojection(chunk):
    point_cloud = chunk.point_cloud
    points = point_cloud.points
    npoints = len(points)
    projections = chunk.point_cloud.projections
    err_sum = 0
    num = 0
    maxe = 0

    point_ids = [-1] * len(point_cloud.tracks)
    point_errors = dict()
    for point_id in range(0, npoints):
        point_ids[points[point_id].track_id] = point_id

    for camera in chunk.cameras:
        if not camera.transform:
            continue
        for proj in projections[camera]:
            track_id = proj.track_id
            point_id = point_ids[track_id]
            if point_id < 0:
                continue
            point = points[point_id]
            if not point.valid:
                continue
            error = camera.error(point.coord, proj.coord).norm() ** 2
            err_sum += error
            num += 1
            if point_id not in point_errors.keys():
                point_errors[point_id] = [error]
            else:
                point_errors[point_id].append(error)
            if math.sqrt(error) > maxe: maxe = math.sqrt(error)

    sigma = math.sqrt(err_sum / num)
    return sigma, maxe    #point_errors

def calc_reprojectionMarker(chunk):
    rmsGCP = []
    rmsCP = []
    diff3D_GCP = []
    diff3D_CP = []
    numSqGCP = 0
    numSqCP = 0
    num3DGCP = 0
    num3DCP = 0
    for marker in chunk.markers:
        #error in image space
        diff = []
        for camera in chunk.cameras:
            try:
                v_proj = marker.projections[camera].coord #2 dimensional vector of the marker projection on the photo
                v_reproj = camera.project(marker.position) #2 dimensional vector of projected 3D marker position
                error = (v_proj - v_reproj).norm() #reprojection error for current photo
                diff.append(error)
                if marker.reference.enabled:
                    rmsGCP.append(error ** 2)
                    numSqGCP += 1
                else:
                    rmsCP.append(error ** 2)
                    numSqCP += 1
            except Exception as e:
                print(e)
                print('marker ' + marker.label + ' in camera ' + camera.label + ' has no projection')

        #error in object space
        error = (chunk.transform.matrix.mulp(marker.position) - chunk.crs.unproject(marker.reference.location)).norm() ** 2
        if marker.reference.enabled:
            diff3D_GCP.append(error)
            num3DGCP += 1
        else:
            diff3D_CP.append(error)
            num3DCP += 1

    #image space
    rmsGCP = math.sqrt(sum(rmsGCP) / numSqGCP)
    # rmsCP = math.sqrt(sum(rmsCP) / numSqCP) #ONLY IF I HAVE CONTROL POINTS

    #object space
    rmsGCP_3D = math.sqrt(sum(diff3D_GCP) / num3DGCP)
    # rmsCP_3D = math.sqrt(sum(diff3D_CP) / num3DCP) #ONLY IF I HAVE CONTROL POINTS

    return rmsGCP, rmsGCP_3D, #rmsCP, #rmsCP_3D

#Set variables
path_project = sys.argv[1]
label = sys.argv[2]
dirpath = sys.argv[3]

# prepare log file
stdoutOrigin=sys.stdout 
sys.stdout = open(path_project + "/1_process_files/3_metashape/Aligment.log", "w")

doc = Metashape.app.document
doc.read_only = False
doc.save(path_project + "/1_process_files/3_metashape/" + label + ".psx")
doc.read_only = False
chunk_original = doc.chunk
    
Metashape.app.cpu_enable = True
Metashape.app.gpu_mask = 1
Metashape.app.update()
doc.save(path_project + "/1_process_files/3_metashape/" + label + ".psx")

#%%STEP0 -> Load images in camera groups

path_master = path_project + "/3_data"

sub_folders = os.listdir(path_master)
for folder in sub_folders:
	folder = os.path.join(path_master, folder)
	if not os.path.isdir(folder):
		continue

	image_list = os.listdir(folder)
	if len(image_list)>0:
		print("Creating a new camera group")
		photo_list = list()
		new_group = chunk_original.addCameraGroup()
		new_group.label = os.path.basename(folder)
		for photo in image_list:
			if photo.rsplit(".",1)[1].lower() in  ["jpg", "jpeg", "tif", "tiff"]:
				photo_list.append(os.path.join(folder, photo))
		chunk_original.addPhotos(photo_list)
			   
		for camera in chunk_original.cameras:
			if not camera.group:
				camera.group = new_group
	else: 		
		print("Empty folder")
        
for groups in chunk_original.camera_groups:
	  if groups.label == 'unusable_images':
		  del_group = groups

try:    
	chunk_original.remove(del_group)
except:
	print("")

print("Image upload finished")

#%% STEP 1 -> Calibration Camera Groups (Create as many groups as systems are installed)
            
for camera in chunk_original.cameras:   
    if camera.label[0:6] == "HRCam1":      
        sensor1 = chunk_original.addSensor()
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
        sensor2 = chunk_original.addSensor()
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
        sensor3 = chunk_original.addSensor()
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
        sensor4 = chunk_original.addSensor()
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
        sensor5 = chunk_original.addSensor()
        sensor5.label = camera.label
        sensor5.type = camera.sensor.type
        sensor5.calibration = camera.sensor.calibration
        sensor5.width = camera.sensor.width
        sensor5.height = camera.sensor.height
        sensor5.focal_length = camera.sensor.focal_length
        sensor5.pixel_height = camera.sensor.pixel_height
        sensor5.pixel_width = camera.sensor.pixel_width
        camera.sensor = sensor5

for camera in chunk_original.cameras:   
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
            
pathToMasks =  path_project + '/1_process_files/2_masks/{filename}.JPG'    
       
for f in chunk_original.frames:
    try:
        f.importMasks(path=pathToMasks, source=Metashape.MaskSource.MaskSourceFile)
    except: 
        print("Error en la mascara")
        
#%% STEP 3 -> Markers 

marker1=chunk_original.addMarker()
marker2=chunk_original.addMarker()
marker3=chunk_original.addMarker()
marker4=chunk_original.addMarker()
marker5=chunk_original.addMarker()

markers_reference=np.loadtxt(dirpath + '/3_reference/1_reference_GCP/reference_markers_LiDAR.txt', delimiter='\t')

chunk_original.marker_location_accuracy = [0.05, 0.05, 0.05] # Marker Accuracy [m]

for marker in chunk_original.markers:
     marker.reference.accuracy = [0.05,  0.05,   0.05] #Marker Accuracy [m]

marker1.reference.location = [markers_reference[0,0], markers_reference[0,1], markers_reference[0,2]]
marker2.reference.location = [markers_reference[1,0], markers_reference[1,1], markers_reference[1,2]]
marker3.reference.location = [markers_reference[2,0], markers_reference[2,1], markers_reference[2,2]]
marker4.reference.location = [markers_reference[3,0], markers_reference[3,1], markers_reference[3,2]]
marker5.reference.location = [markers_reference[4,0], markers_reference[4,1], markers_reference[4,2]]
    
for camera in chunk_original.cameras:  
    markers_track=np.loadtxt(path_project + "/1_process_files/1_markers_GCP/markers_" + camera.label + ".JPG.txt")   
    for i in range(len(markers_track)):         
        new_marker=chunk_original.markers[i]
        if markers_track[i,0] == markers_track[i,0] and markers_track[i,1] == markers_track[i,1]:
            new_marker.projections[camera] = Metashape.Marker.Projection(markers_track[i], True)
            #new_marker.projections[camera] = Metashape.Marker.Projection([0,0], False)           
        else:
            print("No marquer")
                      
print("Ground control points added correctly")

#%% STEP 4 -> Align and optimization Cameras (Loop inspired by Mike James 2017)

chunk_original.tiepoint_accuracy = 0.5
chunk_original.marker_projection_accuracy = 1

iterations = 2

for i in range(iterations): 
    Metashape.app.update()           
     
    t0 = time.time()
     
    chunk_original.matchPhotos(downscale=0, generic_preselection=False, reference_preselection=False, filter_mask=True, mask_tiepoints=False, keypoint_limit=200000, tiepoint_limit=75000, keep_keypoints=True, guided_matching=False, reset_matches=True, subdivide_task=True)
    chunk_original.alignCameras(adaptive_fitting=True, reset_alignment=True, subdivide_task=True)
    doc.save(path_project + "/1_process_files/3_metashape/" + label + ".psx")
    print("Camera aligment performed") 
  
    t1 = time.time()    
            
    print('Total Time aligment iteration '+ str(i) + ': ' +  str((t1-t0)/60) + ' minutes')

    #Optimize Cameras
#     chunk_original.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=False, fit_b2=False, fit_k1=True,
# fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_corrections=True, adaptive_fitting=False, tiepoint_covariance=False)
#     #Update Transform
#     chunk_original.updateTransform()
    
    #doc.save(path_project + '/1_process_files/3_metashape/' + label + '.psx')     
    
    #%% STEP 5 -> Compute RMS reprojection Error (AGISOFT FORUM)
    
    reprojection_rmse, reprojection_maxError = calc_reprojection(chunk_original)
    print("Average tie point residual error: " + str(reprojection_rmse))
    print("Maximum tie point residual error: " + str(reprojection_maxError))
    
    # %% STEP 6 -> Compute Markers error (AGISOFT FORUM)
    
    # error_pix_GCP, error_pix_CP, error_GCP_3D, error_CP_3D = calc_reprojectionMarker(chunk_original)
    error_pix_GCP, error_GCP_3D = calc_reprojectionMarker(chunk_original)
    print("Marker point residual error (GCP): " + str(error_pix_GCP))
    #print("Marker point residual error (CP): " + str(error_pix_CP))
    print("Marker point residual error 3D (GCP): " + str(error_GCP_3D))
    #print("Marker point residual error 3D (CP): " + str(error_CP_3D))        
          
#%% STEP 7 -> Update accuracies and loop again aligment (Loop inspired by Mike James 2017)
    
    chunk_original.tiepoint_accuracy = reprojection_rmse
    chunk_original.marker_projection_accuracy = error_pix_GCP
    
#%% STEP 8 -> Point Filter (based on reprojection error)

threshold_reprojection = 0.5 #0.5 It's a good first approach
threshold_reconstruction = 25
threshold_projection = 6

f = Metashape.PointCloud.Filter()
f.init(chunk_original, criterion = Metashape.PointCloud.Filter.ReprojectionError)
f.removePoints(threshold_reprojection)

f = Metashape.PointCloud.Filter()
f.init(chunk_original, criterion = Metashape.PointCloud.Filter.ReconstructionUncertainty)
f.removePoints(threshold_reconstruction)

f = Metashape.PointCloud.Filter()
f.init(chunk_original, criterion = Metashape.PointCloud.Filter.ProjectionAccuracy)
f.removePoints(threshold_projection)

#%% STEP 8 -> Cameras optimization after last loop iteration and point filter. Tie Point Covariance exported!

#Optimize Cameras
chunk_original.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_corrections=True, adaptive_fitting=False, tiepoint_covariance=True)
#Update Transform
chunk_original.updateTransform()

doc.save(path_project + '/1_process_files/3_metashape/' + label + '.psx')   

# #%% CLOSE LOG FILE
sys.stdout.close()
sys.stdout=stdoutOrigin
Metashape.app.quit()