import cv2 
import numpy as np 
import time 

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
    
def nnProcess(image, model): 
    classes, confs, boxes = model.detect(image, 0.6,0.3)
#    classes, confs, boxes = model.detect(image, 0.65,0.3)
    return classes, confs, boxes 

def drawBox(image, classes, confs, boxes, names, colors):
    new_image = image.copy()
    for(classid, conf, box) in zip(classes, confs, boxes):
        x,y,w,h=box 
        label = '{}: {:.2f}'.format(names[int(classid)],float(conf))
        color = colors[int(classid)]
        cv2.rectangle(new_image, (x,y), (x+w, y+h),color,2)
        cv2.putText(new_image, label, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,2) 
    return new_image 


model, names, colors = initNet()

image = cv2.imread('/home/tychien/2018IDbyName/Adobe/Good/CHS20180315_02_XN_IMG_0020.jpg') 
width, height, channel = image.shape 
ratio = float(width)/float(height)
WIDTH = 1280 
HEIGHT = int(WIDTH/ratio)
frame = cv2.resize(image, (WIDTH,HEIGHT))


classes, confs, boxes = nnProcess(image, model) 
    
image = drawBox(image, classes, confs, boxes, names, colors) 
cv2.imshow('video', image) 
cv2.waitKey(0)
cv2.destroyAllWindows() 
