# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 23:52:44 2020

@author: XBG
"""

from sklearn.cluster import DBSCAN
import numpy as np
from scipy.spatial import Delaunay
import scipy.spatial as ss


# m3c2 = np.loadtxt("1_Data_Test/20191108_20191113.xyz")

# #%%

# ## Filter

# backup = m3c2

# m3c2 = backup

# isnan = np.isnan(m3c2) 

# m3c2 = np.delete(m3c2, np.argwhere(isnan == 1),0)

# m3c2 = np.delete(m3c2, np.argwhere(m3c2[:,5] < 0.03),0)

# ## DBSCAN

# x=np.array([m3c2[:,0],m3c2[:,1],m3c2[:,2]])
# X=x.transpose()

# db = DBSCAN(eps=0.1, min_samples=250).fit(X)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True
# labels = db.labels_

# m3c2 = np.delete(m3c2, np.argwhere(labels == -1),0)
# labels = np.delete(labels, np.argwhere(labels == -1),0)

# result=np.vstack([m3c2[:,0],m3c2[:,1],m3c2[:,2],m3c2[:,5],labels])
# result=result.transpose()

# np.savetxt('1_Data_Test/M3C2_dbscan.xyz', result, fmt='%10.4f') 

#%%
import matplotlib.pyplot as plt
rockfall = np.loadtxt("1_Data_Test/M3C2_dbscan.xyz", dtype=np.float32)

#for x in [0,max(rockfall[:,4])]:
    
ky=np.argwhere(rockfall[:,4]==0)

x=rockfall[ky,0];
y=rockfall[ky,1];
diff=rockfall[ky,1]-rockfall[ky,3];
z=rockfall[ky,2];

# differences=np.append(y,diff)
# x=np.append(x,x)
# z=np.append(z,z)

# points=np.vstack([x,z,differences])
# points=points.transpose()
points=np.append(x,z, axis=1)

tri=Delaunay(points);
conect=tri.vertices;
vol_total=0;

for k in range(0,len(tri.simplices)):     

    x_point=np.array([x[conect[k,0]],x[conect[k,1]],x[conect[k,2]],x[conect[k,0]],x[conect[k,1]],x[conect[k,2]]])
    z_point=np.array([z[conect[k,0]],z[conect[k,1]],z[conect[k,2]],z[conect[k,0]],z[conect[k,1]],z[conect[k,2]]])
    y_point=np.array([y[conect[k,0]],y[conect[k,1]],y[conect[k,2]],diff[conect[k,0]],diff[conect[k,1]],diff[conect[k,2]]])
    result=np.append(x_point,z_point,axis=1)
    result=np.append(result, y_point, axis=1)
    hull = ss.ConvexHull(result)
    print('volume inside points is: ',hull.volume)
    vol=hull.volume
    vol_total=vol_total+vol
    plt.plot(result[:,0], result[:,1], 'o')

plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(result[:,0], result[:,1], 'o')
plt.show()
# plt.savefig("temp.png")

plt.plot(result[hull.vertices[0],0], result[hull.vertices[0],1], 'ro')
plt.plot(result[hull.vertices,0], result[hull.vertices,1], 'r--', lw=2)
plt.show()

import matplotlib.pyplot as plt
plt.plot(result[:,0], result[:,1], 'o')
for simplex in hull.simplices:
    plt.plot(result[simplex, 0], result[simplex, 1], 'k-')

