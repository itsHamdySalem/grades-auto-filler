import cv2
import numpy as np
from functools import cmp_to_key


def cmp(a, b):
    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)
    if abs(br_a[0] - br_b[0]) <= 5:
        return br_a[1] - br_b[1]
    return br_a[0] - br_b[0]


def sorted_counter(contours):
    return sorted(contours, key=cmp_to_key(cmp))


def extract_cells(img, grid_points_img):
        # Convert grid_points_img to grayscale
    grid_points_gray = cv2.cvtColor(grid_points_img, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image (optional, based on your needs)
    _, thresh = cv2.threshold(grid_points_gray, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours using your custom comparison function
    contours = sorted_counter(contours)

    rows = []
    for c in range(len(contours)-1):
        x1, y1, w1, h1 = cv2.boundingRect(contours[c])
        x2, y2, w2, h2 = cv2.boundingRect(contours[c+1])
        rows.append(y1)
        if (x1 != x2):
            break

    N = len(rows)
    M = len(contours) // N

    for x in range(0, N-1):
        for y in range(0, M - 1):
            # Returns the location and width,height for every contour
            x1, y1, w1, h1 = cv2.boundingRect(contours[x + y * N])
            x2, y2, w2, h2 = cv2.boundingRect(contours[x + y * N + 1])
            x3, y3, w3, h3 = cv2.boundingRect(contours[x + (y + 1) * N + 1])
            # crop image
            cell = img[y1 + h1: y3, x2 + w2: x3]
            cv2.imshow("cell{{x * m + y}}", cell)
            cv2.imwrite('./results/cell{{x * m + y}}.jpg', cell)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    img = cv2.imread('img.jpg')
    grid_points_img = cv2.imread('grid_points_img.jpg')
    extract_cells(img=img, grid_points_img=grid_points_img)
