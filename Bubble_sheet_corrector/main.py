from extract_id import *
from get_answers import *
from paper_extraction import *
import sys

model_answers_path = "./samples/model_test2.jPG"


#get the correct answers
img_BGR = cv2.imread(model_answers_path, cv2.IMREAD_COLOR)
colored, grayed = extract_paper_region(img_BGR)
answers_section_gray = grayed[grayed.shape[0]//3 : (grayed.shape[0]-grayed.shape[0]//10), grayed.shape[1]//10 : (grayed.shape[1]-grayed.shape[1]//10)]
answers_section_colored = colored[colored.shape[0]//3 : (colored.shape[0]-colored.shape[0]//10), colored.shape[1]//10 : (colored.shape[1]-colored.shape[1]//10)]

res = get_answers(answers_section_colored, answers_section_gray)
if res is None:
    print("An Error happened while extracting the correct answers from the model answer!")
    sys.exit(0)

[colored[colored.shape[0]//3 : (colored.shape[0]-colored.shape[0]//10), colored.shape[1]//10 : (colored.shape[1]-colored.shape[1]//10)]
 , model_answers_partitioned] = res

model_image = colored


student_answers_path = "./samples/student_test2.jPG"
    
img_BGR = cv2.imread(student_answers_path, cv2.IMREAD_COLOR)
colored, grayed = extract_paper_region(img_BGR)
answers_section_gray = grayed[grayed.shape[0]//3 : (grayed.shape[0]-grayed.shape[0]//10), grayed.shape[1]//10 : (grayed.shape[1]-grayed.shape[1]//10)]
answers_section_colored = colored[colored.shape[0]//3 : (colored.shape[0]-colored.shape[0]//10), colored.shape[1]//10 : (colored.shape[1]-colored.shape[1]//10)]

id_section_gray = grayed[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]
id_section_colored = colored[0 : grayed.shape[0]//3, grayed.shape[1]//10 : (grayed.shape[1]-5*grayed.shape[1]//12)]

id = extract_id(id_section_colored, id_section_gray)
if id is None:
    print("An Error happened while extracting the student ID!")
    sys.exit(0)

res = get_answers(answers_section_colored, answers_section_gray, model_answers_partitioned)
if res is None:
    print("An Error happened while extracting the answers of the student!")
    sys.exit(0)

[colored[colored.shape[0]//3 : (colored.shape[0]-colored.shape[0]//10), colored.shape[1]//10 : (colored.shape[1]-colored.shape[1]//10)]
 , studnent_answers_partitioned] = res

correct = 0
total = 0
for i in range(len(studnent_answers_partitioned)):
    for j in range(len(studnent_answers_partitioned[i])):
        total+=1
        correct+=studnent_answers_partitioned[i][j] ==  model_answers_partitioned[i][j]

student_image = colored

print(id, correct, total)

show_images([student_image, model_image], ['student', 'model'])
