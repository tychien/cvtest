# cv

### Feb 25 2021

build for nano GPU
1. https://www.pyimagesearch.com/2020/03/25/how-to-configure-your-nvidia-jetson-nano-for-computer-vision-and-deep-learning/
2. https://forums.developer.nvidia.com/t/opencv-face-detection-poor-performance-with-jetson-nano/73404
3. finished [show.py](https://github.com/tychien/cvtest/blob/main/show.py) , [showgray.py,](https://github.com/tychien/cvtest/blob/main/showgray.py), [faceeyedetect_label.py](https://github.com/tychien/cvtest/blob/main/faceeyedetect_label.py)

### Feb 26 2021

1. update to cuda virsion opencv for nvidia gpu
2. finished [faceGet.py](https://github.com/tychien/cvtest/blob/main/faceGet.py), [faceTraining.py](https://github.com/tychien/cvtest/blob/main/faceTraining.py),  [faceID.py](https://github.com/tychien/cvtest/blob/main/faceID.py)

### Feb 27 2021

1. Can't work on object tracking . maybe it's the jetson nano thing. the video just stuck in there.
2.https://answers.opencv.org/question/94448/module-cv2-has-no-attribute-createbackgroundsubtractormog/


### Mar 11 2021

1. It's now able to get the x, y, depth

### Mar 14 2021

_depth = depth
if d is been transformed, 

v = 
d_real = depth*cos(v)*cos(h)

fov = field of view
ypx = y in pixel
xpx = x in pixel

x_in_meter = depth * tan(1/2*fov) * (1 - (x/(1/2*xpx)))
y_in_meter = depth * tan(1/2*fov) * (1 - (y/(1/2*ypx)))



