import shutil
import re 

listfile = 'randompic.txt'
source = ''
destDir= '/home/tychien/ChineseWhiteDolphin/findDolphin/VOCdevkit/VOC2018/JPEGImages'

with open(listfile,'r') as f:
    arr = f.readlines()
    while arr:
        source = arr.pop()
        source = re.sub(r'\n','',source)
        shutil.copy(source, destDir)
