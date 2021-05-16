#import sys 
import os 
import cv2
import numpy as np 

#for arg in sys.argv: 
#    print(sys.argv[1])
#array_of_img = []

def read_imdirectory(directory_name):
    for filename in os.listdir(r"./"+directory_name):
        print(filename)
        image = cv2.imread(directory_name+"/"+filename)
        
        #array_of_img.append(img) 
        print(array_of_img) 


image = cv2.imread('/home/tychien/BASNet/test_data/test_images/CHS20180410_02_KP_IMG_5421.jpg')

mask = cv2.imread('/home/tychien/BASNet/test_data/test_results/CHS20180410_02_KP_IMG_5421.png')

result = cv2.bitwise_and(image, mask)
cv2.imwrite('shit.jpg',result)

width, height, channel = result.shape 
ratio = float(width)/float(height) 

result = cv2.resize(result,(1024,int(1024*ratio))) 


#cv2.namedWindow('result', cv2.WINDOW_NORMAL) 
cv2.imshow('result',result) 

cv2.waitKey(0)
cv2.destroyAllWindows() 
