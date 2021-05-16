from colorfilters import HSVFilter
import cv2 

img = cv2.imread('/home/tychien/cvtest/ChineseWhiteDolphin/train/VOCdevkit/VOC2018/JPEGImages/0750.jpg')
width, height, channel = img.shape
ratio = float(height)/float(width) 
WIDTH = 1280 
HEIGHT= int(WIDTH/ratio) 


img = cv2.resize(img,(WIDTH,HEIGHT))
window = HSVFilter(img)
window.show()

print(f'lower: {window.lowerb} upper: {window.upperb}.')
