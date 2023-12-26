from utils import *
import cv2
import numpy as np
from check_circle import *
import sys

def get_answers_for_partition(colored, gray, model_answers = None):
    edged = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(edged, 20, 70)

    detected_circles = cv2.HoughCircles(edged,
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 15, minRadius = 13, maxRadius = 20)
    if detected_circles is None:
        print("This partition is empty and has no questions.")
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
    number_of_choices = 0
    for i in range(len(circles)):
        if abs(circles[0][1]-circles[i][1]) < 40: number_of_choices+=1

    answers = []
    for i in range(len(circles)//number_of_choices) :
        currentRow = circles[i*number_of_choices:(1+i)*number_of_choices]
        currentRow = sorted(currentRow, key=lambda t: t[0])
        mx = 0
        dig = 0 
        for j in range (len(currentRow)):
            [a, b, r] = currentRow[j]
            cnt = count_good_pixels(gray, a, b)
            if cnt > mx: 
                mx = cnt
                dig = j
        answers.append(dig)
        [a, b, r] = currentRow[dig]
        if (model_answers is not None):
            if model_answers[len(answers)-1] == dig: cv2.circle(colored, (a, b), r, (0, 255, 0), 2)
            else: cv2.circle(colored, (a, b), r, (0, 0, 255), 2)
    return [colored, answers]

def get_answers(colored, gray, model_answers = None): # returns the image after circling all the answers and also an array of answers
    answers = []
    for i in range (3) : 
       model_answers_part = None
       if model_answers is not None and len(model_answers) > i: model_answers_part = model_answers[i]
       # split it into three sections to handle the worst case, when the number of questions is maximum possible
       cur = get_answers_for_partition(colored[0 : colored.shape[0], i*colored.shape[1]//3 : (1+i)*colored.shape[1]//3],
                                       gray[0 : gray.shape[0], i*gray.shape[1]//3 : (1+i)*gray.shape[1]//3],
                                       model_answers_part)
       if cur is None:
           continue
       colored[0 : colored.shape[0], i*colored.shape[1]//3 : (1+i)*colored.shape[1]//3] = cur[0]
       answers.append(cur[1])
    return [colored, answers]