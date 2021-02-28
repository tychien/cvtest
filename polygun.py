import cv2

RECT, HEXAGON = 1,0

cap = cv2.VideoCapture(0)
if cap.isOpened() == False:
    cap.open()

while (True):

    ret, frame = cap.read()

    #frame = cv2.imread('poly.png')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9,9),0)
    edged = cv2.Canny(gray, 50, 150)
    edged = cv2.dilate(edged, None, iterations=3)
    #edged = cv2.erode(edged, None, iterations=2)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    print('Num. of Contours = '+ str(len(contours)))
    print('Contours[0]:'+str(len(contours[0])))
    #print('rec edge num:{} '.format(len(contours[RECT])))
    #print('hex edge num:{} '.format(len(contours[HEXAGON])))

    for n in contours:
        approx = cv2.approxPolyDP(n, 5, True)
        cv2.drawContours(frame, [approx], -1, (255,0,0),5)
        if len(approx) == 4:
            cv2.drawContours(frame, [approx], -1, (0,0,255) , 5)
    
    
    #print('rec edge num:{} '.format(len(approx_rect)))
    #print('edge num:{} '.format(len(approx_1)))

    #cv2.drawContours(frame, [approx_1], -1, (255,255,0),5)
    #cv2.drawContours(frame, [approx_rect],-1, (0,0,255), 5)
    #cv2.drawContours(frame, [approx_hex], -1, (0,0,255),5)
    
    cv2.imshow('contour',frame)
    cv2.imshow('frame', edged)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()
