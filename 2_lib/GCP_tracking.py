# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:24:59 2020

@author: XBG
"""
import cv2
import numpy as np
import pandas as pd

#%% GCP TRACKING

def performFeatureTrackingLK(dirpath, project_path, referencePath, imagePath, useApprox=False, initialEstimateNewPos=None, windowTemplate_x=101, windowTemplate_y=101, maxDistBackForward_px=50):
    
    startImg = cv2.imread(dirpath + "/3_reference/1_reference_GCP/1_reference_images/" + referencePath, 0)
    searchImg = cv2.imread(project_path + "/3_data/" + referencePath[0:6] + "_Puigcercos/" + imagePath , 0)
    featuresToSearch = np.loadtxt(dirpath + "/3_reference/1_reference_GCP/reference_markers_"+referencePath[0:6]+".txt")    
    featuresToSearchFloat = np.asarray(featuresToSearch, dtype=np.float32)

     #parameters for lucas kanade optical flow
    lk_params = dict(winSize  = (windowTemplate_x,windowTemplate_y), maxLevel=3, criteria = (cv2.TERM_CRITERIA_EPS |cv2.TERM_CRITERIA_COUNT, 30, 0.01))

     #calculate optical flow
    if useApprox:
         #work with initial estimates, i.e. pre-set shift of search window
         initialEstimateNewPosFloat = np.asarray(initialEstimateNewPos,dtype=np.float32)
         trackedFeatures, status, _ = cv2.calcOpticalFlowPyrLK(startImg, searchImg, featuresToSearchFloat, initialEstimateNewPosFloat, None, **lk_params)
         #check backwards
         initialEstimateNewPosFloatCheck = trackedFeatures + (featuresToSearchFloat - initialEstimateNewPosFloat) 
         trackedFeaturesCheck, _, _ = cv2.calcOpticalFlowPyrLK(searchImg, startImg, trackedFeatures, initialEstimateNewPosFloatCheck, None, **lk_params)
    else:
         #...or not
         trackedFeatures, status, _ = cv2.calcOpticalFlowPyrLK(startImg, searchImg, featuresToSearchFloat, None, **lk_params)

         #check backwards
         trackedFeaturesCheck, status, _ = cv2.calcOpticalFlowPyrLK(searchImg, startImg, trackedFeatures, None, **lk_params)

      #set points that fail backward forward tracking test to nan
    distBetweenBackForward = abs(featuresToSearch-trackedFeaturesCheck).reshape(-1, 2).max(-1)
    keepGoodTracks = distBetweenBackForward < maxDistBackForward_px
    trackedFeaturesDF = pd.DataFrame(trackedFeatures, columns=['x','y'])
    trackedFeaturesDF.loc[:,'check'] = keepGoodTracks
    trackedFeaturesDF = trackedFeaturesDF.where(trackedFeaturesDF.check == True)
    trackedFeaturesDF = trackedFeaturesDF.drop(['check'], axis=1)
    trackedFeatures = np.asarray(trackedFeaturesDF)

     # cv2.destroyAllWindows()
    return trackedFeatures, status

#%% MASK TRACKING -> CREATE NEW MASKS

def mask_tracking(dirpath, referencePath, imagePath, trackedFeatures):
    # Calculate Homography
    featuresToSearch = np.loadtxt(dirpath + "/3_reference/1_reference_GCP/reference_markers_"+referencePath[0:6]+".txt")
    H_matrix, _ = cv2.findHomography(featuresToSearch, trackedFeatures, cv2.RANSAC, 3)      
    startMask=cv2.imread(dirpath + "/3_reference/1_reference_GCP/2_reference_masks/" + referencePath[0:6] + ".jpg", 0)
    img_coregistered = cv2.warpPerspective(startMask, H_matrix,(startMask.shape[1],startMask.shape[0])) 
 
    return img_coregistered