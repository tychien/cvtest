import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i1','--image1',required=True, help = 'first image')
ap.add_argument('-i2','--image2',required=True, help = 'second image')
args = vars(ap.parse_args())

img1 = cv2.imread(args['image1'])
img2 = cv2.imread(args['image2'])

feature = cv2.xfeatures2d.SIFT_create()
#feature = cv2.ORB_create()
kp1, des1 = feature.detectAndCompute(img1, None)
kp2, des2 = feature.detectAndCompute(img2, None)

bf = cv2.BFMatcher()
#bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.knnMatch(des1, des2, k=2)
#matches = bf.match(des1, des2)


good = []
for m, n in matches:
    if (m.distance < 0.55 * n.distance) & (len(good)<1000):
        good.append(m)
        print('Matching points :{}'.format(len(good)))
        img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [good], outImg=None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
'''
matches = sorted(matches, key=lambda x:x.distance)
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20
    ],outImg=None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
'''

width, height, channel = img3.shape
ratio = float(width)/float(height)
img3 = cv2.resize(img3, (1024, int(1024 * ratio)))
cv2.imshow('image',img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
