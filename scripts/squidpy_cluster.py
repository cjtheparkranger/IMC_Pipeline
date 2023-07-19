#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 12:34:26 2023

@author: cjcurry
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import scanpy as sc
import squidpy as sq
from anndata import AnnData
from anndata.experimental.pytorch import AnnLoader
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import torch
import torch.nn as nn
import seaborn as sbn



ints = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/normalization/intensities_normalized'
reg = '/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/normalization/regionprops'
acollection = {}
files = os.listdir(ints)
files = [i for i in files if i != '.DS_Store']

rois = {}
for file in files:
    #roi = file.replace('_intensities.csv','')
    roi = 'BS17_slide1_s0_a1_ac'
    intensity = pd.read_csv(os.path.join(ints,roi+'_intensities.csv'))
    channels = list(intensity.columns)
    intensity['set'] = roi
    intensity['in_temp'] = np.nan
    for x in intensity.index:
        intensity['in_temp'][x] = "Cell "+str(intensity['Object'][x])+' of '+roi
    intensity.index = intensity['in_temp'].rename('Index')
    sets = intensity['set']
    
    
    regions = pd.read_csv(os.path.join(reg,roi+'_regionprops.csv')).drop(columns=['Object'])
    coordinates= regions.iloc[:,[1,2]]
    coordinates.index = intensity.index
    intensity = intensity.drop(columns=['Object','in_temp','set'])
    adata = AnnData(intensity)

    
    adata = AnnData(intensity.to_numpy(), obsm={"spatial": coordinates.to_numpy()})
    
    # adata.obs_names['set'] = intensity.index.to_numpy()
    rois[roi] = adata



channels_use = ['aSMA', 'CD14', 'CD16', 'CD163', 'CD11b', 'CD31', 'CD45', 'BCMA', 'CD11c', 'FOXP3', 'CD4',
            'CD68', 'CD117', 'CD20', 'CD8', 'CD56', 'CD138', 'CD3', 'CD27', 'HLADR']

channels_list = list()
for x in channels:
    if x in channels_use:
        channels_list = channels_list + [channels.index(x)]
        



# var = ['cell1','cell2','cell3','cell4','cell5','cell6','cell7','cell8']
# adata.var_names = var


#necessary object creation for clustering
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)



# creation of leiden clustering for different resolution levels
sc.tl.leiden(adata, key_added = "leiden_1.0") # default resolution in 1.0
sc.tl.leiden(adata, resolution = 0.6, key_added = "leiden_0.6")
sc.tl.leiden(adata, resolution = 0.4, key_added = "leiden_0.4")
sc.tl.leiden(adata, resolution = 1.4, key_added = "leiden_1.4")
adata

sq.pl.spatial_scatter(adata, shape=None, color=['leiden_0.4', 'leiden_0.6', 'leiden_1.0','leiden_1.4'], size=50)
#sc.pl.heatmap(adata, var, groupby=['leiden_0.4', 'leiden_0.6', 'leiden_1.0','leiden_1.4'])

# heatmap testing code
# cluster = adata.obs
# intensity['leiden_0.6'] = cluster['leiden_0.6'].to_list()
# intensity['leiden_0.6'] = intensity['leiden_0.6'].dtype(float)



# test = sbn.heatmap(intensity)







