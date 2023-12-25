from paper_extraction import *
import sys

def count_good_pixels(image, a, b, th = 180):
    cnt = 0
    for y in range(a-25, a+26):
        for x in range(b-25, b+26):
            if image[x, y] < th: cnt+=255-image[x, y]
    return cnt

def extract_id(colored, gray):
    edged = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(edged, 20, 70)
    detected_circles = cv2.HoughCircles(edged,
                    cv2.HOUGH_GRADIENT, 1, 20, param1 = 70,
                param2 = 20, minRadius = 25, maxRadius = 35)
    detected_circles = np.uint16(np.around(detected_circles)) 

    if detected_circles is None:
        print("Error: Something went wrong during extracting the ID.")
        sys.exit(1)

    circles = []  
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        circles.append((a, b, r))
    print(len(circles)) 

    # Sort regarding to Y
    circles =  sorted(
        circles,
        key=lambda t: t[1]
    )
    if (len(circles)) > 1: # handling if the D in ID is considered as a circle so just neglect it
        if abs(circles[0][1]-circles[1][1]) > 40:
            circles = circles[1:]
    
    id = ""
    for i in range(len(circles)//10) :
        currentRow = circles[i*10:i*10+10]
        currentRow = sorted(currentRow, key=lambda t: t[0])
        mx = 0
        dig = 0
        for j in range (len(currentRow)):
            [a, b, r] = currentRow[j]
            cnt = count_good_pixels(gray, a, b)
            if cnt > mx: 
                mx = cnt
                dig = j
        [a, b, r] = currentRow[dig]
        cv2.circle(colored, (a, b), r, (0, 255, 0), 2)
        id+=str(dig)
                
    return id

    
img_BGR = cv2.imread("./samples/11.jPG", cv2.IMREAD_COLOR)
colored, grayed = extract_paper_region(img_BGR)
answers_section_gray = grayed[grayed.shape[0]//3 : (grayed.shape[0]-grayed.shape[0]//10), grayed.shape[1]//10 : (grayed.shape[1]-grayed.shape[1]//10)]
answers_section_colored = colored[colored.shape[0]//3 : (colored.shape[0]-colored.shape[0]//10), colored.shape[1]//10 : (colored.shape[1]-colored.shape[1]//10)]

id_section_gray = grayed[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]
id_section_colored = colored[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]

id = extract_id(id_section_colored, id_section_gray)
print(id)

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