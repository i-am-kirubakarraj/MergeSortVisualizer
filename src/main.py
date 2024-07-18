import tkinter as tk
from tkinter import messagebox
import ctypes
import random
import time
import threading

# Load the shared library
if ctypes.sizeof(ctypes.c_voidp) == 4:
    merge_sort_lib = ctypes.CDLL('./merge_sort.dll')
else:
    merge_sort_lib = ctypes.CDLL('./merge_sort.so')

merge_sort_lib.merge_sort.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)

class MergeSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Merge Sort Visualizer")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg='white')
        self.canvas.pack()

        self.entry = tk.Entry(self.frame, width=50)
        self.entry.pack(pady=5)
        self.entry.insert(0, 'Enter numbers separated by commas')

        self.sort_button = tk.Button(self.frame, text='Sort', command=self.start_sorting)
        self.sort_button.pack(pady=5)

        self.result_var = tk.StringVar()
        self.result_label = tk.Label(self.frame, textvariable=self.result_var)
        self.result_label.pack(pady=5)

        self.data = []
        self.is_sorting = False

    def generate_data(self):
        self.data = [random.randint(10, 100) for _ in range(10)]
        self.draw_data(self.data, ['blue' for _ in range(len(self.data))])

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_width = 800
        c_height = 400
        x_width = c_width / (len(data) + 1)
        offset = 30
        spacing = 10
        normalized_data = [i / max(data) for i in data]
        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * 340
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
        self.root.update_idletasks()

    def merge_sort(self):
        self.is_sorting = True
        arr_type = ctypes.c_int * len(self.data)
        c_array = arr_type(*self.data)

        def merge_sort_thread():
            merge_sort_lib.merge_sort(c_array, 0, len(self.data) - 1)
            self.data = list(c_array)
            self.is_sorting = False

        threading.Thread(target=merge_sort_thread).start()
        self.visualize_sort()

    def visualize_sort(self):
        while self.is_sorting:
            self.draw_data(self.data, ['green' if i < 2 else 'blue' for i in range(len(self.data))])
            time.sleep(0.5)

        self.draw_data(self.data, ['green' for _ in range(len(self.data))])
        self.result_var.set(f'Sorted Array: {self.data}')

    def start_sorting(self):
        if not self.is_sorting:
            try:
                self.data = list(map(int, self.entry.get().split(',')))
                if len(self.data) < 2:
                    raise ValueError("Please enter at least two numbers.")
                self.merge_sort()
            except Exception as e:
                messagebox.showerror('Error', str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MergeSortVisualizer(root)

    # Create buttons or menu items for user interaction
    generate_button = tk.Button(root, text="Generate Data", command=app.generate_data)
    generate_button.pack()

    root.mainloop()
