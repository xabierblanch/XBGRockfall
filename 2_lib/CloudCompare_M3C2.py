# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 00:48:31 2019

@author: Xabier
"""

import subprocess

def M3C2_Crop2D(path_file_1,path_file_2,M3C2_Parameters,path_M3C2_file, CROP2D_ZY):

    M3C2_Command = r'"C:\Program Files\CloudCompare\CloudCompare.exe" -SILENT -AUTO_SAVE OFF -C_EXPORT_FMT ASC -PREC 3 -o "' + path_file_1 + '" -o "' + path_file_2 + '" -CROP2D Y 7 ' + CROP2D_ZY + ' -M3C2 ' + M3C2_Parameters + ' -SAVE_CLOUDS FILE "' + "'" + path_file_1 + "' '" + path_file_2 + "' '" + path_M3C2_file + "'" + '"'
    
    subprocess.run(M3C2_Command)