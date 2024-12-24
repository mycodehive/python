import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

class HEICtoJPEGConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('HEIC to JPEG Converter')
        self.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()

        self.select_button = QPushButton('Select Source Folder')
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)

        self.convert_button = QPushButton('Convert HEIC to JPEG')
        self.convert_button.clicked.connect(self.convert_files)
        layout.addWidget(self.convert_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def select_folder(self):
        self.input_dir = QFileDialog.getExistingDirectory(self, 'Select Source Folder')
        if self.input_dir:
            self.log_output.append(f'Selected folder: {self.input_dir}')

    def convert_files(self):
        if not hasattr(self, 'input_dir'):
            self.log_output.append('Please select a source folder first.')
            print("Select Source Folder")
            return

        output_dir = os.path.join(self.input_dir, "converted")
        os.makedirs(output_dir, exist_ok=True)

        for file_name in os.listdir(self.input_dir):
            if file_name.lower().endswith(".heic"):
                heic_path = os.path.join(self.input_dir, file_name)
                jpeg_path = os.path.join(output_dir, file_name.rsplit(".", 1)[0] + ".jpg")

                image = Image.open(heic_path)
                image.save(jpeg_path, "JPEG")

                self.log_output.append(f'Converted {file_name} to {jpeg_path}')

        self.log_output.append('Conversion completed.')
        os.startfile(output_dir)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = HEICtoJPEGConverter()
    converter.show()
    sys.exit(app.exec_())