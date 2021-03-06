#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 21:03:04 2019

@author: admin
"""

import tModel
import glob
import numpy as np
import cv2
import skimage
import re
import tFunctions as tFunc
# =============================================================================
import matplotlib.pyplot as plt
import scipy
from scipy import ndimage
# =============================================================================
num_px = 20
no_first_layer_units = num_px * num_px * 3 

def load_dataset(subset_selection, fileType, num_px):
    if re.search(subset_selection, "training, evaluation, validation") is None:
        raise SystemExit("ERROR: Please select training, evaluation or validation")
    if fileType != 'jpg':
        raise SystemExit("ERROR: Please select JPG only")
        
    train_set_x = []
    train_set_y = []
    
    print("INFO: Start to load dataset")
    
    folder_name = 'images/' + subset_selection
    folder_file_type_selection = folder_name + '/*.' + fileType
    
    for filename in glob.glob(folder_file_type_selection): #assuming jpg
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        try:
            my_image = skimage.transform.resize(image, output_shape=(num_px,num_px,3)).reshape((no_first_layer_units))
        except ValueError as e:
            print("Value Error: " + str(e))
            continue
        train_set_x.append(my_image)
        if filename.startswith(folder_name+'/1'):
            train_set_y.append(1)
        else:
            train_set_y.append(0)
            
    np_train_set_x = np.array(train_set_x).T
    print(np_train_set_x.shape)
    np_train_set_y = np.array(train_set_y).reshape(1, len(train_set_y))
    assert np_train_set_x.shape[0] == num_px*num_px*3, "An image should have " + str(num_px*num_px*3) + " pixels!"
    assert np_train_set_y.shape[0] == 1, "y should have shape (1, ..)"
    print(subset_selection + " dataset loaded successfully.")
    return np_train_set_x, np_train_set_y
   
    
X_train, Y_train = load_dataset('training','jpg',num_px)
Y_train = tFunc.one_hot_matrix(Y_train, 2)
Y_train = Y_train.reshape(2,3000)

X_vali, Y_vali = load_dataset('validation','jpg',num_px)
Y_vali = tFunc.one_hot_matrix(Y_vali, 2)
Y_vali = Y_vali.reshape(2,1000)

X_test, Y_test = load_dataset('evaluation','jpg',num_px)
Y_test = tFunc.one_hot_matrix(Y_test, 2)
Y_test = Y_test.reshape(2,1000)

units_per_layer = [num_px * num_px * 3, 500, 100, 80, 50, 40, 10, 2]

parameters = tModel.model(X_train, Y_train, X_test, Y_test, X_vali, Y_vali, units_per_layer, minibatch_size = 1000, num_epochs = 2000)



# =============================================================================
my_image = "0_122.jpg"
 
# We preprocess your image to fit your algorithm.
fname = "images/evaluation/" + my_image
image = np.array(cv2.imread(fname, cv2.IMREAD_COLOR))
my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
my_image_prediction = tFunc.predict(my_image, parameters, units_per_layer)

if my_image_prediction == 1:
    prediction_text = "Yes sir, it is food"
else:
    prediction_text = "It can't be food!"
 
plt.imshow(image)
print("Your algorithm predicts: y = " + str(np.squeeze(my_image_prediction)))
print(prediction_text)
# =============================================================================
