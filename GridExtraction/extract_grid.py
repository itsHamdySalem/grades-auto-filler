import cv2
import numpy as np


def extract_grid(img):
    # Convert image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Image Thresholding
    _, img_bin = cv2.threshold(
        img_gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Image Inversion
    img_bin = 255 - img_bin

    # kernel length
    kernel_length = np.array(img).shape[1] // 33
    # vertical kernel : to detect vertical lines
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, kernel_length))
    # horizontal kernel : to detect horizontal lines
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (kernel_length, 1))
    # general kernel
    general_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Draw vertical lines
    img_with_vertical_lines = cv2.erode(img_bin, vertical_kernel, iterations=3)
    img_with_vertical_lines = cv2.dilate(
        img_with_vertical_lines, vertical_kernel, iterations=3)
    vertical_lines = cv2.HoughLinesP(
        img_with_vertical_lines, 1, np.pi / 180, 40, minLineLength=10, maxLineGap=20)
    for line in vertical_lines:
        for x1, y1, x2, y2 in line:
            img_with_vertical_lines = cv2.line(
                img_with_vertical_lines, (x1, 0), (x2, img_with_vertical_lines.shape[0]), (255, 255, 255), 1)
    cv2.imwrite('./results/img_with_vertical_lines.jpg',
                img_with_vertical_lines)

    # Draw horizontal lines
    horizontal_lines_img = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(
        horizontal_lines_img, horizontal_kernel, iterations=3)
    horizontal_lines = cv2.HoughLinesP(
        horizontal_lines_img, 2, np.pi / 180, 40, minLineLength=5, maxLineGap=10)
    for line in horizontal_lines:
        for x1, y1, x2, y2 in line:
            horizontal_lines_img = cv2.line(
                horizontal_lines_img, (0, y1), (horizontal_lines_img.shape[1], y2), (255, 255, 255), 1)
    cv2.imwrite('./results/horizontal_lines_img.jpg',
                horizontal_lines_img)

    # Combine vertical and horizontal lines
    output_img = cv2.bitwise_and(
        img_with_vertical_lines, horizontal_lines_img)
    # Erode the image
    output_img = cv2.erode(~output_img, general_kernel, iterations=3)
    # Thresholding
    _, output_img = cv2.threshold(
        output_img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    cv2.imwrite('./results/grid_points_img.jpg', output_img)

    cv2.waitKey(0)


if __name__ == '__main__':
    img = cv2.imread('test.jpg')
    extract_grid(img)
