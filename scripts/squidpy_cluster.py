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



ints = 'ImcSegmentationPipeline/analysis/normalization/intensities_normalized'
reg = 'ImcSegmentationPipeline/analysis/normalization/regionprops'
clust = 'ImcSegmentationPipeline/analysis/clustered'
acollection = {}
files = os.listdir(ints)
files = [i for i in files if i != '.DS_Store']
try:
    os.mkdir(clust)
except:
    print('Directory already exists.')

rois = {}
for file in files:
    roi = file.replace('_intensities.csv','')

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
    
    #necessary object creation for clustering
    sc.pp.pca(adata)
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)



    # creation of leiden clustering for different resolution levels
    sc.tl.leiden(adata, key_added = "leiden_1.0") # default resolution in 1.0
    sc.tl.leiden(adata, resolution = 0.6, key_added = "leiden_0.6")
    sc.tl.leiden(adata, resolution = 0.4, key_added = "leiden_0.4")
    sc.tl.leiden(adata, resolution = 1.4, key_added = "leiden_1.4")
    adata.write_h5ad(clust+'/'+roi)
    

    sq.pl.spatial_scatter(adata, shape=None, color=['leiden_0.4', 'leiden_0.6', 'leiden_1.0','leiden_1.4'], size=50)
    #sc.pl.heatmap(adata, var, groupby=['leiden_0.4', 'leiden_0.6', 'leiden_1.0','leiden_1.4'])
    


channels_use = ['aSMA', 'CD14', 'CD16', 'CD163', 'CD11b', 'CD31', 'CD45', 'BCMA', 'CD11c', 'FOXP3', 'CD4',
            'CD68', 'CD117', 'CD20', 'CD8', 'CD56', 'CD138', 'CD3', 'CD27', 'HLADR']

channels_list = list()
for x in channels:
    if x in channels_use:
        channels_list = channels_list + [channels.index(x)]
        








