#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 15:40:39 2023

@author: cjcurry
"""

import os
import shutil
import subprocess
root = "/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/histocat"
probroot = "/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/probability_mask"
folders = os.listdir(root)
folders = [i for i in folders if i != '.DS_Store']

markers = ['196Pt','195Pt', 'Yb176', 'Eu151']
mega_marker = 'Eu151'
nuclei_marker = 'Yb176'
failures = []

for folder in folders:
    roi = os.path.join(root,folder)
    files = os.listdir(os.path.join(root, folder))
    # try:
    #     os.mkdir(os.path.join(probroot, folder))
    # except:
    #     print('"prob" directory already exists for this ROI.')
    output = os.path.join(probroot, folder)
    files = [i for i in files if i != '.DS_Store']
    files = [i for i in files if 'Probabilities' not in i]
    megakary = [i for i in files if mega_marker in i]
    nuclei = [i for i in files if nuclei_marker in i]
    files = [item for item in files if any(search in item for search in markers)]
    if len(files) < 4:
        failures = failures + [folder]
        continue
    file_string = ' '.join(files)
    os.chdir(os.path.join(root, folder))
    # subprocess.run('/Applications/ilastik-1.4.0-OSX.app/Contents/ilastik-release/run_ilastik.sh --headless \
    #                 --project=/Users/cjcurry/IMC_Bone_Marrow.ilp \
    #                 --export_source=Probabilities \
    #                 --output_format="tiff sequence" \
    #                 --output_filename_format='+output+'/{nickname}_{result_type}_{slice_index}.tiff \\'
    #                 +file_string, shell=True)
    files = os.listdir(output)
    nuc = [item for item in files if ('Yb176' in item) & ('0.tiff' in item)]
    membrane = [item for item in files if ('Pt' in item) & ('1.tiff' in item)]
    #mega = [item for item in files if ('Eu151' in item) & ('2.tiff' in item)]
    needed = nuc + membrane
    for file in files:
        if file not in needed:
            os.remove(os.path.join(output,file))
    shutil.copyfile(os.path.join(root,folder,megakary[0]), os.path.join(output,megakary[0]))
    shutil.copyfile(os.path.join(root,folder,nuclei[0]), os.path.join(output,nuclei[0]))

    # output = os.path.join(root,folder,'masks')
    # #inp = os.path.join(root,folder,'prob')
    # inpdir = os.listdir(inp)
    # inpdir = [os.path.join(inp,x) for x in inpdir]
    # with open('input_list.txt', mode='wt', encoding='utf-8') as myfile:
    #     myfile.write('\n'.join(inpdir))
    
    # subprocess.run('/Applications/CellProfiler.app/Contents/MacOS/cp \
    #                -c \
    #                -r -p /Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/resources/pipelines/BM_segmentation_ilastik.cpproj \
    #                -o ' +output+' -i', shell=True)
    #               # --file-list '+roi+'/input_list.txt', shell=True)
    # break
    

    
# for file cleanup
dir='/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/segmentation_mask'
folders = os.listdir(dir)
folders = [i for i in folders if i != '.DS_Store']

for folder in folders:
    files = os.listdir(os.path.join(dir,folder))
    files = [i for i in files if i != '.DS_Store']
    for name in files:
        if name.endswith(("_test.tiff")):
          os.remove(os.path.join(dir,folder, name))



