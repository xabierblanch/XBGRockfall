# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 19:25:44 2020

@author: XBG
"""
                                          
import numpy as np
from scipy.spatial import KDTree
import time

ti = time.time()
print("Step0")
sparse_cloud = np.genfromtxt(fname='1_Data_Test/Dresden_accuracy_pt_prec.txt')
dense_cloud = np.genfromtxt(fname='1_Data_Test/20191113.xyz')
tf = time.time()
print(str(tf-ti) + " seconds\n")

print("Step1")
sparse = sparse_cloud[:,0:3]
dense = dense_cloud[:,0:3]
tf = time.time()
print(str(tf-ti) + " seconds\n")

print("Step2")
kdtree = KDTree(sparse)
[dist,points]=kdtree.query(dense,1)
tf = time.time()
print(str(tf-ti) + " seconds\n")

print("Step3")
errors = sparse_cloud[points,3:6]
tf = time.time()
print(str(tf-ti) + " seconds\n")

print("Step4")
final=np.append(dense, errors, axis=1) 
tf = time.time()
print(str(tf-ti) + " seconds\n")

print("Step5")
np.savetxt('1_Data_Test/20191113_errors.txt',final,fmt='%10.3f')
tf = time.time()
print(str(tf-ti) + " seconds\n")
