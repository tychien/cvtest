import cv2
import numpy as np

#color = ((100,150,0),(140,255,255)) #blue
#color = ((0,120,70),(10,255,255)) #red
#color = ((16,59,0),(47,255,255)) #yellow
color = ((104,0,0),(180,75,255))
lower = np.array(color[0], dtype="uint8")
upper = np.array(color[1], dtype="uint8")

image = cv2.imread('/home/tychien/cvtest/dolphin5.jpeg')
width, height, channel = image.shape

ratio = float(height) / float(width)
WIDTH = 600
HEIGHT = int(WIDTH/ratio)
image = cv2.resize(image,(WIDTH,HEIGHT))
    
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hsv = cv2.GaussianBlur(hsv, (11,11),0)

mask = cv2.inRange(hsv, lower, upper)
mask = cv2.erode(mask, None, iterations = 2)
mask = cv2.dilate(mask, None, iterations = 2)
    
contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) >0:
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    p1 = (x-2, y-2)
    p2 = (x+w+4, y+h+4)

    out = cv2.bitwise_and(hsv,hsv,mask=mask)
    cv2.putText(image, 'x={} ,y={}'.format(x+w/2,y+h/2),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
    cv2.rectangle(image, p1, p2, (0,255,255),2)
    cv2.rectangle(hsv, p1, p2, (0,255,255),2)
    cv2.rectangle(out, p1, p2, (0,255,255),2)
    image = cv2.hconcat([image,hsv, out])
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()


