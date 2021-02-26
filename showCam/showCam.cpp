#include <opencv2/core.hpp>
#include <stdio.h>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>

using namespace cv;
int main()
{
    VideoCapture camera;
    
    if (!camera.isOpened())
    	camera.open(0);
    
    while(true)
    {
    	Mat frame;
	camera >> frame;
	namedWindow("frame", WINDOW_AUTOSIZE );
	imshow("frame", frame);

    }
   
    waitKey(0);
    
    return 0;
}
