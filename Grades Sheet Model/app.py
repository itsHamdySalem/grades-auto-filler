import cv2
from paper_extraction import extract_paper_region
from grid_extraction import extract_grid
from grid_data_extraction import extract_data_from_grid
from grades_sheet_generation import generate_excel_sheet

img_path = "Grades Sheet Model/Test Cases/1.jpg"
input_img = cv2.imread(img_path, cv2.IMREAD_COLOR)

extracted_paper_img = extract_paper_region(input_img=input_img, iterations=1)

extracted_grid = extract_grid(extracted_paper_img)

extracted_data_from_grid = extract_data_from_grid(extracted_grid)

generate_excel_sheet(extracted_data_from_grid)
