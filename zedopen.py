import pyzed.sl as sl
import cv2
import numpy as np

def main():
    zed = sl.Camera()
    
    input_type = sl.InputType()
    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.MILLIMETER

    err = zed.open(init)

    image_size = zed.get_camera_information().camera_resolution
    image_size.width = image_size.width /2
    image_size.height= image_size.height /2

    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    
    while True:
        err = zed.grab()
        if err == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image_zed, sl.VIEW.LEFT)
            image_ocv = image_zed.get_data()
            cv2.imshow("Image",image_ocv)

            key = cv2.waitKey(10)

    cv2.destroyAllWindows()
    zed.close()

if __name__ == "__main__":
    main()
