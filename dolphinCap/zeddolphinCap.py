import cv2 
import numpy as np 
import time 


index = 0
total = 100
n = 1

def initNet():
    CONFIG = 'yolov4-tiny-myobj.cfg'
    WEIGHT = 'yolov4-tiny-myobj_best.weights'
    NAMES = 'obj.names'
    
    with open(NAMES, 'r') as f:
        names = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0,255,size=(len(names),3))

        net = cv2.dnn.readNet(CONFIG,WEIGHT)
        model = cv2.dnn_DetectionModel(net) 
        model.setInputParams(size=(416,416),scale=1/255.0)
        model.setInputSwapRB(True) 
        return model, names, colors 
    
def nnProcess(image, model, index): 
    #classes, confs, boxes = model.detect(image, 0.6,0.3)
    classes, confs, boxes = model.detect(image, 0.7,0.3)
    if(len(confs)>0):
        index += (len(confs))
        print(confs[0])
    return classes, confs, boxes, index

def saveImage(dolphinIMG, index):
    filename = 'images/h0/{:03d}.jpg'.format(index)
    cv2.imwrite(filename, dolphinIMG)
    print(filename)

    
def drawBox(image, classes, confs, boxes, names, colors, index):
    new_image = image.copy()
    for(classid, conf, box) in zip(classes, confs, boxes):
        x,y,w,h=box 
        save_image = new_image[y:y+h, x:x+w] 
        saveImage(save_image, index)
        label = '{}: {:.2f}'.format(names[int(classid)],float(conf))
        color = colors[int(classid)]
        cv2.rectangle(new_image, (x,y), (x+w, y+h),color,2)
        cv2.putText(new_image, label, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,2) 
    return new_image


model, names, colors = initNet()
cap = cv2.VideoCapture(0) #from webcam 
#cap = cv2.VideoCapture('/home/tychien/Downloads/dolphinPTS.mp4')

if cap.isOpened() == 0:
    exit(-1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while n>0:
    print('index:{:03d}'.format(index))
    begin_time = time.time()
    ret, frame = cap.read() 
    frame = np.split(frame,2,axis=1)
    frame = frame[0]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    classes, confs, boxes, index = nnProcess(frame, model,index) 
    
    frame = drawBox(frame, classes, confs, boxes, names, colors, index) 
    fps = 'fps:{:.2f}'.format(1/ (time.time() - begin_time))
    cv2.putText(frame, fps, (10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,204,255),2) 
    cv2.imshow('video', frame) 
    
    if index >= total:
        print('capture done')
        n = -1
        break

    if cv2.waitKey(1) ==27:
        cv2.destroyAllWindows() 
        break 
