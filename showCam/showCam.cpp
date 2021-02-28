#include <opencv2/core.hpp>
#include <stdio.h>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <ctime>
#include <iostream>


using namespace cv;
int main()
{
    VideoCapture camera;
    
    if (!camera.isOpened())
    	camera.open(0);
    
    while(true)
    {
	std::clock_t t = clock();
 	Mat frame;
	camera >> frame;
	namedWindow("frame", WINDOW_AUTOSIZE );
	imshow("frame", frame);
	std::clock_t end_t = clock();
	auto fps = 1000.0*(end_t-t)/CLOCKS_PER_SEC;

	std::cout << "frame rate: " << fps << std::endl;

	if (waitKey(1) ==27){
		destroyAllWindows();
		break;
	}

    }
   
    waitKey(0);
    
    return 0;
}
