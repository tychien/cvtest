import cv2

cap = cv2.VideoCapture('/home/tychien/Downloads/topdowndolphin.mp4')
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
success, frame = cap.read()

count = 0 
while success:
    success, frame = cap.read()
    cv2.imwrite('frame_%04d.jpg' % count, frame)
    print('Read ',count, 'frame: ', success)
    count += 1
