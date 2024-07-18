import tkinter as tk
from tkinter import messagebox
import ctypes
import os

# Load the shared library
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

def on_sort():
    try:
        global sorted_arr, current_step
        arr = list(map(int, entry.get().split(',')))
        sorted_arr = merge_sort(arr)
        current_step = 0
        visualize_sort()
    except Exception as e:
        messagebox.showerror('Error', str(e))

def visualize_sort():
    global current_step
    if current_step < len(sorted_arr):
        result_var.set(f'Step {current_step + 1}: {sorted_arr[:current_step + 1]}')
        current_step += 1
        app.after(1000, visualize_sort)  # Adjust delay as needed for visualization speed
    else:
        result_var.set(f'Sorted Array: {sorted_arr}')

app = tk.Tk()
app.title('Merge Sort Visualizer')

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=50)
entry.pack(pady=5)
entry.insert(0, 'Enter numbers separated by commas')

sort_button = tk.Button(frame, text='Sort', command=on_sort)
sort_button.pack(pady=5)

result_var = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_var)
result_label.pack(pady=5)

app.mainloop()

