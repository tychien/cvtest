import numpy as np
import pyzed.sl as sl
import cv2
import time
import math

def main() :

    
    # Setting Color to catch with 
    color = ((0,120,70),(10,255,255)) 
    lower = np.array(color[0], dtype='uint8')
    upper = np.array(color[1], dtype='uint8')

    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    input_type = sl.InputType()
    init = sl.InitParameters(input_t=input_type)
    init.camera_resolution = sl.RESOLUTION.HD1080
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.METER

    # Open the camera
    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS :
        print(repr(err))
        zed.close()
        exit(1)

    # Set runtime parameters after opening the camera
    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.STANDARD

    # Prepare new image size to retrieve half-resolution images
    image_size = zed.get_camera_information().camera_resolution
    image_size.width = image_size.width /2
    image_size.height = image_size.height /2

    # Declare your sl.Mat matrices
    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    depth_image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)

    key = ' '
    while key != 113 :
        start_time = time.time()
        err = zed.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS :
            # Retrieve the left image, depth image in the half-resolution
            zed.retrieve_image(image_zed, sl.VIEW.LEFT, sl.MEM.CPU, image_size)
            zed.retrieve_measure(depth_image_zed, sl.MEASURE.DEPTH, sl.MEM.CPU, image_size)

            # To recover data from sl.Mat to use it with opencv, use the get_data() method
            # It returns a numpy array that can be used as a matrix with opencv
            image_ocv = image_zed.get_data()
            depth_image_ocv = depth_image_zed.get_data()

            
            hsv = cv2.cvtColor(image_ocv, cv2.COLOR_BGR2HSV)
            hsv = cv2.GaussianBlur(hsv, (11,11),0)
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.erode(mask, None, iterations = 2)
            mask = cv2.dilate(mask, None, iterations = 2)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            if len(contours) >0:
                cnt = max(contours, key=cv2.contourArea)
                if cv2.contourArea(cnt) <100:
                    continue
                x,y,w,h = cv2.boundingRect(cnt)
                centroidx = x+w*0.5
                centroidy = y+h*0.5
                ypx = int(len(depth_image_ocv))
                xpx = int(len(depth_image_ocv[0]))

                fovv = 57 * math.pi/180
                fovh = 88 * math.pi/180

                vfn = ((0.5*ypx)-centroidy)/(0.5*ypx) * math.tan(0.5*fovv)
                hfn = ((0.5*xpx)-centroidx)/(0.5*xpx) * math.tan(0.5*fovh)

                atanv = math.atan(vfn)*180/math.pi
                atanh = math.atan(hfn)*180/math.pi


                p1 = (x-2, y-2)
                p2 = (x+w+4, y+h+4)

                depth = depth_image_ocv[y][x] 
                d_prl = depth * math.cos(math.atan(vfn)) * math.cos(math.atan(hfn))
                
                x_in_m = d_prl*math.tan(0.5*fovh)*(1-(x/(0.5*xpx)))
                y_in_m = d_prl*math.tan(0.5*fovv)*(1-(y/(0.5*ypx))) 

                cv2.rectangle(image_ocv,(5,10),(350,30),(0,0,0),-1)
                cv2.putText(image_ocv, 'x={:03.3f}m, y={:03.3f}m, r={:03.3f}m'.format(-x_in_m,y_in_m,d_prl),(10,25),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,255),1)
                cv2.rectangle(image_ocv, p1, p2, (0,255,255),2)
            
            
            cv2.imshow("Image", image_ocv)
            #cv2.imshow("Depth", depth_image_ocv)
            fps = 1/(time.time()-start_time)
            print('fps:{:.1f}'.format(fps))
            key = cv2.waitKey(10)
    cv2.destroyAllWindows()
    zed.close()

    print("\nFINISH")

if __name__ == "__main__":
    main()
