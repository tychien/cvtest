import cv2
import time

cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    cap.open()

while (True):
    
    start_time = time.time()

    ret, frame = cap.read()
    
    cv2.imshow("frame", frame)

    fps = 1/(time.time()-start_time)

    print('{:.1f}'.format(fps))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()
