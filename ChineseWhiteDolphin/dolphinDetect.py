import cv2 
import numpy as np 
import time 

def initNet():
    CONFIG = 'yolov4-tiny-myobj.cfg'
    WEIGHT = 'yolov4-tiny-myobj_best.weights'
    #WEIGHT = 'yolov4-gaztop.weights'
    NAMES = 'obj.names'
    
    with open(NAMES, 'r') as f:
        names = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0,255,size=(len(names),3))

        net = cv2.dnn.readNet(CONFIG,WEIGHT)
        model = cv2.dnn_DetectionModel(net) 
        model.setInputParams(size=(416,416),scale=1/255.0)
        model.setInputSwapRB(True) 
        return model, names, colors 
    
def nnProcess(image, model): 
    #classes, confs, boxes = model.detect(image, 0.6,0.3)
    classes, confs, boxes = model.detect(image, 0.01,0.3)
    return classes, confs, boxes 

def drawBox(image, classes, confs, boxes, names, colors):
    new_image = image.copy()
    for(classid, conf, box) in zip(classes, confs, boxes):
        x,y,w,h=box
        area = w*h
        label = '{}: {:.2f}, {}'.format(names[int(classid)],float(conf),int(area))
        color = colors[int(classid)]
        cv2.rectangle(new_image, (x,y), (x+w, y+h),color,2)
        cv2.putText(new_image, label, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,2) 
    return new_image 

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

color5 = ((0,0,123),(180,55,255))  # 0750.jpg
lower5 = np.array(color5[0], dtype="uint8")
upper5 = np.array(color5[1], dtype="uint8")

model, names, colors = initNet()
#cap = cv2.VideoCapture(0) #from webcam 
#cap = cv2.VideoCapture('/home/tychien/Downloads/topdowndolphin.mp4')
cap = cv2.VideoCapture('/home/tychien/Downloads/0918X36/1/10030153.mp4')
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ratio = cap.get(cv2.CAP_PROP_FRAME_WIDTH) / cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
WIDTH = 1280 
HEIGHT = int(WIDTH/ratio)
#HEIGHT = 720 

while True: 
    begin_time = time.time()
    ret, frame = cap.read() 
    frame = cv2.resize(frame, (WIDTH,HEIGHT))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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

    mask5 = cv2.inRange(hsv, lower5, upper5)
    mask5 = cv2.erode(mask5, None, iterations = 1)
    mask5 = cv2.dilate(mask5, None, iterations = 1)


    mask = mask1 + mask2 + mask3 + mask4 + mask5

    out = cv2.bitwise_and(frame,frame,mask=mask)

    classes, confs, boxes = nnProcess(frame, model) 
    #classes, confs, boxes = nnProcess(out, model) 
    
    frame = drawBox(frame, classes, confs, boxes, names, colors) 
    #frame = drawBox(out, classes, confs, boxes, names, colors) 
    fps = 'fps:{:.2f}'.format(1/ (time.time() - begin_time))
    cv2.putText(frame, fps, (10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,204,255),2) 
    #cv2.putText(out, fps, (10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,204,255),2) 
    cv2.imshow('video', frame) 
    #cv2.imshow('video', out) 
    if cv2.waitKey(1) ==27:
        cv2.destroyAllWindows() 
        break 
