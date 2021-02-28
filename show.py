import cv2
import time

cap = cv2.VideoCapture(0)
width = 1280
height= 960

if cap.isOpened() == False:
    cap.open()

while (True):
    
    start_time = time.time()

    ret, frame = cap.read()

#    frame = cv2.resize(frame, (width, height))
    cv2.imshow("frame", frame)

    fps = 1/(time.time()-start_time)

    print('{:.1f}'.format(fps))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()
