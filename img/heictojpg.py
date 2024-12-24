"""
Description : convert HEIC to JPEG
Location : https://github.com/sahuni/python
Date : 2024.12.20
"""

import os
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

# dircetory setting
input_dir = "C:\\Users\\aaa\\Downloads\\2023\\2023"
output_dir = os.path.join(input_dir, "converted")

os.makedirs(output_dir, exist_ok=True)

# convert HEIC to JPEG
for file_name in os.listdir(input_dir):
    if file_name.lower().endswith(".heic"):
        heic_path = os.path.join(input_dir, file_name)
        # List of convertible extensions
        valid_extensions = [".heic", ".HEIC"]

        # Handle file extensions case-insensitively
        if any(file_name.endswith(ext) for ext in valid_extensions):
            jpeg_path = os.path.join(output_dir, file_name.rsplit(".", 1)[0] + ".jpg")

        image = Image.open(heic_path) #Successfully opens HEIC files and converts them to Pillow image objects.
        image.save(jpeg_path, "JPEG")

        print(f"Converted {file_name} to {jpeg_path}")
