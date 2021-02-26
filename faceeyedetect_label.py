import cv2
import time

cap = cv2.VideoCapture(0)

face_cascade    = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade     = cv2.CascadeClassifier('haarcascade_eye.xml')

if cap.isOpened() == False:
    cap.open()

while (True):
    
    start_time  = time.time()

    ret, frame  = cap.read()
    frame = cv2.flip(frame,1)

    gray        = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces       = face_cascade.detectMultiScale(gray, 1.5, 3)
    for(x,y,w,h) in faces:
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h),(210,204,228),9)
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, 'face', (x,y-20), font, 3, (210,204,228), 5, cv2.LINE_AA)
        face_rect = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(face_rect, 1.3,8)
        for (ex, ey, ew, eh) in eyes:
            center = (x + ex + int(ew/2.0), y+ey+int(eh/2.0))
            r = int(min(ew, eh) /2.0)
            frame = cv2.circle(frame, center, r, (227,182,183),5)
            cv2.putText(frame, 'eye', (x+ex, y+ey-5), font, 1, (227,182,183),4, cv2.LINE_AA) 
         
    cv2.imshow("frame", frame)

    fps = 1/(time.time()-start_time)

    print('{:.1f}'.format(fps))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()
