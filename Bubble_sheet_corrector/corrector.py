from paper_extraction import *

def is_filled(image, A, thresh_1, thresh_2):
    Ax0 = A[0] - 5
    Ay0 = A[1] - 5
    Ax1 = A[0] + 5
    Ay1 = A[1] + 5
    circleImage = image[Ay0:Ay1,Ax0:Ax1]
    circleImage[circleImage < thresh_1] = 0
    sumPixels = np.sum(circleImage)
    return sumPixels < thresh_2

def extract_id(colored, gray):
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.Canny(gray, 20, 70)
    detected_circles = cv2.HoughCircles(gray,
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 20, minRadius = 25, maxRadius = 35)
    detected_circles = np.uint16(np.around(detected_circles)) 
    circles = []  
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        circles.append((a, b, r))
        cv2.circle(colored, (a, b), r, (0, 255, 0), 2)
        print(a, b, r)
    print(len(circles)) 
    show_images([colored, gray], ['RGB', 'grayScale'])

    
img_BGR = cv2.imread("./samples/2.jPG", cv2.IMREAD_COLOR)
colored, grayed = extract_paper_region(img_BGR)
answers_section = grayed[grayed.shape[0]//3 : (grayed.shape[0]-grayed.shape[0]//10), grayed.shape[1]//10 : (grayed.shape[1]-grayed.shape[1]//10)]

id_section_gray = grayed[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]
id_section_colored = colored[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]

extract_id(id_section_colored, id_section_gray)

# show_images([img_BGR, grayed, answers_section, id_section], ['original', 'grayScale', 'answer_section', 'id_section'])

# colored = colored[grayed.shape[0]//3:(grayed.shape[0]-grayed.shape[0]//10),grayed.shape[1]//10:(grayed.shape[1]-grayed.shape[1]//10)]
# answers_section = cv2.GaussianBlur(answers_section, (5, 5), 0)
# edged = cv2.Canny(answers_section, 20, 70)
# detected_circles = cv2.HoughCircles(edged,
#                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
#                param2 = 20, minRadius = 25, maxRadius = 35)
# detected_circles = np.uint16(np.around(detected_circles)) 
# circles = []  
# for pt in detected_circles[0, :]:
#     a, b, r = pt[0], pt[1], pt[2]
#     circles.append((a, b, r))
#     cv2.circle(colored, (a, b), r, (0, 255, 0), 2)
#     print(a, b, r)
# print(len(circles)) 

# # Sort regarding to Y
# circles =  sorted(
#     circles,
#     key=lambda t: t[1]
# )
        
# # ID_section = grayed[grayed.shape[0]//3:(grayed.shape[0]-grayed.shape[0]//10),grayed.shape[1]//10:(grayed.shape[1]-grayed.shape[1]//10)]
# show_images([colored, grayed, edged], ['RGB', 'grayScale', 'mb3bsa'])