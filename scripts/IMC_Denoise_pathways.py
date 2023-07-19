#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:36:19 2023

@author: cjcurry
"""


import os
import glob
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from typing import List
import pandas as pd

from sniffing_func import *

rootdir = '/Users/cjcurry/Documents/IMC_Pipeline/IMC_Denoise'
rawdir = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/histocat_raw'
training_dir = '/Users/cjcurry/Documents/IMC_Pipeline/IMC_Denoise/trained_weights'
denoised_dir = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/histocat'

if not os.path.exists(denoised_dir):
    os.mkdir(denoised_dir)

subdirs = os.listdir(rawdir)


temp_trn = os.listdir(training_dir)
trn = []
for x in temp_trn:
    if '.hdf5' in x:
        trn.append(x)

for subdir in subdirs:
    if '.DS_Store' in subdir:
        continue
    else:
        temp_trn = os.listdir(training_dir)
        trn = []
        for x in temp_trn:
            if '.hdf5' in x:
                trn.append(x)
        subpath = rawdir+'/'+subdir
        files = os.listdir(subpath)
        denoised_sub = denoised_dir+'/'+subdir
        if not os.path.exists(denoised_sub):
            os.mkdir(denoised_sub)
        for file in files:
            marker = file[2:5]+file[0:2]
            marker2 = file[0:5]
            Raw_img_name = subdir+'/'+file
            weights = [f for f in trn if marker in f]
            weights2 = [p for p in trn if marker2 in p]
            # if ('190' in marker) | ('190' in marker2):
            #     continue
            try:
                if len(weights) > 0:
                    weights_name = weights[0]
                    print('Training data exists for '+marker+' , intiating prediction module.')
                    IMC_Denoise_Predict(marker, weights_name, Raw_img_name, file, denoised_sub, training_dir, rawdir)
                elif len(weights2) > 0:
                    weights_name = weights2[0]
                    print('Training data exists for '+marker+' , intiating prediction module.')
                    IMC_Denoise_Predict(marker, weights_name, Raw_img_name, file, denoised_sub, training_dir, rawdir)
                else:
                    marker = file[0:5]
                    print('No training data found, self contained training and prediction initiated.')
                    IMC_Denoise_Train_and_Predict(marker, Raw_img_name, file, denoised_sub, rawdir)
            except:
                continue
                
