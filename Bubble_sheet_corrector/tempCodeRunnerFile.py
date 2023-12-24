cv2.HoughCircles(edged, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
               param2 = 15, minRadius = 20, maxRadius = 30)