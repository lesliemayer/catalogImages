"""Class to help with HSV color blocking"""

import logging
import numpy as np
import cv2


class HSVCOLORBLOCK :

    def __init__(self, image, lower=[0,0,0], upper=[255,255,255]) :

        # The lower and upper boundarys of the color we are searching for
        self.lower = np.array(lower, dtype = "uint8")
        self.upper = np.array(upper, dtype = "uint8")

        # Convert the image to HSV color space
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Binary image of the parts of the image that fall in this color range
        # 1 = yes, 0 = no
        self.binary = cv2.inRange(self.image, lower, upper)

        # % of image that falls into this color bin
        self.percent = 0  # initilize to 0


    # Get the % of image that falls into this color bin
    def get_percent(self):

        # Get the total number of pixels in the binary image
        totalPix = self.binary.shape[0] * self.binary.shape[1]
        logging.debug("total Pixels in resized image : %s * %s = %s", self.binary.shape[1], self.binary.shape[0], totalPix)

        # For testing, create array of all 1's
        #nonZero = np.count_nonzero(np.ones((self.binary.shape[0], self.binary.shape[1])))

        # Get number of non-zero pixels :
        nonZero = np.count_nonzero(self.binary)
        logging.debug("Number of non-zero pixels in binary array : %s", nonZero)

        # Calcuate the percentage from the non zero pixels
        self.percent = (float(nonZero) / float(totalPix)) * 100.
        logging.debug("Percent of color %s", self.percent)

        return self.percent


    # Get the largest contour that surrounds the color
    def get_largest_contour(self):

        # initialize cnt
        cnt = None

        # find contours in the thresholded image
        # cv2.findContour function is destructive to the NumPy array that is passed in.
        (_, cnts, _) = cv2.findContours(self.binary.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        # check to see if any contours were found
        if len(cnts) > 0 :
            # sort the contours and find the largest one
            # Larger contours in front of list, grab the one w/ largest area,
            # assuming this is the outline of the phone.
            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        return cnt
