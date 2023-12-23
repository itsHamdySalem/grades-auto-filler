import joblib
import cv2
import numpy as np

svm_model_filename_digit = "svm_model_digits.joblib"
svm_model_filename_symbol = "svm_model_symbols.joblib"
loaded_svm_model_digit = joblib.load(svm_model_filename_digit)
loaded_svm_model_symbol = joblib.load(svm_model_filename_symbol)


target_img_size = (32, 32)
def extract_hog_features(img):
    img = cv2.resize(img, dsize=target_img_size)
    win_size = (32, 32)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)
    
    block_size = (block_size_in_cells[1] * cell_size[1], block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9
    hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()



def predict_digit(img):
    hog_features = extract_hog_features(img)
    if hog_features is None:
        return ""
    cv2.imshow("image", img)
    cv2.waitKey(0)
    hog_features = hog_features.reshape(1, -1)

    prediction = loaded_svm_model_digit.predict(hog_features)
    return prediction[0]

def predict_symbol(img):

    hog_features = extract_hog_features(img)
    hog_features = hog_features.reshape(1, -1)

    prediction = loaded_svm_model_symbol.predict(hog_features)
    return prediction[0]



def segement(img):
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr))
    white_img_large_contours = np.ones(img.shape)
    dimensions_contours = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if(w*h > 50):
            dimensions_contours.append((x, y, w, h))
            cv2.rectangle(white_img_large_contours,(x, y), (x+w, y+h), (0, 0, 255), 3)
    return dimensions_contours, img


def getIdFromImage(img):
    img = cv2.resize(img, (128, 64))
    cv2.imshow("image", img)
    cv2.waitKey(0)
    segmented_dimensions, filtered_img = segement(img)
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
