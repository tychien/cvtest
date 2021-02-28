import cv2
import numpy as np

color = ((0,0,0),(50,50,50))
lower = np.array(color[0], dtype="uint8")
upper = np.array(color[1], dtype="uint8")

cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    cap.open()

while (True):

    ret, frame = cap.read()
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (11,11),0)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) >0:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) < 100:
            continue
        x,y,w,h = cv2.boundingRect(cnt)
        p1 = (x-2, y-2)
        p2 = (x+w+4, y+h+4)

        out = cv2.bitwise_and(hsv,hsv,mask=mask)
        cv2.rectangle(frame, p1, p2, (0,255,255),2)
        cv2.rectangle(hsv, p1, p2, (0,255,255),2)
        cv2.rectangle(out, p1, p2, (0,255,255),2)
        frame = cv2.hconcat([frame,hsv, out])
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) ==27:
        cv2.destroyAllWindows()
        break

'''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9,9),0)
    edged = cv2.Canny(gray, 50, 150)
    edged = cv2.dilate(edged, None, iterations=3)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    print('Num. of Contours = '+ str(len(contours)))
    print('Contours[0]:'+str(len(contours[0])))

    for n in contours:
        approx = cv2.approxPolyDP(n, 5, True)
        cv2.drawContours(frame, [approx], -1, (255,0,0),5)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], -1, (0,0,255) , 5)
    
    
    
    cv2.imshow('contour',frame)
    cv2.imshow('frame', edged)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

cap.release()

cv2.destroyAllWindows()
