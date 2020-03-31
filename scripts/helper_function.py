import pyrealsense2 as rs
import numpy as np
import cv2
import time 
import imutils

def find_obj_sift(kp1,des1,sample_dimension,scene,match_count,algorithm):
    MIN_MATCH_COUNT = match_count
    # find the keypoints and descriptors with SIFT
    kp2, des2 = algorithm.detectAndCompute(scene,None)
    
    #try:

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)


    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        # findHomography returns a mask that tells us, which point pairs did not pass the RANSAC filter
        matchesMask = mask.ravel().tolist()

        h,w,c = sample_dimension
        # Take corners of the first image and transform them onto the second image
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        dst = np.int32(dst)
        scene = cv2.polylines(scene,[dst],True,255,3, cv2.LINE_AA)
        
        print('p', dst)
        

    else:
        scene = scene
        dst = [] 
        #return scene 

            
    return scene , dst
    

def center_and_grip(points, frame): 

    

    return center 


def color_tracker(boundaries, image):
	for (lower, upper) in boundaries:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		#frame = imutils.resize(image, width=600)
		#blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, lower, upper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

			# find contours in the mask and initialize the current
			# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask
			c = max(cnts, key=cv2.contourArea)
			contours = []
			centers = []
			for cnt in cnts:
				if cv2.contourArea(cnt)>= 0.7*cv2.contourArea(c):
					((x, y), radius) = cv2.minEnclosingCircle(c)
					M = cv2.moments(cnt)
					center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
					contours.append(cnt)
					centers.append(center)


		else: 
			contours = []
			centers = []
		#print('contours', contours)

	return contours, centers			
