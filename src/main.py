import tkinter as tk
from tkinter import messagebox
import ctypes
import time

# Load the shared library
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
if os.name == 'nt':
    merge_sort_lib = ctypes.CDLL(os.path.join(current_dir, 'merge_sort.dll'))
elif os.name == 'posix':
    merge_sort_lib = ctypes.CDLL(os.path.join(current_dir, 'merge_sort.so'))
else:
    raise OSError('Unsupported operating system')

merge_sort_lib.merge_sort.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int)

def merge_sort(arr):
    arr_type = ctypes.c_int * len(arr)
    c_array = arr_type(*arr)
    merge_sort_lib.merge_sort(c_array, 0, len(arr) - 1)
    return list(c_array)

class MergeSortVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Merge Sort Visualizer')
        self.geometry('800x600')

        self.array = []
        self.sorted_array = []
        self.steps = []
        self.current_step = 0

        self.canvas = tk.Canvas(self, width=800, height=400, bg='white')
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)

        self.info_label = tk.Label(self, text='', font=('Arial', 12))
        self.info_label.pack(pady=10)

        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.insert(0, 'Enter numbers separated by commas')

        self.sort_button = tk.Button(self, text='Sort', command=self.start_sorting)
        self.sort_button.pack(pady=5)

        self.next_button = tk.Button(self, text='Next Step', command=self.next_step, state=tk.DISABLED)
        self.next_button.pack(pady=5)

    def start_sorting(self):
        try:
            self.array = list(map(int, self.input_entry.get().split(',')))
            self.sorted_array = merge_sort(self.array.copy())
            self.steps = self.merge_sort_steps(self.array.copy())
            self.current_step = 0
            self.draw_array(self.array)
            self.next_button.config(state=tk.NORMAL)
            self.sort_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def merge_sort_steps(self, arr):
        steps = []
        self.merge_sort_recursive(arr, 0, len(arr) - 1, steps)
        return steps

    def merge_sort_recursive(self, arr, left, right, steps):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort_recursive(arr, left, mid, steps)
            self.merge_sort_recursive(arr, mid + 1, right, steps)
            self.merge(arr, left, mid, right, steps)

    def merge(self, arr, left, mid, right, steps):
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            steps.append(arr.copy())
            k += 1

        while i < len(L):
            arr[k] = L[i]
            steps.append(arr.copy())
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            steps.append(arr.copy())
            j += 1
            k += 1

    def draw_array(self, arr):
        self.canvas.delete(tk.ALL)
        bar_width = 800 / len(arr)
        bar_height_ratio = 400 / max(arr) if arr else 1
        for i, num in enumerate(arr):
            x0 = i * bar_width
            y0 = 400
            x1 = (i + 1) * bar_width
            y1 = 400 - num * bar_height_ratio
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue')
            self.canvas.create_text((x0 + x1) / 2, y0 + 10, text=str(num))
        self.update_idletasks()

    def next_step(self):
        if self.current_step < len(self.steps):
            self.draw_array(self.steps[self.current_step])
            self.info_label.config(text=f'Step {self.current_step + 1}: Sorting...')
            self.current_step += 1
            if self.current_step == len(self.steps):
                self.next_button.config(state=tk.DISABLED)
                self.info_label.config(text='Sorting Complete!')
        else:
            self.next_button.config(state=tk.DISABLED)

if __name__ == '__main__':
    app = MergeSortVisualizer()
    app.mainloop()

