"""Reads in an image of a star, and an earth limb edge, gets the contours and draws them,
gets the contour approximation of the contours using the Douglas-Peucker algorithm, calculates
the moments of the contours, used the moments to see if the contour shapes match, gets the
most extreme points along the contour, and draws a line connecting the extreme left and right points.

Written by L.R. Mayer"""


import numpy as np  # for defining the kernel
import cv2

green = (0,255,0)


#img1 = cv2.imread('star.jpg',0)  if put optional 0 on end, will not draw color, only black,
#img1 = cv2.imread('C:\Users\lrmayer\Documents\Mayer\CatalogImages\Code\limb_edge\limb_edge_fl28_iss3628.jpg')
img1 = cv2.imread('star1.jpg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread(r'C:\Users\lrmayer\Documents\Mayer\CatalogImages\Code\limb_edge\limb_edge_fl28.jpg')
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


#cv2.imshow("img1", img1)
#cv2.imshow("img2", img2)


thresh1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)[1]
thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("thresh1", thresh1)
cv2.imshow("thresh2", thresh2)
cv2.waitKey(0)


#(_,contours,hierarchy) = cv2.findContours(thresh,2,cv2.CHAIN_APPROX_SIMPLE)
contours = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
print ("img1 : Length of contours = {}".format(len(contours)))
cnt1 = contours[0]
# Get contour length
# Second argument specify whether shape is a closed contour (if passed True), or just a curve.
perimeter1 = cv2.arcLength(cnt1,False)
print "length of cnt1 = {}".format(perimeter1)

# get approximation of contour 1 (remove small curves)
# See : http://opencvpython.blogspot.com/2012/06/contours-2-brotherhood.html  Contour Approximation
approx1 = cv2.approxPolyDP(cnt1,0.1*cv2.arcLength(cnt1,True),True)

(_,contours,hierarchy) = cv2.findContours(thresh2,2,cv2.CHAIN_APPROX_SIMPLE)
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

approx2 = cv2.approxPolyDP(cnt2,0.1*cv2.arcLength(cnt2,True),True)

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

print "Hu moments of approx1, approx2"
print cv2.HuMoments(cv2.moments(approx1)).flatten()
print cv2.HuMoments(cv2.moments(approx2)).flatten()


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



# Very long....
# print "cnt1 = "
# print cnt1
# print "cnt2 = "
# print cnt2

print "approx2 = "
print approx2

print "type of cnt1 : "
print type(cnt1)

print "size of cnt1 : {}".format(cnt1.size)
print "shape of cnt1 : {}".format(cnt1.shape)

# determine the most extreme points along the contour
extLeft = tuple(cnt1[cnt1[:, :, 0].argmin()][0])
extRight = tuple(cnt1[cnt1[:, :, 0].argmax()][0])

print "extreme left, right points of cnt1 : "
print extLeft, extRight

# Draw line on binary image from extreme left to right
#cv2.line(thresh, extLeft, extRight, green)
cv2.line(thresh1, (0,0), (300,300), green)

# show the new image
cv2.imshow("new drawn closed contour",thresh1)

# Get contour of new image w/ line drawn

# Get hu moments of new closed contour

# Draw the closed contour


cv2.waitKey(0)
