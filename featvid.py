import pyzed.sl as sl
import numpy as np
import math
import cv2


zed = sl.Camera()
input_type = sl.InputType()
init = sl.InitParameters(input_t = input_type)
init.coordinate_units = sl.UNIT.METER
init.camera_resolution = sl.RESOLUTION.HD1080

err = zed.open(init)

image_size = zed.get_camera_information().camera_resolution
image_size.width = image_size.width /2
image_size.height = image_size.height /2
image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)

while True:
    err = zed.grab()

    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        zed.retrieve_image(image_zed, sl.VIEW.LEFT)
        image_ocv = image_zed.get_data()
    
    
    image = image_ocv

    #sift_feature = cv2.xfeatures2d.SIFT_create()
    #surf_feature = cv2.xfeatures2d.SURF_create()
    orb_feature  = cv2.ORB_create()

    #sift_kp = sift_feature.detect(image)
    #surf_kp = surf_feature.detect(image)
    orb_kp  = orb_feature.detect(image)

    #sift_out= cv2.drawKeypoints(image, sift_kp, None)
    #surf_out= cv2.drawKeypoints(image, surf_kp, None)
    orb_out = cv2.drawKeypoints(image, orb_kp, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)


    #image = cv2.vconcat((cv2.hconcat([image, sift_out]),cv2.hconcat([surf_out, orb_out])))



    cv2.imshow('image', image)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()
zed.close()
