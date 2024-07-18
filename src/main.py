import tkinter as tk
import random

class MergeSortVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Merge Sort Visualizer")
        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')
        self.canvas.pack()
        self.data = []

    def generate_data(self):
        self.data = [random.randint(10, 100) for _ in range(50)]
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
        # Implement merge sort algorithm
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MergeSortVisualizer(root)

    # Create buttons or menu items for user interaction
    generate_button = tk.Button(root, text="Generate Data", command=app.generate_data)
    generate_button.pack()

    root.mainloop()
