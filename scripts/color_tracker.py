import pyrealsense2 as rs
import numpy as np
import cv2
import time 
import imutils 
from helper_function import *


#define color boundaries in HSV space
boundaries = [
	
	([50, 104, 64], [125, 255, 255]),       #blue
    ([0 , 93, 117] , [37, 255, 255])		#yellow
]

contour_color  = (0,255,0)
center_color = (0,0,255)
center_line_thickness = 4

resize_ratio = 0.7

fbs = 30
# available resolutions = (640,360),(640,400),(640,480),(848.100),(848,480),(1280,720),(1280,800)
image_width = 848
image_height = 480

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, image_width, image_height, rs.format.z16, fbs)
config.enable_stream(rs.stream.color, image_width, image_height, rs.format.bgr8, fbs)

# Start streaming
pipeline.start(config)


# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

dst = 0
counter = 0
process_period  = 30   #process once every some number of frames 
try: 
    while True:
        cur_time = time.time()
        counter +=1
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        #calculate pointcloud from frames
        #point_cloud = rs.pointcloud.calculate(aligned_frames)
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #isolate colors based on boundaries 
        for boundary in boundaries:
            print(boundary)
            contours, centers = color_tracker([boundary], color_image)
            print('centers',centers)
            if len(contours) > 0 :
                radius = 3
                color_image = cv2.drawContours(color_image, contours, -1, contour_color, 3)
                for center in centers:
                    color_image = cv2.circle(color_image, center, radius, center_color, thickness=center_line_thickness, lineType=8, shift=0)
                    print('c')
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)

        color_image = cv2.resize(color_image,None, fx = resize_ratio,fy=resize_ratio,interpolation = cv2.INTER_CUBIC)
        depth_colormap = cv2.resize(depth_colormap,None, fx=resize_ratio,fy=resize_ratio, interpolation=cv2.INTER_CUBIC)
        images = np.hstack((color_image, depth_colormap))
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)



finally:
    # Stop streaming
    pipeline.stop()