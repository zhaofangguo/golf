import cv2 as cv
import numpy as np
img = cv.imread('images/robot2.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('test', img)
img = np.array([img])
print img[0, 100, 189]

cv.waitKey(0)