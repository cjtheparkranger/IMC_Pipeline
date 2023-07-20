#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 17:34:07 2023

@author: cjcurry
"""

import subprocess
import os
import shutil

ints = 'intensities/'
ints_run = 'intensities_run/'
nei = 'neighbors/'
nei_run = 'neighbors_run/'
rg = 'regionprops/'
rg_run = 'regionprops_run/'
output = 'output/'
try:
    os.mkdir(output)
    os.mkdir(ints_run)
    os.mkdir(nei_run)
    os.mkdir(rg_run)
    print('Running directories created.')
except:
    print('Running directories already exist.')



rois = os.listdir(ints)


for roi in rois:
    file = roi.replace('_segmentation_mask.csv','')
    shutil.move(ints+roi, ints_run+roi)
    shutil.move(nei+roi, nei_run+roi)
    shutil.move(rg+roi, rg_run+roi)

    subprocess.run('steinbock export anndata --intensities intensities_run --data regionprops_run --neighbors neighbors_run -o '+file+'.h5ad', shell=True)
    
    shutil.move(ints_run+roi, ints+roi)
    shutil.move(nei_run+roi, nei+roi)
    shutil.move(rg_run+roi, rg+roi)
    #shutil.move(file+'.h5ad', 'output/'+file+'.h5ad')
    
    print('AnnData file for '+file+'.')


os.remove(ints_run)
os.remove(nei_run)
os.remove(rg_run)
print('Running directories now deleted.')
print('All annData files generated.')
