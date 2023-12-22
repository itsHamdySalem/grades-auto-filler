from utils import *
import cv2
import numpy as np

def reorderPoints(points):
    x_sorted = points[np.argsort(points[:, 0])]
    left_most = x_sorted[:2, :, :]
    right_most = x_sorted[2:, :, :]

    left_most = left_most[np.argsort(left_most[:, 1])]
    (tl, bl) = left_most

    right_most = right_most[np.argsort(right_most[:, 1])]
    (tr, br) = right_most

    new_points = np.array([tl, tr, br, bl], dtype=np.int32)
    return new_points


def extract_paper_region(ImagePath):

    img_BGR=cv2.imread(ImagePath, cv2.IMREAD_COLOR)
    img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2GRAY)

    cannyEdgedImage=cv2.Canny(img_gray,100,255)

    win = np.ones((5,5),np.uint8)
    cannyEdgedImage = cv2.dilate(cannyEdgedImage,win,iterations=2)
    contours, _=cv2.findContours(cannyEdgedImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    image_with_contours=np.copy(img_RGB)
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
    
    biggestContour= reorderPoints(largestContour)

    biggest_contour_img=np.copy(img_RGB)
    cv2.drawContours(biggest_contour_img, biggestContour, -1, (0, 255, 0), 20)


    y = img_gray.shape[0]
    x = img_gray.shape[1]

    pts1 = np.float32(biggestContour) 
    pts2 = np.float32([[0, 0],[x, 0], [0, y],[x, y]]) 
    
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    WarpedGrayImage = cv2.warpPerspective(img_gray, matrix, (x, y))
    WarpedColoredImage = cv2.warpPerspective(img_RGB, matrix, (x, y))
    
    show_images([img_RGB,WarpedColoredImage],['Original','RGB'])
    return (WarpedColoredImage,WarpedGrayImage)