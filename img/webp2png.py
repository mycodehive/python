import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PIL import Image

class WebPtoPNGConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WebP to PNG Converter")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()
        
        self.label = QLabel("Select a WebP file to convert", self)
        layout.addWidget(self.label)
        
        self.btn_select = QPushButton("Select WebP File", self)
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)
        
        self.btn_convert = QPushButton("Convert to PNG", self)
        self.btn_convert.setEnabled(False)
        self.btn_convert.clicked.connect(self.convert_to_png)
        layout.addWidget(self.btn_convert)
        
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        self.webp_file = ""
    
    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select WebP File", "", "WebP Images (*.webp)")
        
        if file_path:
            self.webp_file = file_path
            self.label.setText(f"Selected: {os.path.basename(file_path)}")
            self.btn_convert.setEnabled(True)
    
    def convert_to_png(self):
        if not self.webp_file:
            return
        
        try:
            img = Image.open(self.webp_file)
            png_path = os.path.splitext(self.webp_file)[0] + ".png"
            img.save(png_path, "PNG")
            self.status_label.setText(f"Converted: {os.path.basename(png_path)}")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebPtoPNGConverter()
    window.show()
    sys.exit(app.exec())
