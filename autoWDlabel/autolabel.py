import os, re, cv2, sys, time
import numpy as np


annotation_dir = '/home/tychien/ChineseWhiteDolphin/findDolphin/VOCdevkit/VOC2018/Annotations'  
listname = '/home/tychien/cvtest/sortandshuffle/randompic.txt'
o_dir = open(listname, 'r')


def initNet():
    CONFIG = 'yolov4-tiny-myobj.cfg'
    WEIGHT = 'yolov4-tiny-myobj_best.weights'
    NAMES  = 'obj.names'

    with open(NAMES, 'r') as f:
        names = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0,255,size=(len(names),3))
        net = cv2.dnn.readNet(CONFIG,WEIGHT)
        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416,416),scale=1/255.0)
        model.setInputSwapRB(True)
        return model, names, colors


def nnProcess(image, model):
    classes, confs, boxes = model.detect(image, 0.7,0.3)
    return classes, confs, boxes


def picspect(filename):
    frame = cv2.imread(filename)
    width = frame.shape[1]
    height= frame.shape[0]
    depth = frame.shape[2]
    model,  names, colors = initNet()
    classes,confs, boxes  = nnProcess(frame, model)
    return [width, height, depth, model, names, colors, classes, confs, boxes]


def getPicSpectAndDetect():
    with o_dir as o:
        arr = o.readlines()
        counter = 0
        while arr:
            if counter <1000:
                starttime = time.time()
                filename = arr.pop()
                filename = re.sub(r'\n','',filename)
                spect = picspect(filename)
                name = filename.split('/')[-1]
                print(name)
                #print(filename)
                writeAnnotation(name,filename,picspect(filename))
                counter+=1
                timeleft = (1000-counter)*(time.time()-starttime)
                
                print(str(counter/1000*100)+'%, '+'{:06.3f} s'.format(timeleft))
                #sys.stdout.write('\r%d%%' % ((counter/1000)*100))
            else: 
                break


def writeAnnotation(picturefile,picturepath,picspect):
    filename = picturefile.split('.')[-2]+'.xml'
    with open(filename,'w') as f:
        f.write('<annotation>\n'+ 
                '\t<folder>JPEGImages</folder>\n'+
                '\t<filename>'+picturefile+'</filename>\n'+ 
                '\t<path>'+picturepath+'</path>\n'+
                '\t<source>\n'+
                '\t\t<database>Unknown</database>\n'+ 
                '\t</source>\n'+
                '\t<size>\n'+
                '\t\t<width>'+str(picspect[0])+'</width>\n'+
                '\t\t<height>'+str(picspect[1])+'</height>\n'+
                '\t\t<depth>'+str(picspect[2])+'</depth>\n'+
                '\t</size>\n'+
                '\t<segmented>0</segmented>\n')
        for(classid, conf, box) in zip(picspect[6],picspect[7],picspect[8]):
            x,y,w,h = box 
            name = picspect[4][int(classid)]
            f.write('\t<object>\n'+
                    '\t\t<name>'+name+'</name>\n'+
                    '\t\t<pose>Unspecified</pose>\n'+
                    '\t\t<truncated>0</truncated>\n'+
                    '\t\t<difficult>0</difficult>\n'+
                    '\t\t<bndbox>\n'+
                    '\t\t\t<xmin>'+str(x)+'</xmin>\n'+
                    '\t\t\t<ymin>'+str(y)+'</ymin>\n'+
                    '\t\t\t<xmax>'+str(x+w)+'</xmax>\n'+
                    '\t\t\t<ymax>'+str(y+h)+'</ymax>\n'+
                    '\t\t</bndbox>\n'+
                    '\t</object>\n')
        f.write('</annotation>')
                
getPicSpectAndDetect()
