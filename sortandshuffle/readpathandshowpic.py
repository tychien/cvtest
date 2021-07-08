import cv2
import re

filename = ''
readfilename = 'randompic.txt'
f_dir = open(readfilename, 'r')

with f_dir as f:
    arr = f.readlines()
    filename += arr[0] 
    filename = re.sub(r'\n','',filename)
    
print(filename)

frame = cv2.imread(filename)
cv2.imshow('image', frame)

cv2.waitKey(0)
cv2.destroyAllWindows()
