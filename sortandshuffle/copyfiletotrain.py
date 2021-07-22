import shutil
import re 

listfile = '/home/tychien/cvtest/sortandshuffle/randompic.txt'
source = ''
destDir= '/home/tychien/ChineseWhiteDolphin/findDolphin/VOCdevkit/VOC2018/JPEGImages'
counter = 0

with open(listfile,'r') as f:
    arr = f.readlines()
    
    while arr:
        if counter < 1000:
            source = arr.pop()
            source = re.sub(r'\n','',source)
            shutil.copy(source, destDir)
            counter+=1
        else:
            break
