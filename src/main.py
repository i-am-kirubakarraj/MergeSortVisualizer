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
        if len(self.data) > 1:
            mid = len(self.data) // 2
            left_half = self.data[:mid]
            right_half = self.data[mid:]

            # Recursive calls to divide and sort each half
            self.data = self.merge_sort_helper(left_half)
            self.data = self.merge_sort_helper(right_half)

            # Merge sorted halves
            merged_data = []
            i = j = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    merged_data.append(left_half[i])
                    i += 1
                else:
                    merged_data.append(right_half[j])
                    j += 1
            
            # Append remaining elements
            merged_data.extend(left_half[i:])
            merged_data.extend(right_half[j:])

            # Update data and visualize
            self.data = merged_data
            self.draw_data(self.data, ['green' for _ in range(len(self.data))])

    def merge_sort_helper(self, arr):
        # Base case for recursion
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left_half = self.merge_sort_helper(arr[:mid])
        right_half = self.merge_sort_helper(arr[mid:])

        return self.merge(left_half, right_half)

    def merge(self, left, right):
        merged = []
        while left and right:
            if left[0] < right[0]:
                merged.append(left.pop(0))
            else:
                merged.append(right.pop(0))
        merged.extend(left or right)
        return merged


if __name__ == "__main__":
    root = tk.Tk()
    app = MergeSortVisualizer(root)

    # Create buttons or menu items for user interaction
    generate_button = tk.Button(root, text="Generate Data", command=app.generate_data)
    generate_button.pack()

    root.mainloop()

