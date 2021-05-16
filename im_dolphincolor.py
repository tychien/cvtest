import cv2
import numpy as np

#color = ((100,150,0),(140,255,255)) #blue
#color = ((0,120,70),(10,255,255)) #red
#color = ((16,59,0),(47,255,255)) #yellow
#color = ((104,0,0),(180,75,255))
#color = ((0,0,0),(180,255,255))
#color = ((0,20,0),(79,89,255))
#color = ((0,0,0),(84,164,255))
#color = ((110,31,45),(180,133,255)) # 0000.jpg 
color1 = ((117,12,32),(163,43,166)) # 1000.jpg
lower1 = np.array(color1[0], dtype="uint8")
upper1 = np.array(color1[1], dtype="uint8")

color2 = ((116,31,45),(180,133,255)) # 0000.jpg
lower2 = np.array(color2[0], dtype="uint8")
upper2 = np.array(color2[1], dtype="uint8")

color3 = ((116,0,63),(180,103,248)) # 0500.jpg
lower3 = np.array(color3[0], dtype="uint8")
upper3 = np.array(color3[1], dtype="uint8")

color4 = ((0,0,105),(180,57,181)) # 1200.jpg
lower4 = np.array(color4[0], dtype="uint8")
upper4 = np.array(color4[1], dtype="uint8")

image = cv2.imread('/home/tychien/cvtest/ChineseWhiteDolphin/train/VOCdevkit/VOC2018/JPEGImages/0423.jpg')
width, height, channel = image.shape

ratio = float(height) / float(width)
WIDTH = 840
HEIGHT = int(WIDTH/ratio)
image = cv2.resize(image,(WIDTH,HEIGHT))
    
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#hsv = cv2.GaussianBlur(hsv, (11,11),0)

mask1 = cv2.inRange(hsv, lower1, upper1)
mask1 = cv2.erode(mask1, None, iterations = 1)
mask1 = cv2.dilate(mask1, None, iterations = 1)

mask2 = cv2.inRange(hsv, lower2, upper2)
mask2 = cv2.erode(mask2, None, iterations = 1)
mask2 = cv2.dilate(mask2, None, iterations = 1)

mask3 = cv2.inRange(hsv, lower3, upper3)
mask3 = cv2.erode(mask3, None, iterations = 1)
mask3 = cv2.dilate(mask3, None, iterations = 1)

mask4 = cv2.inRange(hsv, lower4, upper4)
mask4 = cv2.erode(mask4, None, iterations = 1)
mask4 = cv2.dilate(mask4, None, iterations = 1)


mask = mask1 + mask2 + mask3 + mask4 

contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) >0:
    cnt = max(contours, key=cv2.contourArea)
    x,y,w,h = cv2.boundingRect(cnt)
    p1 = (x-2, y-2)
    p2 = (x+w+4, y+h+4)

    out = cv2.bitwise_and(image,image,mask=mask)
    cv2.putText(image, 'x={} ,y={}'.format(x+w/2,y+h/2),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
    cv2.rectangle(image, p1, p2, (0,255,255),2)
    cv2.rectangle(hsv, p1, p2, (0,255,255),2)
    #cv2.rectangle(out, p1, p2, (0,255,255),2)
    image = cv2.hconcat([image,hsv, out])
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()


