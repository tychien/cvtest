import cv2 
import numpy as np 

color = ((115,0,47),(180,152,255))
lower = np.array(color[0],dtype="uint8")
upper = np.array(color[1],dtype="uint8") 



image = cv2.imread('IMG_7819.JPG')
width, height, channel = image.shape
ratio = float(width)/float(height) 
#image = cv2.resize(image,(1024,int(1024*ratio)))


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
hsv = cv2.GaussianBlur(hsv,(13,13),0)

mask = cv2.inRange(hsv, lower, upper) 
mask = cv2.erode(mask, None, iterations = 2)
mask = cv2.dilate(mask, None, iterations = 2) 

edged = cv2.Canny(mask,20,40)
contours,hierarchy= cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
#out = edged.copy()
#out =  image.copy()
#out.fill(0)
out = cv2.bitwise_and(image,image,mask=mask)

#cv2.drawContours(out,contours,-1,(0,255,255),1)
image = cv2.resize(image,(1024,int(1024*ratio)))
out = cv2.resize(out,(1024,int(1024*ratio)))
image = cv2.hconcat([image,out])
cv2.imshow('frame',image) 
cv2.waitKey(0)
cv2.destroyAllWindows() 
