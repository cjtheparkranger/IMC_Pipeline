#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:39:45 2023

@author: cjcurry
"""

import os
from PIL import Image

tiff_dir = 'ImcSegmentationPipeline/analysis/histocat/'
stack_dir = 'ImcSegmentationPipeline/analysis/tiff_stack/'

rois = os.listdir(tiff_dir)
rois = [i for i in rois if 'BS17' in i]





for roi in rois:
    dic = {}
    files = os.listdir(tiff_dir+roi)
    files = [i for i in files if 'BS17' in i]
    i = 1
    for file in files:
        if i == 1:
            og = Image.open(tiff_dir+roi+'/'+file)
            i = 2
        else:
            dic[file] = Image.open(tiff_dir+roi+'/'+file)
    slices = list(dic.values())
    og.save(stack_dir+roi+".tiff", save_all=True, append_images=slices)

