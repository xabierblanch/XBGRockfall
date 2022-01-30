# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:47:43 2020

@author: XBG
contact: xabierblanch@gmail.com
University of Barcelona
RISKNAT Research Group

This code uses other works published previously by other authors.
I'm open to implement improvements, increase the usability
Use it freely respecting the citations

Free knowledge makes community ♥

"""

#%%###############################################################################################
##################################################################################################
################################ SETUP SECTION (Script Parameters) ###############################

  #%% IMPORT FUNCTIONS AND INITIALIZATION
    
import os
from datetime import datetime
import cv2
import numpy as np

os.chdir('..')     
dirpath = os.getcwd()
os.chdir(dirpath + "/2_lib")

from sharpen_test import blur_detection
from GCP_tracking import performFeatureTrackingLK
from GCP_tracking import mask_tracking
from file_mgmt import find_all
# from file_mgmt import check_number
from CloudCompare_M3C2 import M3C2_Crop2D
import shutil
# from rockfall_extraction import dbscan

#%% LOOP 4D - IMAGE LOCATION

#Project_name ()

project_name = "HRCam_4D"

#%% LOOP 4D - IMAGE LOCATION

paths=[dirpath + '/4_TEST_DATA/HRCam1_Puigcercos',dirpath + '/4_TEST_DATA/HRCam2_Puigcercos',dirpath + '/4_TEST_DATA/HRCam3_Puigcercos',dirpath + '/4_TEST_DATA/HRCam4_Puigcercos',dirpath + '/4_TEST_DATA/HRCam5_Puigcercos']

files = [os.listdir(paths[0]),os.listdir(paths[1]),os.listdir(paths[2]),os.listdir(paths[3]),os.listdir(paths[4])]

dates = []
for i in range (len(files[1])):
    dates.append(files[1][i][7:15])  

dates = list(dict.fromkeys(dates))

for i in range (1,len(dates)):
     
    #%% FOLDER CREATION AND GENERAL SOURCE IMAGE PATHS
    
    file_name = [dates[i+24],dates[i+30]]
    
    now = datetime.now()
    
    try:
        shutil.rmtree(dirpath + "/" + file_name[0] + "_" + file_name[1] + "_" +  project_name + "/") 
        print("Project folder deleted")
    except:
        print("Project folder doesn't exist")
    
    os.mkdir(dirpath + "/" + file_name[0] + "_" + file_name[1] + "_" +  project_name + "/")
    project_path=(dirpath + "/" + file_name[0] + "_" + file_name[1] + "_" +  project_name)
    label=file_name[0] + "_" + file_name[1] + "_" +  project_name
    os.mkdir(project_path + "/1_process_files")
    os.mkdir(project_path + "/2_results")
    os.mkdir(project_path + "/2_results/1_DensePointClouds")
    os.mkdir(project_path + "/2_results/2_M3C2")
    os.mkdir(project_path + "/2_results/3_Rockfalls")
    os.mkdir(project_path + "/1_process_files/1_markers_GCP")
    os.mkdir(project_path + "/1_process_files/2_masks")
    os.mkdir(project_path + "/1_process_files/3_metashape")
    os.mkdir(project_path + "/3_data")
    
    print("\n##############################################################n")
    
    print("\nXBG_Process initialized\n")
    
    #print("Script parameters -> days_before {}, time_gap: {}, project_name: {}\n".format(days_before,time_gap,project_name))
        
    print ("The Script will run this comparison: {} vs {}.".format(file_name[0],file_name[1]))
       
    #test path (uncheck if doesn't has acces to the server)
    paths=[dirpath + '/4_TEST_DATA/HRCam1_Puigcercos',dirpath + '/4_TEST_DATA/HRCam2_Puigcercos',dirpath + '/4_TEST_DATA/HRCam3_Puigcercos',dirpath + '/4_TEST_DATA/HRCam4_Puigcercos',dirpath + '/4_TEST_DATA/HRCam5_Puigcercos']
    
    #%% DATA MANAGEMENT (THIS SECTION HAVE TO BE ADAPTED FOR EVERY USER)
        
    print("\nImage management started. The selected images will be moved to the 3_data folder\n")   
    for date in file_name:
        try:
            for path in paths:       
                find_all(date,path,project_path)
        except:
            print("Image source doesn't exist")
    
    # option=check_number(project_path)
    # if option == 2:
        # raise SystemExit
    
    #%% SHARPEN\BLUR QUALITY FILTER
    
    print("\nInitiated blur detection\n")
    blur_detection(project_path)
    # option=check_number(project_path)
    # if option == 2:
        # raise SystemExit
    print("\nFinished blur detection\n")    
    
    #%% GCPs TRACKING and MASK CREATION
    
    print("\nInitiated GCP's tracking\n")
    for referencePath in os.listdir(dirpath + "/3_reference/1_reference_GCP/1_reference_images"):  
        try:    
            for imagePath in os.listdir(project_path + "/3_data/" + referencePath[0:6] + "_Puigcercos"):
                try:
                    [trackedFeatures, status] = performFeatureTrackingLK(dirpath, project_path, referencePath, imagePath,False)           
                    np.savetxt(project_path + "/1_process_files/1_markers_GCP/markers_" + imagePath + ".txt", trackedFeatures, delimiter='\t', fmt='%0.3f')
                    print(imagePath + " GCP's tracking performed")
                    
                except:
                    print("GCP tracking can't be performed. File {} exist but doesnt has GCP reference".format(imagePath))
                try:
                    img_coregistered = mask_tracking(dirpath, referencePath, imagePath, trackedFeatures)
                    cv2.imwrite(project_path + "/1_process_files/2_masks/" + imagePath, img_coregistered) 
                    print(imagePath + " Masks files performed")
                except:
                    print(print("Masks files can't be created. File {} exist but doesnt has mask reference".format(imagePath)))
        except:
            print("{} images doesn't exist and the GCP tracking is not performed".format(referencePath[0:6]))
            
    print("\nFinished GCP's tracking\n")
            
    #%% SCRIPT UPDATE
    # Function4 -> Cam_calibration
            
    #%% AGISOFT WORKFLOW 1
    
    print("\nLaunch of Agisoft Metashape's first workflow. Check the new opened terminal\n")               
    os.system('"C:/Program Files/Agisoft/Metashape Pro/metashape.exe" --gui -r ' + dirpath + "/2_lib/metashape_aligment.py " + project_path + " " + label + " " + dirpath)     
    print("First Agisoft Metashape wokflow ended. Check the log_metashape file to detect errors\n")                      
    
    #%% POINT COORDINATE PRECISION
    #Author: Mike James 2019
    
    print("\nMike James' Code Running\n")               
    os.system('"C:/Program Files/Agisoft/Metashape Pro/metashape.exe" -r ' + dirpath + "/2_lib/export_point_coordinate_precision_MJames_[mod].py " + project_path + " " + label)            
    print("Mike James' Code Running ended. Check the file saved in the results folder\n")  
    
    #%% AGISOFT WORKFLOW 2
    
    print("\nLaunch of Agisoft Metashape's second workflow. Check the new open terminal\n")               
    os.system("cmd /c" '"C:/Program Files/Agisoft/Metashape Pro/metashape.exe" --gui -r ' + dirpath + "/2_lib/metashape_densecloud.py " + project_path + " " + label)        
    print("Second Agisoft Metashape wokflow ended. Check the log_metashape file to detect errors\n") 
    
    #%% CloudCompare + M3C2
    
    print("\nThe comparison of the M3C2 cloud starts. During the loading of the point clouds no pop-ups will be shown. Check task managers to see CloudCompare working\n")               
    
    [file1,file2]=os.listdir(project_path + '/2_results/1_DensePointClouds')
    
    path_file_1 = project_path + '/2_results/1_DensePointClouds/' + file1
    path_file_2 = project_path + '/2_results/1_DensePointClouds/' + file2    
    path_M3C2_file = project_path + '/2_results/2_M3C2/' + file1[0:len(file1)-4] + '_' + file2[0:len(file1)-4] + '.xyz'
    M3C2_Parameters = dirpath + "/2_lib/m3c2_params.txt"
            
    # CROP2D_ZY = "10.55951309 -50.24749374 30.70545959 -49.92360306 33.16702271 -30.36065674 33.36135864 22.30382729 10.23562336 22.62771797"
      
    # CROP2D_ZY = "26.163 -72.766 28.338 -61.129 32.182 -43.364 31.613 -30.615 33.077 -28.934 32.810 8.141 9.865 8.341 11.057 -58.444 16.232 -64.045 16.870 -66.056 15.841 -69.445 17.456 -74.236 26.192 -73.060" 
    
    # CROP2D_ZY = "29.92826 -56.34698 14.16985 -57.24696 10.11440 -56.58390 8.80823 10.40658 10.86383 22.60760 30.37924 22.81836 32.52592 19.59346 33.36720 -27.99439 32.57182 -44.21746 29.72573 -56.36671"
    
    CROP2D_ZY = "29.54740 -59.51600 10.64730 -58.64710 8.95050 6.44140 33.1236 6.63770 33.36150 -29.60800 31.82770 -49.03520 29.54740 -59.51600"
        
    M3C2_Crop2D(path_file_1,path_file_2,M3C2_Parameters,path_M3C2_file, CROP2D_ZY)
    
    print("\nM3C2 Comparison made. Check the results in the folder results\n")
        
     #%% Rockfall extraction
     
    print("\nRockfall extraction process\n")
    # eps=0.1
    # min_samples=250
    # dbscan(path_M3C2_file, project_path)  
    print("\nRockfall extraction process\n")
    
    print("\nThe code has been completed. Remember that you can check all the files generated in the different folders\n")
    
    print("\n##############################################################\n")