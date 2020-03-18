## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import time 
from helper_function import find_obj_sift

start_moment  = time.time()

sample_img = cv2.imread('images/sample2.jpg')
# creating SIFT object 
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(sample_img,None)
sample_dimension = sample_img.shape
match_count = 10


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
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)

        print('depth', depth_image.shape, depth_image[1][0])
        print('color', depth_colormap.shape)
        #applying Sift detector 
        try:
            if((cur_time-start_moment) > 5.0 ):
                if counter >= process_period:
                
                    color_image , dst= find_obj_sift(kp1,des1,sample_dimension,color_image,match_count,sift)
                    counter = 0
                    


            if dst != []:       
                new_dst = dst
                print(new_dst)
                            #counter = 0
            # Stack both images horizontally
            print(dst[0][0][0])
            print(rs.depth_frame.get_distance(depth_frame, 5, 5) )
            
        
        except Exception as inst:
            print(inst)
            print(type(inst))
            pass 
        
        images = np.hstack((color_image, depth_colormap))
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)



finally:
    # Stop streaming
    pipeline.stop()