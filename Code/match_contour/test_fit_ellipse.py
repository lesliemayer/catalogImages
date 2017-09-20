""" Python Code to read in an image and match it w/ contour of another image
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

# cv2.imshow("thresh1", thresh1)
# cv2.imshow("thresh2", thresh2)
# cv2.waitKey(0)

# Get contour of 1st image
#contours = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
contours = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
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
#cv2.imshow("1st contour", img1)

cv2.drawContours(img2, [cnt2], 0, green, 2)
#cv2.imshow("2nd contour", img2)

# Fit an ellipse to the contours
ellipse = cv2.fitEllipse(cnt1)
# this is a tuple (center, size, angle)
# (x_centre,y_centre),(minor_axis,major_axis),angle
print "Ellipse 1 : {}".format(ellipse)

# Draw the ellipse on the image
cv2.ellipse(img1,ellipse,(255,255,0),2)
cv2.imwrite("fitellipse1.jpg", img1)


cv2.imshow("ellipse fit 1", img1)

# Fit an ellipse to the contours
ellipse = cv2.fitEllipse(cnt2)

# Draw the ellipse on the image
cv2.ellipse(img2,ellipse,(255,255,0),2)

cv2.imshow("ellipse fit 2", img2)

# draw the minimum enclosing circle
# THIS DOES NOT FOLLOW LIMB, JUST DRAWS A CIRCLE AROUND IT
# (x,y),radius = cv2.minEnclosingCircle(cnt1)
# center = (int(x),int(y))
# radius = int(radius)
# cv2.circle(img1,center,radius,(160,250,0),2)
#
# cv2.imshow("circle fit 1", img1)

# RotatedRect temp = minAreaRect(Mat(contours[i]))

# Get the convex hull surrounding limb
hull1 = cv2.convexHull(cnt1)

# Draw the hull
cv2.drawContours(img1, [hull1], 0, (100,100,100), 2)
cv2.imshow("hull 1", img1)

# Get the convex hull surrounding limb
hull2 = cv2.convexHull(cnt2)

# Draw the hull
cv2.drawContours(img2, [hull2], 0, (100,100,100), 2)
cv2.imshow("hull 2", img2)

# get momemts of the hulls
print
print "Moments of cnt1, cnt2 : "
print cv2.moments(hull1)
print cv2.moments(hull2)
print

print "Hu moments of hull1, hull2"
print cv2.HuMoments(cv2.moments(hull1)).flatten()
print cv2.HuMoments(cv2.moments(hull2)).flatten()

# Run match shapes on the hulls
#ret = cv2.matchShapes(hull1,hull2,1,0.0)
ret = cv2.matchShapes(hull1,hull2,1,0.0)
#ret = cv2.matchShapes(cnt1,cnt2, cv2.CV_CONTOURS_MATCH_I1,  0.0)
print
print "Result of matchShapes on hull1, hull2 : "
print ret

#img3 = cv2.imread('star1.jpg')
img3 = cv2.imread(r'E:\Lightning\SmallISS030-E-228216.jpg')
gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray3", gray3)
thresh3 = cv2.threshold(gray3, 127, 255, cv2.THRESH_BINARY)[1]

# Get contour of 1st image
#contours = cv2.findContours(thresh3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
contours = cv2.findContours(thresh3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
cnt3 = contours[0]

print ("img3 : Length of contours = {}".format(len(contours)))



#cv2.drawContours(img3, [cnt3], -1, (100,200,100), 2)
cv2.drawContours(img3, contours, -1, (100,200,100), 2)
cv2.imshow("largest contour star", img3)

ret = cv2.matchShapes(hull1,cnt3,1,0.0)
#ret = cv2.matchShapes(cnt1,cnt2, cv2.CV_CONTOURS_MATCH_I1,  0.0)
print
print "Result of matchShapes on hull1, cnt3 : "
print ret

cv2.waitKey(0)


