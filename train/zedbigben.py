import pyzed.sl as sl
import cv2
import numpy as np 
import time 

def initNet():
    CONFIG = 'yolov4-tiny-myobj.cfg'
    WEIGHT = 'yolov4-tiny-myobj_final.weights'
    NAMES  = 'obj.names' 

    with open(NAMES, 'r') as f:
        names = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0,255,size=(len(names),3))

    net = cv2.dnn.readNet(CONFIG, WEIGHT)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416,416),scale=1/255.0)
    model.setInputSwapRB(True)

    return model, names, colors

def nnProcess(image, model):
    classes, confs, boxes = model.detect(image, 0.6, 0.3)
    return classes, confs, boxes


def drawBox(image, classes, confs, boxes, names, colors):
    new_image= image.copy()
    for (classid, conf, box) in zip(classes, confs, boxes):
        x,y,w,h = box 
        label = '{}: {:.2f}'.format(names[int(classid)],float(conf))
        color = colors[int(classid)]
        cv2.rectangle(new_image, (x,y),(x+w,y+h),color,2)
        cv2.putText(new_image, label, (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.7,color, 2)
    return new_image


zed = sl.Camera() 

input_type = sl.InputType()
init = sl.InitParameters(input_t = input_type)
init.camera_resolution = sl.RESOLUTION.HD1080 
err = zed.open(init)

image_size = zed.get_camera_information().camera_resolution
image_size.width = image_size.width /2
image_size.height = image_size.height/2

image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)


model, names, colors = initNet()

while True:
    begin_time = time.time()
    err = zed.grab() 
    zed.retrieve_image(image_zed, sl.VIEW.LEFT,sl.MEM.CPU, image_size)
    frame = image_zed.get_data()


    #frame = cv2.resize(frame, (WIDTH,HEIGHT ))
    classes, confs, boxes = nnProcess(frame, model)
    frame = drawBox(frame, classes, confs, boxes, names, colors)

    fps = 'fps: {:.2f}'.format(1 / (time.time() - begin_time))
    cv2.putText(frame, fps, (10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,204, 255),2)
    cv2.imshow('video',frame)
    if cv2.waitKey(1) ==27:
        cv2.destroyAllWindows()
        break

