"""
Description : This script captures a region of the screen based on user input.
Location : https://github.com/sahuni/python
Date : 2024.12.21
"""
import pyautogui
import tkinter as tk
from tkinter import simpledialog
import pyscreeze  # Ensure pyscreeze is imported
from PIL import Image, ImageDraw  # Ensure PIL is imported ==> pip install Pillow

def capture_screen_region():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)

    rect = None
    start_x = start_y = 0

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

    def on_mouse_drag(event):
        nonlocal rect
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        nonlocal start_x, start_y, rect
        end_x, end_y = event.x, event.y
        root.destroy()
        x = min(start_x, end_x)
        y = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)

        if width > 0 and height > 0:
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save("captured_region.png")
            print("Screenshot saved as captured_region.png")
        else:
            print("Invalid region. Screenshot not taken.")

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

if __name__ == "__main__":
    capture_screen_region()