#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 16:49:00 2023

@author: cjcurry
"""

from steinbock import measurement, export
import pandas as pd
import os
import numpy as np

img = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/histocat/BS17_slide1_s0_a1_ac'
mask = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/segmentation_mask/BS17_slide1_s0_a1_ac/BS17_slide1_s0_a1_ac_segmentation_mask.tiff'
channels = pd.read_csv('/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/raw/panel.csv')
channels = channels['channel']
measurement.intensities.measure_intensities(img, mask, channels, measurement.IntensityAggregation())

