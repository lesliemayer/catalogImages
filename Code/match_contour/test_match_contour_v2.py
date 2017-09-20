"""Reads in two images that have already been thresholded,
   gets the contours and contour lengths, draws the contours,
   computes the moments, and matches the shapes of the contours.

   Written by L.R. Mayer
"""


import numpy as np  # for defining the kernel
import cv2

green = (0,255,0)

img1 = cv2.imread(r'limb_edge_fl28_iss3628.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread(r'limb_edge_fl28.jpg')
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Threshold the images
thresh1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)[1]
thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("thresh1", thresh1)
cv2.imshow("thresh2", thresh2)
cv2.waitKey(0)

# Get contour of 1st image
contours = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
print ("img1 : Length of contours = {}".format(len(contours)))

cnt1 = contours[0]
# Get contour length
# Second argument specify whether shape is a closed contour (if passed True), or just a curve.
perimeter1 = cv2.arcLength(cnt1,False)
print "length of cnt1 = {}".format(perimeter1)

contours = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
print ("img2 : Length of contours = {}".format(len(contours)))
cnt2 = contours[0]
# Get contour length
# Second argument specify whether shape is a closed contour (if passed True), or just a curve.
perimeter2 = cv2.arcLength(cnt2,False)
print "length of cnt2 = {}".format(perimeter2)
print

# draw contours found
cv2.drawContours(img1, [cnt1], 0, green, 2)
cv2.imshow("1st contour", img1)

cv2.drawContours(img2, [cnt2], 0, green, 2)
cv2.imshow("2nd contour", img2)


# print out hu moments of each contour
print "Hu moments of thresh, thresh2"
print cv2.HuMoments(cv2.moments(thresh1,binaryImage=True)).flatten()
print cv2.HuMoments(cv2.moments(thresh2,binaryImage=True)).flatten()
print
print "Hu moments of cnt1, cnt2"
print cv2.HuMoments(cv2.moments(cnt1)).flatten()
print cv2.HuMoments(cv2.moments(cnt2)).flatten()
print "Area of countours1, 2 :"
print cv2.contourArea(cnt1), cv2.contourArea(cnt2)

print
print "Moments of cnt1, cnt2 : "
print cv2.moments(cnt1)
print cv2.moments(cnt2)
print

ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
#ret = cv2.matchShapes(cnt1,cnt2, cv2.CV_CONTOURS_MATCH_I1,  0.0)
print
print "Result of matchShapes on cnt1, cnt2 : "
print ret
print

cv2.waitKey(0)
