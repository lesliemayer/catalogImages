"""Blob Detection Class - find blobs in an image"""





# Standard imports
# import sys
# import os
import cv2
import numpy as np
# import argparse
import logging
# from imutils import resize
# from filelist import FileList  # import the filelist class
# from filelist import get_filename
# from issimage import ISSIMAGE

# ===================================================================
# Define the cylinder Class
# ===================================================================
class BLOBDETECT:
    """Blob detection object
     Attributes:
         type : type of object (box, etc)
         outerRads : the list of outer radii
         innermostRad : the inner most radius
         laero : length of the object
         haero : height of the object
     """

    # Initialize the object
    def __init__(self, params):

        """Return a new BLOBDETECT object"""

        self.params = params

        # # make sure values are valid - add assert in later????
        # assert innermostRad >= 0.0, "innermostRad < 0 !! : %d" % innermostRad
        # assert self.is_valid(), "outerRads not valid !! "

        # Set up the detector with parameters.
        self.detector = cv2.SimpleBlobDetector_create(params)


        # Write parameters to logging file
        logging.info("------------------------- Simple Blob Detection Parameters -------------------------------------")
        logging.info("min, max Threshold = %s %s", params.minThreshold, params.maxThreshold)

        if (params.filterByArea):
            logging.info("min, max Area = %s %s", params.minArea, params.maxArea)

        if (params.filterByCircularity):
            logging.info("min, max Circularity = %s %s", params.minCircularity, params.maxCircularity)

        if (params.filterByConvexity):
            logging.info("min, max Convexity = %s %s", params.minConvexity, params.maxConvexity)

        if (params.filterByInertia):
            logging.info("min, max Inertia = %s %s", params.minInertiaRatio, params.maxInertiaRatio)

        logging.info("Filter by color = %s", params.filterByColor)

        logging.info("Blob color = %s", params.blobColor)
        logging.info("-------------------------------------------------------------------------------------------------")

    def detect_blobs(self,image):
        # Detect blobs.
        self.keypoints = self.detector.detect(image)


    def get_keypoints_xy(self, roundXY=False):
        """return list of (x,y) tuples of the keypoints"""
        xyList = []
        for keyPoint in self.keypoints:
            x = keyPoint.pt[0]
            y = keyPoint.pt[1]
            if roundXY:
                x = int(round(x))
                y = int(round(y))
            xyList.append((x,y))

        return xyList

    def get_keypoint_xy(self, keypoint, roundXY=False):
        """return (x,y) tuples of a keypoint"""
        x = keyPoint.pt[0]
        y = keyPoint.pt[1]
        if roundXY:
            x = int(round(x))
            y = int(round(y))
        return (x,y)


    def print_keypoints(self, image):
        """print out the keypoints"""

        # print out the keypoints positions
        # for key in keypoints :
        #     # x = keypoints[i].pt[0]  # i is the index of the blob you want to get the position
        #     # y = keypoints[i].pt[1]
        #     logging("keypoint : %s %s", key.pt[0], key.pt[1])

        #logging("keypoint : %s", keypoints[0].pt[0])
        # x = keypoints[0].pt[0]
        # logging.debug("keypoint : %s", x)
        # Size is the diameter size!  not the area
        # logging.debug("keypoint : %s", keypoints[0].size())

        for keyPoint in self.keypoints:
            y = keyPoint.pt[1]
            x = keyPoint.pt[0]
            s = keyPoint.size
            logging.debug("keypoint x,y, diameter size : %s %s %s", x, y, s)

            # Get color or nearest pixel to x,y
            ix = int(x)
            iy = int(y)

            # get the blue, green, red components of pixel[0,0]
            (h, s, v) = image[iy, ix]
            logging.debug("pixel value h, s, v : %s %s %s", h, s, v)

            logging.debug("----------------------------------------------")


    def draw_keypoints(self, image):
        # --------------------------------------------------------------------------------
        # Draw detected blobs as green circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle
        # corresponds to the size of blob
        # ---------------------------------------------------------------------------------
        im_with_keypoints = cv2.drawKeypoints(image, self.keypoints, np.array([]), (0, 255, 0),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return im_with_keypoints


    #def draw_contours
        # draw contours around keypoints - NOT SURE IF THIS WORKS?
        # cv2.drawContours(im, keypoints, -1, (0, 255, 0), 3)



