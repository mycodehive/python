"""
Description : remove background from image
Location : https://github.com/sahuni/python
Date : 2025.01.13
"""

import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox, QScrollArea
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt  # Qt 모듈 추가

class BackgroundRemoverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("배경 제거 프로그램")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.image_label = QLabel("이미지를 선택하세요")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)

        self.load_button = QPushButton("이미지 불러오기")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.process_button = QPushButton("배경 제거 실행")
        self.process_button.clicked.connect(self.remove_background)
        self.process_button.setEnabled(False)
        self.layout.addWidget(self.process_button)

        self.setLayout(self.layout)
        self.image_path = None

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), aspectMode=Qt.KeepAspectRatio))
            self.process_button.setEnabled(True)

    def read_image(self, path):
        try:
            img_array = np.fromfile(path, np.uint8)
            image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            QMessageBox.critical(self, "오류", f"이미지를 불러오는 중 오류가 발생했습니다.\n{str(e)}")
            return None

    def remove_background(self):
        if not self.image_path:
            QMessageBox.warning(self, "경고", "이미지를 먼저 선택하세요.")
            return

        image = self.read_image(self.image_path)
        if image is None:
            QMessageBox.critical(self, "오류", "이미지를 불러오지 못했습니다. 지원되지 않는 파일이거나 경로가 잘못되었습니다.")
            return

        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # 이미지 크기에 비례하는 동적 사각형 적용
        height, width = image.shape[:2]
        rect = (int(width * 0.1), int(height * 0.1), int(width * 0.8), int(height * 0.8))
        
        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        # 마스크 후처리 추가 (모폴로지 열림 연산)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        kernel = np.ones((3, 3), np.uint8)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel, iterations=1)
        result = image * mask2[:, :, np.newaxis]

        folder_path = os.path.dirname(self.image_path)
        base_name = os.path.splitext(os.path.basename(self.image_path))[0]
        save_path = os.path.join(folder_path, f"{base_name}_rmbg.png")

        cv2.imencode('.png', result)[1].tofile(save_path)
        
        # 배경 제거된 이미지 자동으로 불러오기
        pixmap = QPixmap(save_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height(), aspectMode=Qt.KeepAspectRatio))

        QMessageBox.information(self, "완료", f"배경 제거 완료!\n저장 경로: {save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundRemoverApp()
    window.show()
    sys.exit(app.exec())
