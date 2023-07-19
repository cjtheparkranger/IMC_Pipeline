#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 11:25:15 2023

@author: cjcurry
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from IMC_Denoise.DeepSNiF_utils.DeepSNiF_DataGenerator import DeepSNiF_DataGenerator, load_training_patches
from IMC_Denoise.IMC_Denoise_main.DeepSNiF import DeepSNiF


panel = pd.read_csv('/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/raw/panel.csv')

# Release memory
if 'generated_patches' in globals():
    del generated_patches
    
channel_name = input('Which marker would you like to train a network for?')
Raw_directory = "/Users/cjcurry/Documents/IMC_Pipeline/ImcSegmentationPipeline/analysis/histocat_raw" # change this directory to your Raw_image_directory.
Save_directory = "/Users/cjcurry/Documents/python/IMC_Denoise/Raw_IMC_dataset_all_training_data" # If None, it will be saved in the default folder.

protein = panel['name'][panel['channel'] == channel_name]
n_neighbours = 4 # Larger n enables removing more consecutive hot pixels. 
n_iter = 3 # Iteration number for DIMR

DataGenerator = DeepSNiF_DataGenerator(channel_name = channel_name, n_neighbours = n_neighbours, n_iter = n_iter)
generated_patches = DataGenerator.generate_patches_from_directory(load_directory = Raw_directory)
if DataGenerator.save_patches(generated_patches, save_directory = Save_directory):
    print('Data generated successfully!')
    
saved_training_set = 'training_set_'+channel_name+'.npz'
train_data = load_training_patches(filename = saved_training_set, save_directory = Save_directory)
print('The shape of the loaded training set is ' + str(train_data.shape))

train_epoches = 50 # training epoches, which should be about 200 for a good training result. The default is 200.
train_initial_lr = 1e-3 # inital learning rate. The default is 1e-3.
train_batch_size = 128 # training batch size. For a GPU with smaller memory, it can be tuned smaller. The default is 128.
pixel_mask_percent = 0.2 # percentage of the masked pixels in each patch. The default is 0.2.
val_set_percent = 0.15 # percentage of validation set. The default is 0.15.
loss_function = "I_divergence" # loss function used. The default is "I_divergence".
weights_name = "weights_"+channel_name+'-'+protein+".hdf5" # trained network weights name. If None, the weights will not be saved.
loss_name = None # training and validation losses name, either .mat or .npz format. If not defined, the losses will not be saved.
weights_save_directory = '/Users/cjcurry/Documents/IMC_Pipeline/IMC_Denoise/trained_weights' # location where 'weights_name' and 'loss_name' saved.
# If the value is None, the files will be saved in a sub-directory named "trained_weights" of the current file folder.
is_load_weights = False # Use the trained model directly. Will not read from any saved ones.
lambda_HF = 3e-6 # HF regularization parameter.
deepsnif = DeepSNiF(train_epoches = train_epoches, 
                  train_learning_rate = train_initial_lr,
                  train_batch_size = train_batch_size,
                  mask_perc_pix = pixel_mask_percent,
                  val_perc = val_set_percent,
                  loss_func = loss_function,
                  weights_name = weights_name,
                  loss_name = loss_name,
                  weights_dir = weights_save_directory, 
                  is_load_weights = is_load_weights,
                  lambda_HF = lambda_HF)

train_loss, val_loss = deepsnif.train(train_data)

print('Training of '+channel_name+' is complete.')