# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import subprocess
import os

root_dir = os.getcwd()
segpipe = root_dir + '/ImcSegmentationPipeline'
denoise = root_dir + '/IMC_Denoise'

# preprocess .mcd files and convert them to .tiff files
os.chdir(segpipe)
subprocess.run('conda run -n imcsegpipe python scripts/mcd_to_tiff.py', shell=True)
os.chdir(root_dir)

# Activate the denoiser
# os.chdir(denoise)
subprocess.run('conda run -n IMC_Denoise python scripts/IMC_Denoise_pathways.py', shell=True)



# run ilastik to produce probability masks

subprocess.run('conda run -n IMC_Denoise python scripts/ilastik_headless.py', shell=True)

# prompt user to run Cellprofiler
input('Please open CellProfiler and run the "BM_segmentation_ilastik_v2" pipeline in the training_modules folder. For instructions on how to set up the directory, please review the read me file. Press any key to continue after you are done running CellProfiler.')


# run tiff stack
subprocess.run('python scripts/tiff_to_stack.py', shell=True)

# run steinbock loop
subprocess.run('python scripts/anndata_auto.py', shell=True)

#run normalization

subprocess.run('python scripts/normalization.py', shell=True)

#run squidpy cluster
subprocess.run('python scripts/squidpy_cluster.py', shell=True)
