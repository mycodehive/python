# https://github.com/UB-Mannheim/tesseract/wiki

import pytesseract
from PIL import Image

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Image file path
image_path = input("Enter the image file path: ")  # Enter the image file path

# Open the image
image = Image.open(image_path)

# Extract text
extracted_text = pytesseract.image_to_string(image, lang='eng+kor')  # Set language (e.g., English+Korean)

# Print the result
print("=== Extracted Text ===")
print(extracted_text)

# Save the text to a file
with open('extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(extracted_text)
