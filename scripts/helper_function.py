import pyrealsense2 as rs
import numpy as np
import cv2
import time 

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
    

    