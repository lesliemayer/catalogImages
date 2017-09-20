import cv2
import logging
#from pyimagesearch.localbinarypatterns import LocalBinaryPatterns
from localbinarypatterns import LocalBinaryPatterns

class CloudFeatureHistogram:
    def __init__(self, doHSVhist=False):
        # store the number of points and radius
        #self.image = image
        self.doHSVhist = doHSVhist

        # initialize the local binary pattern descriptor
        self.desc = LocalBinaryPatterns(24, 8)

    def get_feature_histogram(self, image):
        # load the image, convert it to grayscale, describe it,
        # and classify it

        # TOO SMOOTH
        #filtered = cv2.bilateralFilter(image, 7, 75, 75)
        # Median blur : remove large outliers
        #filtered = cv2.medianBlur(image, 5)  DON'T DO THIS EITHER!!!
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)


        # Do a histogram equalization to bring out contrast
        # create a CLAHE object (Arguments are optional).
        # is this slow????  - NO, SOMETHING ELSE IS MAKING SLIDING WINDOWS SLOW...............
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        claheGray = clahe.apply(gray)

        # show the new image
        # cv2.imshow('claheGray', claheGray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # local binary pattern histogram
        lbpHist = self.desc.describe(claheGray)

        logging.debug("lbpHist = %s", lbpHist)

        # if self.doHSVhist :
        #
        #     # HSV histogram
        #     # channels = [0, 1] because we need to process both H and S plane.
        #     # bins = [180, 256] 180 for H plane and 256 for S plane.
        #     # range = [0, 180, 0, 256]
        #     # Hue value lies between 0 and 180 & Saturation lies between 0 and 256.
        #     hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
        #
        #     # hsvHistTest = cv2.calcHist([hsv], [1], None, [256], [0, 255])
        #     # cv2.normalize(hsvHistTest, hsvHistTest, 0, 255, cv2.NORM_MINMAX)
        #     #logging.debug("hsvHistTest = %s", hsvHistTest)
        #
        #     # only look at the saturation.  Saturation of white/gray < 0.15 * 255 = 38
        #     (hsvHist, _) = np.histogram(hsv[:,:,1].ravel(),
        #                              bins=np.arange(0, 255),
        #                              #bins=np.arange(0, 7),
        #                              range=(0, 255))
        #
        #     # normalize the histogram
        #     eps = 1e-7
        #     hsvHist = hsvHist.astype("float")
        #     hsvHist /= (hsvHist.sum() + eps)
        #
        #     logging.debug("hsvHist.sum() = %s", hsvHist.sum())
        #     logging.debug("hsvHist = %s", hsvHist)
        #
        #     # Now normalize hsvHist :
        #     # normalize the histogram
        #     # eps = 1e-7
        #     # hsvHist = hsvHist.astype("float")
        #     # hsvHist /= (hsvHist.sum() + eps)
        #
        #     #print "hsvHist = " + str(hsvHist)
        #     #print "hsvHist = " + str(hsvHist.flatten)
        #
        #
        # if self.doHSVhist:
        #     # Make a concatenated feature vector of color statistics and lbp
        #     # texture features
        #     # (horizontally stack the two numpy arrays) [1,2,3] [4,5,6]  ->  [1,2,3,4,5,6]
        #     hist = np.hstack([lbpHist, hsvHist])
        #
        #     #logging.debug("hist = %s", hist )

        #     return hist

        return lbpHist