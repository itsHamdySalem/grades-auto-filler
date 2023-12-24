import cv2
import numpy as np
from functools import cmp_to_key
from utils import show_images


def compare_contours(a, b):
    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)
    if abs(br_a[0] - br_b[0]) <= 5:
        return br_a[1] - br_b[1]
    return br_a[0] - br_b[0]


def sorted_counter(contours):
    return sorted(contours, key=cmp_to_key(compare_contours))


def extract_grid(img):
    kernel_length = np.array(img).shape[1] // 40
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, kernel_length))
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (kernel_length, 1))
    general_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(
        img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin

    for i in range(img_bin.shape[0]):
        for j in range(20):
            img_bin[i][j] = 0
            img_bin[i][-j] = 0
    for i in range(20):
        for j in range(img_bin.shape[1]):
            img_bin[i][j] = 0
            img_bin[-i][j] = 0

    vertical_lines_img = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(
        vertical_lines_img, vertical_kernel, iterations=3)
    vertical_lines = cv2.HoughLinesP(
        vertical_lines_img, 1, np.pi / 180, 127, minLineLength=20, maxLineGap=10)

    for line in vertical_lines:
        for x1, y1, x2, y2 in line:
            vertical_lines_img = cv2.line(
                vertical_lines_img, (x1, 0), (x2, vertical_lines_img.shape[0]), (255, 255, 255), 1)

    horizontal_lines_img = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(
        horizontal_lines_img, horizontal_kernel, iterations=3)
    horizontal_lines = cv2.HoughLinesP(
        horizontal_lines_img, 2, np.pi / 180, 127, minLineLength=20, maxLineGap=10)
    for line in horizontal_lines:
        for x1, y1, x2, y2 in line:
            horizontal_lines_img = cv2.line(
                horizontal_lines_img, (0, y1), (horizontal_lines_img.shape[1], y2), (255, 255, 255), 1)

    grid_img = cv2.bitwise_and(
        vertical_lines_img, horizontal_lines_img)
    grid_img = cv2.dilate(grid_img, general_kernel, iterations=3)
    grid_img = cv2.erode(grid_img, general_kernel, iterations=1)
    _, grid_img = cv2.threshold(
        grid_img, 127, 255, cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        grid_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted_counter(contours)

    rows = []
    for contour in range(len(contours) - 1):
        x1, y1, w1, h1 = cv2.boundingRect(contours[contour])
        x2, y2, w2, h2 = cv2.boundingRect(contours[contour + 1])
        rows.append(y1)
        if (x1 != x2):
            break

    N = len(rows)
    M = len(contours) // N
    grid = []

    for x in range(1, N - 1):
        grid_row = []

        for y in range(0, M - 1):
            if y == 1 or y == 2:
                continue

            x1, y1, w1, h1 = cv2.boundingRect(contours[x + y * N])
            x2, y2, w2, h2 = cv2.boundingRect(contours[x + y * N + 1])
            x3, y3, w3, h3 = cv2.boundingRect(contours[x + (y + 1) * N + 1])

            grid_row.append(img[y1 + h1: y3, x2 + w2: x3])

        grid.append(grid_row)

    return grid
