######################### NEXT LINES ARE ADDED BY XBG IN ORDER TO ADAPT THE ORIGINAL MIKE JAMES SCRIPT #########################
import Metashape
import sys
#Set variables
project_path = sys.argv[1]
name_project = sys.argv[2]
doc = Metashape.app.document
doc.read_only = False
doc.open(project_path + "/1_process_files/3_metashape/" + name_project + ".psx")
doc.read_only = False
out_path = project_path + "/2_results/" + name_project + '_pt_prec.txt'
chunk = doc.chunk

################################################## ORIGINAL MIKE JAMES SCRIPT ##################################################

#import Metashape                                               (disabled by XBG)
import csv
import math

# For use with Metashape Pro v.1.5
#
# Python script associated with James et al. - 
# Mitigating systematic error in topographic models for geomorphic change detection:
# Accuracy, precision and moving beyond off-nadir imagery, Earth Surf. Proc. Landforms
# 
# This script uses Metashape's point coordinate variance estimates to provide oriented and scaled
# point coordinate precision estimates, exported as a text file. 
#
# The text file is saved in the same directory as the Metashape project, with the project file 
# name appended with '_pt_prec.txt'. The file is tab-separated, with one header row and columns:
# X(m) Y(m) Z(m) sX(mm) sY(mm) sZ(mm) covXX(m2) covXY(m2) covXZ(m2) covYY(m2) covYZ(m2) covZZ(m2)
# Where:	X, Y, Z are point coordinates
#			sX, sY, xZ are point coordinate precisions, and
#			cov... are point coordinate covariances.
# Note that units are assumed to be metric, and are as given above (and in the file header line).
#
# Running this script resets the project region to default values.
# 
# Tested and used in PhotoScan Pro v.1.5.0
# Thanks to Paul Pelletier (pap1956@gmail.com) for correcting errors in an early version of this script 
# and (in conjunction with Alexey Pasumansky) for providing the coordinate system transformation code.
# 
# Author: Mike James, Lancaster University, U.K.
# Contact: m.james at lancaster.ac.uk
# Updates: Check http://tinyurl.com/sfmgeoref

#doc = Metashape.app.document                                   (disabled by XBG)
#chunk = doc.chunk                                              (disabled by XBG)
points = chunk.point_cloud.points
point_proj = chunk.point_cloud.projections
npoints = len(points)

#out_path = doc.path[0:(len(doc.path)-4)] + '_pt_prec.txt'      (disabled by XBG)

# Get transforms to account for real-world coordinate system (CRS)
# Note, this resets the region to the default
M = chunk.transform.matrix
region = chunk.region
T = chunk.crs.localframe(M.mulp(chunk.region.center)) * M
if chunk.transform.scale:
	R = chunk.transform.scale * T.rotation()
else:
	R = T.rotation()

# Open the output file and write the precision estimates to file
with open(out_path, "w") as fid:
	# Open the output file
	fwriter = csv.writer(fid, delimiter='\t', lineterminator='\n')
	
	# Write the header line
	fwriter.writerow( [	'X(m)', 'Y(m)', 'Z(m)', 'sX(mm)', 'sY(mm)', 'sZ(mm)',
						'covXX(m2)', 'covXY(m2)', 'covXZ(m2)', 'covYY(m2)', 'covYZ(m2)', 'covZZ(m2)'] )					

	# Iterate through all valid points, writing a line to the file for each point
	for point in chunk.point_cloud.points:
		if not point.valid:
			continue
		
		# Transform the point coordinates into the output local coordinate system
		if chunk.crs:
			V = M * (point.coord)
			V.size = 3
			pt_coord = chunk.crs.project(V)
		else:
			V = M * (point.coord)
			V.size = 3
			pt_coord = V

		# Transform the point covariance matrix into the output local coordinate system
		pt_covars = R * point.cov * R.t()

		# Write the line of coordinates, precisions and covariances to the text file
		fwriter.writerow( [ 
			'{0:0.5f}'.format( pt_coord[0] ), '{0:0.5f}'.format( pt_coord[1] ), '{0:0.5f}'.format( pt_coord[2] ),
			'{0:0.7f}'.format( math.sqrt(pt_covars[0, 0])*1000 ), '{0:0.7f}'.format( math.sqrt(pt_covars[1,1])*1000 ), '{0:0.7f}'.format( math.sqrt(pt_covars[2, 2] )*1000),
			'{0:0.9f}'.format( pt_covars[0, 0] ), '{0:0.9f}'.format( pt_covars[0, 1] ), '{0:0.9f}'.format( pt_covars[0, 2] ),
			'{0:0.9f}'.format( pt_covars[1, 1] ), '{0:0.9f}'.format( pt_covars[1, 2] ), '{0:0.9f}'.format( pt_covars[2, 2] ) ] )

				 
	# Close the text file
	fid.close()
    
doc.save(project_path + '/1_process_files/3_metashape/' + name_project + '.psx')