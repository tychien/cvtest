import cv2

n = 1       #pic cal. 
index = 0   #filename.
total = 100 #total pic.

def saveImage(face_image, index):
    filename = '/home/nano2/image/h0/{:03d}.pgm'.format(index)
    cv2.imwrite(filename, face_image)
    print(filename)

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while n>0:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.5, 3)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0),3)
        cv2.putText(frame, 'img_{:03d}, face_{:03d}'.format(n,index),(x,y-20),cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0),2,cv2.LINE_AA)
        if n % 5 ==0:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (400,400))
            saveImage(face_img, index)
            index +=1
            if index >=total:
                print('traning finished')
                n = -1
                break
        n+=1

    cv2.imshow('video',frame)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
