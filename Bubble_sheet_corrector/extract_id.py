from utils import *
import cv2
import numpy as np

def extract_id(colored, gray):
    edged = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(edged, 20, 70)
    detected_circles = cv2.HoughCircles(edged,
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 15, minRadius = 13, maxRadius = 20)
    if detected_circles is None:
        print("Error: Something went wrong during extracting the ID.")
        return None
    
    detected_circles = np.int16(np.around(detected_circles)) 

    circles = []  
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        circles.append((a, b, r))

    circles =  sorted(
        circles,
        key=lambda t: t[1]
    )
    if (len(circles)) > 1: # handling if the D in ID word is considered as a circle so just neglect it
        if np.abs(circles[0][1]-circles[1][1]) > 40:
            circles = circles[1:]
    
    id = ""
    for i in range(len(circles)//10) :
        currentRow = circles[i*10:i*10+10]
        currentRow = sorted(currentRow, key=lambda t: t[0])
        mx = 500
        dig = -1
        for j in range (len(currentRow)):
            [a, b, r] = currentRow[j]
            cnt = count_good_pixels(gray, a, b)
            if cnt > mx: 
                mx = cnt
                dig = j
        if dig == -1 : return None

        id+=str(dig)
                
    return id