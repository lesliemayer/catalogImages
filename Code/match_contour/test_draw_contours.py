"""Python Code to read in an image and draw a line on it
   Written by L.R. Mayer 2017"""



import numpy as np  # for defining the kernel
import cv2


green = (0,255,0)

#img1 = cv2.imread('star.jpg',0)
#img1 = cv2.imread('C:\Users\lrmayer\Documents\Mayer\CatalogImages\Code\limb_edge\limb_edge_fl28_iss3628.jpg',0)

img1 = cv2.imread(r'E:\Lightning\SmallISS030-E-228233.jpg',0)

cv2.line(img1, (0,0), (300,300), green, 10) # not sure why this isn't working

cv2.imshow("img1", img1)


canvas = np.zeros((300,300,3), dtype = "uint8")

cv2.line(canvas, (0,0), (300,300), green, 10)

cv2.imshow("Canvas", canvas)

cv2.waitKey(0)
