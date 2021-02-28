import cv2

image = cv2.imread('blox.jpg')

sift_feature = cv2.xfeatures2d.SIFT_create()
surf_feature = cv2.xfeatures2d.SURF_create()
orb_feature  = cv2.ORB_create()

sift_kp = sift_feature.detect(image)
surf_kp = surf_feature.detect(image)
orb_kp  = orb_feature.detect(image)

sift_out= cv2.drawKeypoints(image, sift_kp, None)
surf_out= cv2.drawKeypoints(image, surf_kp, None)
orb_out = cv2.drawKeypoints(image, orb_kp, None)


image = cv2.vconcat((cv2.hconcat([image, sift_out]),cv2.hconcat([surf_out, orb_out])))



cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
