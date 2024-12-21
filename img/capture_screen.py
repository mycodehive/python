"""
Description : This script captures a region of the screen based on user input.
Location : https://github.com/sahuni/python
Date : 2024.12.21
"""
import pyautogui
import tkinter as tk
from tkinter import simpledialog
import pyscreeze  # Ensure pyscreeze is imported
from PIL import Image  # Ensure PIL is imported ==> pip install Pillow

def capture_screen_region():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Ask user for the region to capture
    x = simpledialog.askinteger("Input", "Enter X coordinate:")
    y = simpledialog.askinteger("Input", "Enter Y coordinate:")
    width = simpledialog.askinteger("Input", "Enter width:")
    height = simpledialog.askinteger("Input", "Enter height:")

    if x is not None and y is not None and width is not None and height is not None:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save("captured_region.png")
        print("Screenshot saved as captured_region.png")
    else:
        print("Invalid input. Screenshot not taken.")

if __name__ == "__main__":
    capture_screen_region()