"""对图片进行反色"""
import numpy as np
import cv2

img = cv2.imread('good.jpg')

height = img.shape[0]
width  = img.shape[1]

negative_file = np.zeros((height, width, 3))

b,g,r = cv2.split(img)

r = 255 - r
b = 255 - b
g = 255 - g

negative_file[:,:,0] = b
negative_file[:,:,1] = g
negative_file[:,:,2] = r

print(negative_file)
cv2.imwrite("negative_good.jpg", negative_file)