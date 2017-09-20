'''
Created on Sep 26, 2016

@author: lrmayer
'''

# import necessary packages
import numpy as np
import cv2
import mahotas

# ========================================================================
# Quantify the image using HSV color mean, standard deviation, and texture
# ========================================================================
class HSVColorTexture :
    def __init__(self):
        # Initialize the object
        pass  # do nothing

    # ------------------------------------------------------------------------------------------
    # Describe the image
    # Uses the mean, std of the HSV colors, and the haralick texture features as the descriptor
    # ------------------------------------------------------------------------------------------
    def describe(self, image):
        # extract the mean and standard deviation from each
        # channel of image in HSV color space

        # ----------------------------------------------------------------------------------------------
        # Convert image to HSV color space, then compute the mean & stand. dev. for each channel - lrm
        # Why is HSV color used here ???? Why use mean & std?
        # ----------------------------------------------------------------------------------------------
        (means, stds) = cv2.meanStdDev(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
        # concatenate : Join a sequence of arrays along an existing axis. returns a ndarray - lrm
        # np.ndarray.flatten : Return a copy of the array collapsed into one dimension.
        colorStats = np.concatenate([means, stds]).flatten()

        # extract Haralick texture features
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        haralick = mahotas.features.haralick(gray).mean(axis=0)

        # return a concatenated feature vector of color statistics and Haralick
        # texture features
        # (horizontally stack the two numpy arrays) [1,2,3] [4,5,6]  ->  [1,2,3,4,5,6]
        return np.hstack([colorStats, haralick])


# ------------------------------------------------------------------------------------------------------------
