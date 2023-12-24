import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from grid_extraction import extract_grid
from paper_extraction import extract_paper_region
from grid_data_extraction import extract_data_from_grid
from grades_sheet_generation import generate_excel_sheet


class AppConfig:
    BG_COLOR = '#F0F0F0'
    LABEL_BG_COLOR = '#F0F0F0'
    BUTTON_BG_COLOR = '#D3D3D3'
    IMAGE_RESIZE_DIMENSIONS = (256, 512)
    LARGE_FONT = ('times', 20, 'bold')
    SMALL_FONT = ('times', 12, 'bold')


class GradesSheetApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("724x480")
        self.window.title('Grades Sheet Model')
        self.setup_gui()

    def setup_gui(self):
        self.window.configure(bg=AppConfig.BG_COLOR)
        self.center_window()

        upload_label = tk.Label(
            self.window, text='Upload your sheet', font=AppConfig.LARGE_FONT, background=AppConfig.LABEL_BG_COLOR)
        upload_label.pack(side="top", fill="both", pady=(50, 20))

        upload_button = tk.Button(self.window, text='Upload image',
                                  background=AppConfig.BUTTON_BG_COLOR, width=20, command=self.upload_file)
        upload_button.pack(side="top", pady=20)

        self.results_label = tk.Label(
            self.window, text='', font=AppConfig.SMALL_FONT, background=AppConfig.LABEL_BG_COLOR)
        self.results_label.pack(side="top", fill="both", pady=(50, 20))

    def center_window(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width - 724) / 2)
        y_coordinate = int((screen_height - 480) / 2)
        self.window.geometry(f"724x480+{x_coordinate}+{y_coordinate}")

    def upload_file(self):
        try:
            file_types = [('Jpg Files', '*.jpg')]
            selected_files = filedialog.askopenfilename(
                multiple=True, filetypes=file_types, title='Select Image Files')

            col_position = 1
            row_position = 9
            self.results_label.config(text='Wait Results....')

            for file_path in selected_files:
                excel_buffer = self.process_image(file_path)
                self.display_excel(excel_buffer)

        except Exception as error:
            messagebox.showerror('Error', f"An error occurred: {error}")

    def process_image(self, image_path):
        try:
            input_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            extracted_paper_image = extract_paper_region(
                input_img=input_image, iterations=1)
            extracted_grid = extract_grid(extracted_paper_image)
            extracted_data_from_grid = extract_data_from_grid(extracted_grid)
            excel_buffer = generate_excel_sheet(extracted_data_from_grid)
            return excel_buffer

        except Exception as error:
            messagebox.showerror('Error', f"Error processing image: {error}")

    def display_excel(self, excel_buffer):
        try:
            df = pd.read_excel(excel_buffer, engine='openpyxl')

            df = df.applymap(lambda x: str(x) if pd.notna(
                x) and not isinstance(x, (int)) else x)

            top = tk.Toplevel(self.window)
            top.title("Excel Sheet Snapshot")

            def handle_results_window_close():
                top.destroy()
                self.results_label.config(text='')

            top.protocol("WM_DELETE_WINDOW", handle_results_window_close)

            tree = ttk.Treeview(top, columns=list(df.columns), show='headings')
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='c')

            for index, row in df.iterrows():
                values = row.to_list()
                tree.insert("", "end", values=values)

            tree.pack(expand=tk.YES, fill=tk.BOTH)

            self.results_label.config(text='Processing is completed')

            top.wait_window(top)

        except Exception as error:
            messagebox.showerror(
                'Error', f"Error displaying Excel sheet: {error}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = GradesSheetApp()
    app.run()
