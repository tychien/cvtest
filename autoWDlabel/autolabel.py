import os, re, cv2 

annotation_dir = '/home/tychien/cvtest/autoWDlabel/'  
listname = '/home/tychien/cvtest/sortandshuffle/randompic.txt'
o_dir = open(listname, 'r')
picturefile = 'shit.jpg'
picturepath = '/home/tychien/cvtest/'+picturefile


def picspect(filename):
    frame = cv2.imread(filename)
    width = frame.shape[1]
    height= frame.shape[0]
    depth = frame.shape[2]
    return [width, height, depth]


def getPicSpectAndDetect():
    with o_dir as o:
        arr = o.readlines()
        counter = 0
        while arr:
            if counter <10:
                filename = arr.pop()
                filename = re.sub(r'\n','',filename)
                spect = picspect(filename)
                name = filename.split('/')[-1]
                print(name)
                print(filename)
                writeAnnotation(name,filename,picspect(filename))
                counter+=1
            else: 
                break

def writeAnnotation(picturefile,picturepath,picspect):
    filename = picturefile.split('.')[-2]+'.xml'
    with open(filename,'a') as f:
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
                '\t</size>\n')

getPicSpectAndDetect()
