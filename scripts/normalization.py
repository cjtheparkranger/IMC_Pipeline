#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:58:29 2023

@author: cjcurry
"""

import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import copy
import matplotlib.pyplot as plt

root = "ImcSegmentationPipeline/analysis/normalization/intensities"
files = os.listdir(root)
files = [i for i in files if i != '.DS_Store']

# to rename files if necessary
# def rename(path, file, label):
#     new = file.replace('segmentation_mask',label)
#     old_file = os.path.join(path, file)
#     new_file = os.path.join(path, new)
#     os.rename(old_file, new_file)
    
# for file in files:    
#     rename(root, file, 'regionprops')
#     rename(root, file, 'neighbors')
#     rename(root, file, 'intensities')



root = 'ImcSegmentationPipeline/analysis/normalization'

ints = 'intensities'

intensities = {}

files = os.listdir(os.path.join(root,ints))
files = [i for i in files if i != '.DS_Store']

for file in files:
    intensities[file] = pd.read_csv(os.path.join(root,ints,file))
# files = [i.replace('_segmentation_mask','_intensities') for i in files]



# create violin plots to map

temp = copy.deepcopy(intensities)
h3 = pd.DataFrame(columns=['HistoneH3','ROI'])
for roi in temp:
    temp[roi]['ROI'] = roi.replace('_intensities.csv','')
    temp[roi] = temp[roi].loc[:,['HistoneH3','ROI']]
    h3 = pd.concat([h3,temp[roi]])
    
    
fig, ax = plt.subplots()

sns.violinplot(ax = ax,
               data = h3,
               x = 'ROI',
               y = 'HistoneH3',
               split = True)

#plt.figure(figsize=(8,4))

plt.xlabel('Region of Interest')
plt.ylabel('Histone H3 Median Intensity')
plt.ylim([-10, 50])
ax.set_title( "Histone H3 Median Intensity by Cell Object" , size = 20 )
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, fontsize=4, ha="right")
plt.tight_layout()
plt.show()










med_int = pd.DataFrame(columns = ['roi','med_int'])
med_int['roi'] = files
for roi in intensities:
    med_int['med_int'][med_int['roi']==roi] = intensities[roi]['HistoneH3'].median()


max_int = med_int['med_int'].max()

med_int['multiplier'] = max_int/med_int['med_int']

for roi in intensities:
    maxx = med_int['multiplier'][med_int['roi']==roi].item()
    intensities[roi].iloc[:,1:] = intensities[roi].iloc[:,1:]*maxx
    




temp = copy.deepcopy(intensities)
h3 = pd.DataFrame(columns=['HistoneH3','ROI'])
for roi in temp:
    temp[roi]['ROI'] = roi.replace('_intensities.csv','')
    temp[roi] = temp[roi].loc[:,['HistoneH3','ROI']]
    h3 = pd.concat([h3,temp[roi]])
    
    

fig, ax = plt.subplots()

sns.set(style="darkgrid")
sns.color_palette("pastel")
sns.violinplot(ax = ax,
               data = h3,
               x = 'ROI',
               y = 'HistoneH3',
               color = 'b',
               split = True)

plt.xlabel('Region of Interest')
plt.ylabel('Histone H3 Median Intensity')
plt.ylim([-10, 60])
ax.set_title( "Histone H3 Median Intensity by Cell Object" , size = 20 )
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, fontsize=4, ha="right")
plt.tight_layout()
plt.show()









zstack = pd.DataFrame()
for roi in intensities:
    intensities[roi]['key'] = roi
    if zstack.empty:
        zstack = intensities[roi]
    else:
        zstack = pd.concat([zstack,intensities[roi]], ignore_index=True)
    
scaler = StandardScaler()


for p in zstack.columns:
    if p in ['Object', 'key']:
        continue
    else:
        data = np.array(zstack[p]).reshape(-1,1)
        scaler.fit(data)
        standardized_dataset = scaler.transform(data)
        zstack[p] = standardized_dataset
            
files = zstack['key'].unique()

for file in files:
    intensities[file] = zstack[zstack['key'] == file]
    intensities[file] = intensities[file].drop(columns = ['key'])
    #intensities[file].to_csv(root+'/intensities_normalized/'+file, index = False)



temp = copy.deepcopy(intensities)
h3 = pd.DataFrame(columns=['HistoneH3','ROI'])
for roi in temp:
    temp[roi]['ROI'] = roi.replace('_intensities.csv','')
    temp[roi] = temp[roi].loc[:,['HistoneH3','ROI']]
    h3 = pd.concat([h3,temp[roi]])
    
    

fig, ax = plt.subplots()

sns.set(style="darkgrid")
sns.color_palette("pastel")
sns.violinplot(ax = ax,
               data = h3,
               x = 'ROI',
               y = 'HistoneH3',
               color = 'b',
               split = True)

plt.xlabel('Region of Interest')
plt.ylabel('Histone H3 Intensity Z-score')
plt.ylim([-2, 10])
ax.set_title( "Z-score Normalized Histone H3 Median Intensity by Cell Object" , size = 15 )
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, fontsize=4, ha="right")
plt.tight_layout()
plt.show()