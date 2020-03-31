# Vision-based auto gripping
object detection based on classical computer vision approaches with intel Realsense D435 for purpose of automated 
## Language: python 3
## Dependencies: 
> **pyrealsense** 

  >> $ pip3 install pyrealsense

> **Open CV**

>> $ pip3 install opencv-python

> **Imutils** 

>>  $ pip3 install imutils

## Hardware: 
> Intel Realsense D435 

In folder "scripts/.." containing live streaming scripts. 
  
### Sift-based object detection:

Sift is mainly used for objects that have some texture or local features to detect. 

To use SIFT you need to install opencv from source and contribution library
> $ pip3 install opencv-python==3.4.2.16

> $ pip3 install opencv-contrib-python==3.4.2.16

Take an image of the object you want to detect during streaming. Image should contain only object you want to detect and put it in folder: 
> $ scripts/images/... 

Modify path in line 16 in scripts/Sift.py

> sample_img = cv2.imread('path/to/image.extension')

> example: $ sample_img = cv2.imread('images/sample1.jpg')

connect your Realsense camera

run script: 

>> python3 scripts/Sift.py


### Color-based tracking:

This is used to track objects that are blank but with very significant color. color filtering here is done in HSV color space.
 
 run script: 
  > $ python3 scripts/color_tracker.py 
  
  
 if you want to detect your own object use script "range-detector". you can find it in folder: scripts/ 
 
 or from Imutils library: https://github.com/jrosebr1/imutils/blob/master/bin/range-detector
 
 This scripts helps you to find your color boundareis. It's recommended to do it in HSV space not RGB. 
 
 to run script: 
 
 > $ range-detector --filter HSV --image /path/to/image.png
 
 Take values you got and open scripts/color_tracker.py 
 
 add your values inside "Boundaries" tuble in line 10. 
 
 then run script: 
> $ python3 scripts/color_tracker.py 
