import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i1','--image1',required=True, help = 'image1')
args = vars(ap.parse_args())

image = cv2.imread(args['image1'])

print(args['image1'])

#image = cv2.imread(img1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (9,9),0)
edged = cv2.Canny(gray, 20, 40)
contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
out = image.copy()
out.fill(0)
cv2.drawContours(out, contours, -1, (0, 255, 255),1)
#image = cv2.vconcat(image, out) 
cv2.imshow('frame', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
