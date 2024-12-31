"""
Description: Extract text from images using OCR
Location: https://github.com/sahuni/python
Date: 2024.12.31
"""
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
import pytesseract
from PIL import Image

class ImageTextExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Left layout: Image loading and display
        left_layout = QVBoxLayout()
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.image_label = QLabel("Image will be displayed here.")
        self.image_label.setFixedSize(400, 500)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.load_button, alignment=Qt.AlignTop)
        left_layout.addWidget(self.image_label, alignment=Qt.AlignTop)
        left_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Right layout: Extract text and text display
        right_layout = QVBoxLayout()
        self.extract_button = QPushButton("Extract")
        self.extract_button.clicked.connect(self.extract_text)
        self.extract_button.setEnabled(False)
        self.text_area = QTextEdit()
        self.text_area.setFixedSize(400, 500)
        self.text_area.setPlaceholderText("Extracted text will be displayed here.")
        right_layout.addWidget(self.extract_button, alignment=Qt.AlignTop)
        right_layout.addWidget(self.text_area, alignment=Qt.AlignTop)
        right_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Combine layouts
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Image Text Extractor")
        self.setGeometry(100, 100, 800, 500)

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)", options=options)
        
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), aspectRatioMode=Qt.KeepAspectRatio))
            self.extract_button.setEnabled(True)

    def extract_text(self):
        if hasattr(self, 'image_path'):
            try:
                # Set Tesseract path
                pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Modify the path as needed

                image = Image.open(self.image_path)
                extracted_text = pytesseract.image_to_string(image, lang='kor+eng')  # Support for Korean and English
                self.text_area.setPlainText(extracted_text)
            except Exception as e:
                self.text_area.setPlainText(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageTextExtractor()
    window.show()
    sys.exit(app.exec_())