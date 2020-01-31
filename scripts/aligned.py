## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2

#put your color filter range values here
#boundaries = [([25, 50, 50], [62, 200, 250])]
boundaries = [([0,0,00],[50,50,50])]

#converting boundaries to numpy arrays
for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")

fbs = 60
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

try:
    while True:

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
        mask = cv2.inRange(color_image, lower, upper)
        masked_image = cv2.bitwise_and(color_image, color_image, mask = mask)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((masked_image, depth_colormap))
        
        print(color_image.shape)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()