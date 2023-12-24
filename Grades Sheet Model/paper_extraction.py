import cv2
import numpy as np
from utils import *


def reorder_points(points):
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


def extract_paper_region(input_img, iterations=1):
    output_image = input_img

    for i in range(iterations):
        input_img = output_image
        img_RGB = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_RGB, cv2.COLOR_BGR2GRAY)

        canny_edged_image = cv2.Canny(img_gray, 100, 255)

        win = np.ones((5, 5), np.uint8)
        canny_edged_image = cv2.dilate(canny_edged_image, win, iterations=2)
        contours, _ = cv2.findContours(
            canny_edged_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        image_with_contours = np.copy(img_RGB)
        cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 20)

        largest_contour = np.array([])
        mxArea = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            approximated_edge = cv2.approxPolyDP(
                contour, 0.02 * perimeter, True)
            if area > mxArea and len(approximated_edge) == 4:
                mxArea = area
                largest_contour = approximated_edge

        biggest_contour = reorder_points(largest_contour)

        y, x = img_gray.shape[:2]

        pts1 = np.array(biggest_contour, np.float32)
        pts2 = np.array([[0, 0], [x, 0], [0, y], [x, y]], np.float32)

        matrix = cv2.getPerspectiveTransform(pts1, pts2)

        output_image = cv2.warpPerspective(img_gray, matrix, (x, y))

    return output_image
