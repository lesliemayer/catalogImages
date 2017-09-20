import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from imutils import resize
from filelist import FileList  # import the filelist class
import logging
import argparse

# # for getting focal length from the photos database
from issimage import ISSIMAGE

# filename = r'C:\Users\lrmayer\Documents\Mayer\MyOpenCV_Code\Smallcoins.jpg'
# filename = r'F:\imagews\training\Earthlimb_ISS005-E-8536.jpg'  # perfect for learning
#filename = r'F:\imagews\training\Earthlimb_ISS009-E-23413.jpg'
#filename = r'F:\imagews\training\Earthlimb_ISS009-E-28843.jpg'
# filename = r'F:\imagews\training\Land_ISS009-E-22319.jpg'  # dark part is window, not limb
# filename = r'F:\imagews\training\Night_ISS028-E-26603.jpg'


# python find_limb_part2.py E:\BetterLightning --log=debug --list="E:\BetterLightning\lightning.txt"
# python find_limb_part2.py F:\imagews\training --log=debug --list="F:\imagews\training\earthlimb.txt"
# python find_limb_part2.py F:\imagews\training --log=debug --list="F:\imagews\training\various.txt"
# python find_limb_part2.py F:\imagews\training --log=debug --list="F:\imagews\training\aurora.txt"
# python find_limb_part2.py F:\imagews\training --log=debug --list="F:\imagews\training\list.txt"


# -------------------------------------------
# Thresholding for finding where the limb is
# -------------------------------------------
doThreshold = False
threshold = 50

# -------------------------------------------------
# Get rid of small bright features (stars,  noise)
# -------------------------------------------------
doOpening = True

# -------------------------------------------------
# Get rid of small bright features (stars,  noise)
# -------------------------------------------------
doClosing = True


# -----------------------------------------------------
# Construct the argument parse and parse the arguments
# -----------------------------------------------------
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser(description="Find earth limb in images")
ap.add_argument("dataset", help="Path to images")  # this is required

# Add logging file argument
ap.add_argument("-l", "--log", help="Logging Value", default="info")

# Add list file argument
ap.add_argument("-li", "--list", help="List of images to read")

# parse the arguments
args = ap.parse_args()

# -------------------------------------------------------------
# Set up logging file
# -------------------------------------------------------------
# loglevel is bound to the string value obtained from the
# command line argument. Convert to upper case to allow the user to
# specify --log=DEBUG or --log=debug
# -------------------------------------------------------------
numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level, filename='find_limb_part2.log', filemode='w')


# -------------------------------------
# Get the list of image names to read
# -------------------------------------
theList = FileList(args.dataset,  args.list)
imagePaths = theList.getPathFilenames()

logging.info("imagePath is %s", imagePaths)

# --------------------------------------
# Loop over the input dataset of images
# --------------------------------------
for filename in imagePaths:

    if args.list :
        if not os.path.isfile(filename) :
               sys.exit("filename " + filename + "  does not exist")

        # Read image
        img = cv2.imread(filename)

        # resize the image
        # def resize(image, width = None, height = None, inter = cv2.INTER_AREA)
        resized = resize(img, width=500)

        # initialize ISSIMAGE class for setting up the image
        xx = ISSIMAGE(filename)

        xx.resize()

        xx.show()

        # ----------------------
        # Get the sun elevation
        # ----------------------
        sunElev = xx.get_sun_elev()
        logging.debug("Sun elevation = %s", sunElev)

        # ----------------------
        # Get the focal length
        # ----------------------
        focalLength = xx.get_focal_length()
        logging.debug("Focal length = %s", focalLength)


        # -----------------
        # convert to gray
        # -----------------
        gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)

        # Do histogram equalization ??? (only needed for night time limb)
        # equalize the histogram of the image
        eq = cv2.equalizeHist(gray)
        cv2.imshow("histogram of open/close", eq)
        #closed = eq.copy()


        # ------------------------------------------------------
        # Smooth the image
        # nn = the neighborhood size
        # For finding the limb, want the image to be very smooth
        # -------------------------------------------------------
        nn = 11  # Get less edges w/ higher n
        #nn = 5
        #gray = cv2.GaussianBlur(gray, (nn, nn), 0)

        # -----------------------------------------------
        # Bilateral filtering preserves the edges
        # 2nd parameter is the window size for smoothing
        # -----------------------------------------------
        #filtered = cv2.bilateralFilter(gray,9,75,75)
        filtered = cv2.bilateralFilter(gray,19,75,75)

        cv2.imshow("bilateral filter", filtered)



        # ==================================================================
        # Do an opening to get rid of more noise (the small bright areas)
        # ==================================================================
        if (doOpening):
            #kernel = np.ones((3, 3), np.uint8)
            kernel = np.ones((9, 9), np.uint8)
            #kernel = np.ones((19, 19), np.uint8)  # to big for night images
            opened = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
        else:
            opened = filtered.copy()

        # ---------------------------------------
        # Do closing to get of small dark spots
        # ---------------------------------------
        if (doClosing):
            #kernel = np.ones((3, 3), np.uint8)
            #kernel = np.ones((9, 9), np.uint8)
            #kernel = np.ones((19, 19), np.uint8)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        else:
            closed = opened.copy()

        cv2.imshow("opened/closed", closed)


        # ---------------------------------------------------------------------------------------------
        # Show the gradient image (for testing whether this is a viable method for getting night limb)
        # ---------------------------------------------------------------------------------------------
        kernel = np.ones((3, 3), np.uint8)
        gradient = cv2.morphologyEx(closed, cv2.MORPH_GRADIENT, kernel)
        cv2.imshow("gradient of opened/closed", gradient)


        # ---------------------
        # Threshold the image
        # ---------------------
        if (doThreshold) :

            if (sunElev > 10) :
                # image needs to be 1D for threshold function
                # Simple, binary thresholding
                #ret, thresh = cv2.threshold(opened, 100, 255, cv2.THRESH_BINARY)  # not bad, but may be too high
                # pretty good, but not good w/ very bright limb images : Earthlimb_ISS009-E-16194.jpg - Earthlimb_ISS009-E-16199.jpg
                # May need to figure out peaks of bimodal color histogram on the gray image or something like that

                logging.debug("threshold = %s", threshold)
                ret, thresh = cv2.threshold(closed, threshold, 255, cv2.THRESH_BINARY)

            elif (sunElev < -30. and sunElev > -70.) :

                #threshold = 75  # to get the bright limb  # too low
                #threshold = 100  # to get the bright limb # too high
                #threshold = 90  # too high
                #threshold = 85 # too high
                threshold = 80
                #logging.debug("threshold = %s", threshold)
                # this global thresholding not really working b/c of variable lighting
                #ret, thresh = cv2.threshold(closed, threshold, 255, cv2.THRESH_BINARY)

                # adaptive gaussian thresholding
                logging.debug("Adaptive Gaussian threshold")
                nn = 11  # not good - too many, lots of them dots
                nn = 5  # better, but only gets the really big contrasts
                nn = 3  # same as above
                #nn = 9  # not sure why there is a bunch of dot contours above limb
                #thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, 2)
                thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, 10)
                #  This only gets the egdes that are very big in contrast (very dark next to very light)
                #thresh = cv2.adaptiveThreshold(closed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, nn, -10)
                #ret, thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)\

            else:

                logging.debug("binary + otsu threshold")
                ret, thresh = cv2.threshold(closed,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)




        else:
            thresh = opened.copy()   # gives too many contours

        #cv2.imshow("threshold", thresh)


        # ---------------------------------------------------------------
        # compute edges on the smoothed image
        # any gradient values below 30 are considered
        # non-edges whereas any values above 150 are considered
        # sure edges.
        # ----------------------------------------------------------------
        edgeThresh1 = 30
        edgeThresh2 = 50  # use for thresholded day limb


        # too many contours when sun elev is high (by night standards)
        # no contours in very low sun elev : -76
        edgeThresh1 = 50
        edgeThresh2 = 100  # alot of contours, but maybe its ok, as long as it gets the limb


        #edgeThresh2 = 200  # not enough
        #edgeThresh2 = 150  # not enough
        #edgeThresh2 = 150  # good for city lights

        edged = cv2.Canny(thresh, edgeThresh1, edgeThresh2)  # use for day limb

        # run the canny edge detection on smoothed image
        #                image, threshold1, threshold2
        # Any gradient value larger than threshold2 is considered
        # to be an edge. Any value below threshold1 is considered
        # not to be an edge. Values in between threshold1
        # and threshold2 are either classified as edges or non-edges
        # based on how their intensities are 'connected'
        # threshold1 = 30
        # threshold2 = 150
        # canny = cv2.Canny(image, threshold1, threshold2)
        # cv2.imshow("Canny 1", canny)
        # cv2.waitKey(0)



        cv2.imshow("Edges", edged)

        # find the contours of the edges. cnts is the returned contours
        # This method returns
        # a 3-tuple of: (1) our image after applying contour detection
        # (which is modified and essentially destroyed), (2) the
        # contours themselves, cnts, and (3) the hierarchy of the contours
        # (OpenCV 3.0 is different from OpenCV 2.4, which returns a tuple of 2)
        # This function is destructive
        # to the image you pass in. If you intend using that image
        # later on in your code, it's best to make a copy of it, using
        # the NumPy copy method.
        # The second argument is the type of contours we want.
        # We use cv2.RETR_EXTERNAL to retrieve only the outermost
        # contours (i.e., the contours that follow the outline of the
        # coin). We can also pass in cv2.RETR_LIST to grab all contours.
        # Other methods include hierarchical contours using
        # cv2.RETR_COMP and cv2.RETR_TREE, but hierarchical contours
        # are outside the scope of this book.
        # of resources.
        # Our contours cnts is simply a Python list. We can use
        # the len function on it to count the number of contours that
        # were returned.
        (_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)



        # draw the contours in green on the coins image
        # contour index of -1 means draw all contours.  If just
        # wanted to draw ith contour, just enter i
        # The last argument is the thickness of the line we
        # are drawing. We'll draw the contour with a thickness of
        # two pixels.
        # cv2.drawContours(resized, cnts, -1, (0, 255, 0), 2)
        # cv2.imshow("contours", resized)

        # See :
        # http://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html
        # for information about contour characterics (used below, like getting bounding rectangle)

        green = (0, 255, 0)
        red = (0, 0, 255)
        yellow = (0, 255, 255)

        # write number of contours on the image
        numContours = len(cnts)

        # loop over contours
        for (i, c) in enumerate(cnts):

            #logging.info("\nContour #%s",format(c))
            logging.info("\nContour #%s", c)

            # -------------------------------------------------------------------------------------------
            # Straight Bounding Rectangle :
            # A straight rectangle, it
            # doesn't consider the rotation of the object. So area of the bounding rectangle won't be
            # minimum. It is found by the function sget the bounding rectangle
            # -------------------------------------------------------------------------------------------
            (x, y, w, h) = cv2.boundingRect(c)
            #print("x,y,w,h : {} {} {} {} ".format(x,y,w,h))

            # get the aspect ratio
            aspect_ratio = float(w) / float(h)
            #print("aspect_ratio : {}".format(aspect_ratio))
            logging.info("aspect ratio : %12.5f",aspect_ratio)

            # get extent : Extent is the ratio of contour area to bounding rectangle area.
            # extent = object area/bounding rectangle area
            area = cv2.contourArea(c)  # get the contour area
            logging.info("contour area : %12.5f", area)
            rect_area = w * h
            extent = float(area) / rect_area
            logging.info("extent : %12.5f", extent)

            # ------------------------------------------------------------------------------------
            # Get the minimum closing circle that completely covers the object with minimum area.
            # ------------------------------------------------------------------------------------
            (x, y), radius = cv2.minEnclosingCircle(cnts[i])
            center = (int(x), int(y))
            radius = int(radius)
            #cv2.circle(resized, center, radius, (0, 255, 255), 2)
            logging.info("x,y, radius of min circle : %s %s %12.3f", x, y, radius)


            # Rotated Rectangle :
            # The bounding rectangle is drawn
            # with minimum area, so it considers the rotation also.  The function used is cv2.minAreaRect().
            # It returns a Box2D structure which contains following detals - ( center (x, y), (width, height),
            # angle of rotation ).But to draw this rectangle, we need 4 corners of the rectangle.
            # It is obtained by the function cv2.boxPoints()

            rect = cv2.minAreaRect(cnts[i])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(resized, [box], 0, (0, 255, 255), 2)

            if  (area < 1.) :
            #if (area == 0.):
                cv2.drawContours(resized, cnts, i, red, 2)
            else:
                cv2.drawContours(resized, cnts, i, green, 2)

            logging.info("-----------------------")

        cv2.putText(resized, str(numContours) + ' contours', (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow("contours", resized)
        cv2.waitKey(0)










# # noise removal
# kernel = np.ones((3,3),np.uint8)
# opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
#
# # sure background area
# sure_bg = cv2.dilate(opening,kernel,iterations=3)
#
# # Finding sure foreground area
# dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
# ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
#
# # Finding unknown region
# sure_fg = np.uint8(sure_fg)
# unknown = cv2.subtract(sure_bg,sure_fg)
#
# # Marker labelling
# ret, markers = cv2.connectedComponents(sure_fg)
#
# # Add one to all labels so that sure background is not 0, but 1
# markers = markers+1
#
# # Now, mark the region of unknown with zero
# markers[unknown==255] = 0
#
# #markers = cv2.watershed(img,markers)
# #img[markers == -1] = [255,0,0]
#
# markers = cv2.watershed(resized,markers)
# resized[markers == -1] = [255,0,0]

#cv2.imshow("watershed", resized)
#cv2.waitKey(0)