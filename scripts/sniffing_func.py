#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 17:45:02 2023

@author: cjcurry
"""

import tifffile as tp
from PIL import Image
from IMC_Denoise.IMC_Denoise_main.DIMR import DIMR
from IMC_Denoise.IMC_Denoise_main.DeepSNiF import DeepSNiF
from IMC_Denoise.DeepSNiF_utils.DeepSNiF_DataGenerator import DeepSNiF_DataGenerator



def IMC_Denoise_Predict(marker, weights_name, Raw_img_name, file, denoised_dir, training_dir,rawdir):
    weights_save_directory = training_dir # location where 'weights_name' will be loaded. 
    # If the value is None, the files will be loaded from the default directory.
    is_load_weights = True # read from the saved one.
    deepsnif = DeepSNiF(weights_name = weights_name,
                      weights_dir = weights_save_directory, 
                      is_load_weights = is_load_weights)
    
    Img_raw = tp.imread(rawdir+'/'+Raw_img_name)
    n_neighbours = 4 # Larger n enables removing more consecutive hot pixels. 
    n_iter = 3 # Iteration number for DIMR
    window_size = 3 # Slide window size. For IMC images, window_size = 3 is fine.
    Img_DIMR_DeepSNiF = deepsnif.perform_IMC_Denoise(Img_raw, n_neighbours = n_neighbours, n_iter = n_iter, window_size = window_size)
    sniffed = Image.fromarray(Img_DIMR_DeepSNiF)
    sniffed.save(denoised_dir+'/'+file)
    print('Denoised image of '+file+' created and saved at '+ Raw_img_name+'.')
    
    
def IMC_Denoise_Train_and_Predict(marker, Raw_img_name, file, denoised_dir, rawdir):
    # Release memory
    if 'generated_patches' in globals():
        del generated_patches
    
    channel_name = marker
    Raw_directory = rawdir
    Save_directory = "/Users/cjcurry/Documents/IMC_Pipeline/IMC_Denoise/Raw_IMC_dataset_all_training_data"# change this directory to your Raw_image_directory.
    
    n_neighbours = 4 # Larger n enables removing more consecutive hot pixels. 
    n_iter = 3 # Iteration number for DIMR
    window_size = 3 # Slide window size. For IMC images, window_size = 3 is fine.
    
    DataGenerator = DeepSNiF_DataGenerator(channel_name = channel_name, n_neighbours = n_neighbours, n_iter = n_iter, window_size = window_size)
    generated_patches = DataGenerator.generate_patches_from_directory(load_directory = Raw_directory)
    if DataGenerator.save_patches(generated_patches, save_directory = Save_directory):
        print('Data generated successfully!')
    
    print('The shape of the generated training set is ' + str(generated_patches.shape) + '.')
    
    train_epoches = 50 # training epoches, which should be about 200 for a good training result. The default is 200.
    train_initial_lr = 1e-3 # inital learning rate. The default is 1e-3.
    train_batch_size = 128 # training batch size. For a GPU with smaller memory, it can be tuned smaller. The default is 256.
    pixel_mask_percent = 0.2 # percentage of the masked pixels in each patch. The default is 0.2.
    val_set_percent = 0.15 # percentage of validation set. The default is 0.15.
    loss_function = "I_divergence" # loss function used. The default is "I_divergence".
    weights_name = 'weights_'+marker+'.hdf5' # trained network weights saved here. If None, the weights will not be saved.
    loss_name = None # training and validation losses saved here, either .mat or .npz format. If not defined, the losses will not be saved.
    weights_save_directory = None # location where 'weights_name' and 'loss_name' saved.
    # If the value is None, the files will be saved in a sub-directory named "trained_weights" of  the current file folder.
    is_load_weights = False # Use the trained model directly. Will not read from saved one.
    lambda_HF = 3e-6 # HF regularization parameter
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
    train_loss, val_loss = deepsnif.train(generated_patches)
    
    # read a raw image for this marker
    Img_raw = tp.imread(rawdir+'/'+Raw_img_name)
    Img_DIMR_DeepSNiF = deepsnif.perform_IMC_Denoise(Img_raw, n_neighbours = n_neighbours, n_iter = n_iter, window_size = window_size)
    sniffed = Image.fromarray(Img_DIMR_DeepSNiF)
    sniffed.save(denoised_dir+'/'+file)
    print('Denoised image of '+file+' created and saved at '+ Raw_img_name+'.')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    