import openpyxl
from openpyxl.styles import PatternFill


def generate_excel_sheet(data=[], file_path='Grades Sheet Model/grades_sheet.xlsx'):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for i, row_data in enumerate(data):
        for j, value in enumerate(row_data):
            if value == -1:
                continue
            elif value == -2:
                cell = sheet.cell(row=i + 1, column=j + 1, value="")
                cell.fill = PatternFill(
                    start_color="FF0000", end_color="FF0000", fill_type='solid')
            else:
                sheet.cell(row=i + 1, column=j + 1, value=value)
    workbook.save(file_path)
