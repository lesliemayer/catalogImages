import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)

name = 'HSV color space'
cv2.namedWindow(name)

# create trackbars for color change
cv2.createTrackbar('H',name,0,179,nothing)
cv2.createTrackbar('S',name,0,255,nothing)
cv2.createTrackbar('V',name,0,255,nothing)

# create switch for ON/OFF functionality
#switch = '0 : OFF \n1 : ON'
#cv2.createTrackbar(switch, name,0,1,nothing)

while(1):
    cv2.imshow(name,img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    h = cv2.getTrackbarPos('H',name)
    s = cv2.getTrackbarPos('S',name)
    v = cv2.getTrackbarPos('V',name)
    #sw = cv2.getTrackbarPos(switch,name)

    # if sw == 0:
    #     img[:] = 0
    # else:
    #img[:] = [h,s,v]
    img[:] = [h,s,v]
    # convert to rgb space
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

cv2.destroyAllWindows()