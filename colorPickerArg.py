from colorfilters import HSVFilter
import cv2 
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i1','--image1',required=True, help='image1')
args = vars(ap.parse_args())
img = cv2.imread(args['image1'])


width, height, channel = img.shape
ratio = float(height)/float(width) 
WIDTH = 1280 
HEIGHT= int(WIDTH/ratio) 


img = cv2.resize(img,(WIDTH,HEIGHT))
window = HSVFilter(img)
window.show()

print(f'lower: {window.lowerb} upper: {window.upperb}.')
