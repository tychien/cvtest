import pyzed.sl as sl
import cv2
import numpy as np


def main():


    #color = ((100,150,0),(140,255,255)) #blue
    color = ((0,120,70),(10,255,255)) #red
    #color = ((16,59,0),(47,255,255)) #yellow
    lower = np.array(color[0], dtype="uint8")
    upper = np.array(color[1], dtype="uint8")



    zed = sl.Camera()
    
    input_type = sl.InputType()
    init = sl.InitParameters(input_t =input_type)
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.MILLIMETER
    init.camera_resolution = sl.RESOLUTION.HD1080


    err = zed.open(init)
    
    image_size = zed.get_camera_information().camera_resolution
    image_size.width = image_size.width /2
    image_size.height = image_size.height /2

    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    
    
    
    depth_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.F32_C1)

    while True:
        err = zed.grab()

        if zed.grab() == sl.ERROR_CODE.SUCCESS :
            zed.retrieve_image(image_zed, sl.VIEW.LEFT)
            zed.retrieve_measure(depth_zed, sl.MEASURE.DEPTH)
            image_ocv = image_zed.get_data()
            depth_ocv = depth_zed.get_data()
            
            print(depth_ocv[int(len(depth_ocv)/2)][int(len(depth_ocv[0])/2)])
            print('depth_ocv/2= {}'.format(int(len(depth_ocv)/2)))
            print('depth_ocv/2= {}'.format(int(len(depth_ocv[0])/2)))

        frame = image_ocv
    
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (11,11),0)

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations = 2)
        mask = cv2.dilate(mask, None, iterations = 2)
    
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) >0:
            cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) < 100:
                continue
            x,y,w,h = cv2.boundingRect(cnt)
            

            p1 = (x-2, y-2)
            p2 = (x+w+4, y+h+4)

            out = cv2.bitwise_and(hsv,hsv,mask=mask)
            depth = depth_ocv[y][x]
            cv2.putText(frame, 'x={} ,y={},dep={:06.3f}mm'.format(x+w/2,y+h/2,depth),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
            cv2.rectangle(frame, p1, p2, (0,255,255),2)
            cv2.rectangle(hsv, p1, p2, (0,255,255),2)
            cv2.rectangle(out, p1, p2, (0,255,255),2)
            #frame = cv2.hconcat([frame,hsv, out])
        cv2.imshow('frame',frame)
        #cv2.imshow("Image", image_ocv)
        if cv2.waitKey(1) ==27:
            cv2.destroyAllWindows()
            break

    cv2.destroyAllWindows()
    zed.close()


if __name__ == "__main__":
    main()
