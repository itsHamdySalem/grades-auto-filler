from utils import *
import cv2
import numpy as np

def reorderPoints(points):
    points = points.reshape((4, 2))

    newPoints = np.zeros((4, 1, 2), dtype=np.int32)

    add = points.sum(1)
    diff = np.diff(points, axis=1)

    minSumIndex = np.argmin(add)
    maxSumIndex = np.argmax(add)

    minDiffIndex = np.argmin(diff)
    maxDiffIndex = np.argmax(diff)

    newPoints[0] = points[minSumIndex]
    newPoints[3] = points[maxSumIndex]
    newPoints[1] = points[minDiffIndex]
    newPoints[2] = points[maxDiffIndex]

    return newPoints

def extract_paper_region(img_RGB):
    img_RGB = cv2.cvtColor(img_RGB, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_RGB, cv2.COLOR_BGR2GRAY)

    cannyEdgedImage = cv2.Canny(img_gray, 100, 255)

    win = np.ones((5, 5), np.uint8)
    cannyEdgedImage = cv2.dilate(cannyEdgedImage, win, iterations=2)
    contours, _ = cv2.findContours(cannyEdgedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    image_with_contours = np.copy(img_RGB)
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 20)

    largestContour = np.array([])
    mxArea = 0
    
    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        approximatedEdge = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if area > mxArea and len(approximatedEdge) == 4:
            mxArea = area
            largestContour = approximatedEdge
    
    biggestContour = reorderPoints(largestContour)

    y, x = img_gray.shape[:2]

    pts1 = np.array(biggestContour,np.float32)
    pts2 = np.array([[0, 0], [x, 0], [0, y], [x, y]],np.float32)

    
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    WarpedGrayImage = cv2.warpPerspective(img_gray, matrix, (x, y))
    WarpedColoredImage = cv2.warpPerspective(img_RGB, matrix, (x, y))

    # show_images([img_RGB, WarpedColoredImage], ['Original', 'RGB'])
    return WarpedColoredImage, WarpedGrayImage
 