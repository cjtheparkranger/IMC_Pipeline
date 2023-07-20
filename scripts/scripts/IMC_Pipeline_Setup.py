# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import subprocess
import webbrowser

root_dir = os.getcwd()

# install squidpy
squid = input('Do you have squidpy installed? y/n: ')

if squid =='n':
    subprocess.run('conda install -c conda-forge squidpy', shell=True)
    #subprocess.run('conda install hdf5plugin', shell=True)


# install IMC segmentation pipeline
seg = input('Do you have IMC Segmentation Pipeline installed? y/n: ')
if seg == 'n':
    subprocess.run('git clone --recursive https://github.com/BodenmillerGroup/ImcSegmentationPipeline.git', shell=True)
    subprocess.run('cd ImcSegmentationPipeline \
                   conda env create -f environment.yml', shell=True)
               
               
# install IMC Denoise
denoise = input('Do you have IMC Denoise installed? y/n :')
if denoise == 'n':
    subprocess.run('conda create -n "IMC_Denoise"', shell=True)
    subprocess.run('conda activate IMC_Denoise', shell=True)
    subprocess.run('conda install -c anaconda brotlipy', shell=True)
    subprocess.run('pip install tensorflow keras', shell=True)
                   
    subprocess.run('git clone https://github.com/PENGLU-WashU/IMC_Denoise.git', shell=True)
    
    os.replace('IMC_Denoise/setup.py', 'training_modules/setup.py')
    subprocess.run('cd IMC_Denoise \
                   pip install -e .', shell=True)
                   

#prompt ilastik installation  
ilastik = input('Do you have Ilastik installed? y/n: ')

if ilastik == 'n':
    input('Follow the installation instructions on the website that is about to be opened. Press enter to continue.')
    webbrowser.open('https://www.ilastik.org/documentation/basics/installation.html')      

#prompt cellprofiler installation  

cellprofiler = input('Do you have CellProfiler installed? y/n: ')

if cellprofiler == 'n':
    input('Follow the installation instructions on the website that is about to be opened. Press enter to continue.')
    webbrowser.open('https://cellprofiler.org/releases')
    
    
    
    