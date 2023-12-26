import cv2
import joblib
import numpy as np
from utils import *
from PIL import Image
import pytesseract

svm_model_filename_digit = "Grades Sheet Model/svm_model_digits.joblib"
svm_model_filename_symbol = "Grades Sheet Model/svm_model_symbols.joblib"

loaded_svm_model_digit = joblib.load(svm_model_filename_digit)
loaded_svm_model_symbol = joblib.load(svm_model_filename_symbol)

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


def extract_hog_features(img, target_img_size=(32, 32)):
    if img is None or img.size == 0:
        return None
    img = cv2.resize(img, dsize=target_img_size)
    win_size = (32, 32)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)

    block_size = (block_size_in_cells[1] * cell_size[1],
                  block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9
    hog = cv2.HOGDescriptor(win_size, block_size,
                            block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()


def predict_digit(img, isOCRDigit=0):
    if isOCRDigit:
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        return pytesseract.image_to_string(
            img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    else:
        hog_features = extract_hog_features(img)
        if hog_features is None:
            return ""
        hog_features = hog_features.reshape(1, -1)
        prediction = loaded_svm_model_digit.predict(hog_features)
        return prediction[0]


def predict_symbol(img):
    hog_features = extract_hog_features(img)
    hog_features = hog_features.reshape(1, -1)
    prediction = loaded_svm_model_symbol.predict(hog_features)
    return prediction[0]


def segment(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    contours, hierarchy = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr))
    white_img_large_contours = np.zeros(
        img.shape, dtype=np.uint8)  # Fixed line
    dimensions_contours = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if w * h > 50:
            dimensions_contours.append((x, y, w, h))
            cv2.rectangle(white_img_large_contours, (x, y),
                          (x+w, y+h), (0, 0, 255), 3)
    return dimensions_contours, img


def getIdFromImage(img, isOCR=0):
    if isOCR:
        return pytesseract.image_to_string(img)
    else:
        img = cv2.resize(img, (128, 64))
        segmented_dimensions, filtered_img = segment(img)
        cropped_digits = []
        i = 0
        for dimension in segmented_dimensions:
            (x, y, w, h) = dimension
            cropped_digits.append(filtered_img[y-1:y+h+1, x-1:x+w+1])
            i += 1
        predictions = []
        for img in cropped_digits:
            predictions.append(predict_digit(img))
        predictedNumber = ""
        for number in predictions:
            predictedNumber += str(number)
        return predictedNumber


def string_to_value(s):
    if s == 'box':
        return 0
    elif s == 'correct':
        return 5
    elif s == 'empty':
        return -1
    elif s.startswith('horizontal') and s[10:].isdigit():
        return 5 - int(s[10:])
    elif s.startswith('vertical') and s[8:].isdigit():
        return int(s[8:])
    elif s == 'question':
        return -2
    else:
        return None


def extract_data_from_grid(grid=[], isOCRID=1, isOCRDigit=0):
    N = len(grid)
    M = len(grid[0])
    data = [["Code", "1", "2", "3"]]

    for x in range(N):
        row_data = []
        for y in range(M):
            if y == 0:
                row_data.append(getIdFromImage(grid[x][y], isOCRID))
            elif y == 1:
                row_data.append(predict_digit(grid[x][y], isOCRDigit))
            else:
                row_data.append(string_to_value(predict_symbol(grid[x][y])))
        data.append(row_data)

    return data
