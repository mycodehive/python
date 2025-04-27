"""
Description : This script converts MP4 files to Live Photos for iPhone.
Location : https://github.com/sahuni/python
Date : 2025.01.13
"""

# pip install moviepy pillow pyheif
# https://exiftool.org/

import os, re
import subprocess
import uuid
import cv2
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QProgressBar
)
from PySide6.QtCore import QThread, Signal
from PIL import Image
import pillow_heif

# 변환 작업을 별도 스레드에서 실행
class ConverterThread(QThread):
    progress = Signal(str)
    finished = Signal()

    def __init__(self, files, output_dir):
        super().__init__()
        self.files = files
        self.output_dir = output_dir

    def run(self):
        for file in self.files:
            self.convert_mp4_to_live_photo(file)
        self.finished.emit()

    def sanitize_filename(self, name):
        """파일명에서 특수문자 제거 및 공백 처리"""
        name = re.sub(r'[\\/*?:"<>|]', "_", name)  # 특수문자 제거
        name = name.replace(" ", "_")              # 공백 → 밑줄
        return name

    def generate_asset_identifier(self):
        return str(uuid.uuid4())
    
    def exedir(self, mode="script"):
        if getattr(sys, 'frozen', False):  # PyInstaller로 빌드된 경우
            return os.path.dirname(sys.executable)  # 실행 파일의 디렉토리
        elif mode == "cwd":
            return os.getcwd()
        elif mode == "script":
            return os.path.dirname(os.path.abspath(__file__))
        else:
            raise ValueError("Invalid mode. Use 'cwd', 'exe', or 'script'.")

    def extract_cover_image(self, mp4_path, output_path):
        """OpenCV로 MP4에서 첫 프레임 추출"""
        cap = cv2.VideoCapture(mp4_path)
        success, frame = cap.read()
        if success:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image.save(output_path)
            self.progress.emit(f"[{os.path.basename(mp4_path)}] 대표 이미지 추출 완료.")
        else:
            self.progress.emit(f"[{os.path.basename(mp4_path)}] 대표 이미지 추출 실패.")
        cap.release()

    def convert_to_heic(self, jpg_path, heic_path):
        """JPG → HEIC 변환 (pillow-heif 사용)"""
        image = Image.open(jpg_path)
        heif_file = pillow_heif.from_pillow(image)
        heif_file.save(heic_path)
        self.progress.emit(f"{os.path.basename(heic_path)} 변환 완료 (HEIC).")

    def convert_to_mov(self, mp4_path, mov_path):
        """MP4 → MOV 변환 (3초 제한)"""
        ffmpeg_path = r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe"  # ffmpeg.exe의 전체 경로
        subprocess.run([ffmpeg_path, '-i', mp4_path, '-t', '3', '-c:v', 'hevc', '-an', '-vf', 'scale=1080:1920', mov_path], shell=True)
        self.progress.emit(f"{os.path.basename(mov_path)} 변환 완료 (3초 제한).")

    def add_metadata(self, heic_path, mov_path, asset_id):
        currendir = self.exedir("script")
        exiftool_path = os.path.join(currendir, "exiftool.exe")  # exiftool 설치 경로
        """HEIC와 MOV 파일 연결 (Asset Identifier 추가)"""
        subprocess.run([exiftool_path, f'-AssetIdentifier={asset_id}', '-overwrite_original', heic_path], shell=True)
        subprocess.run([exiftool_path, f'-AssetIdentifier={asset_id}', '-overwrite_original', mov_path], shell=True)
        self.progress.emit(f"메타데이터 추가 완료 (Asset ID: {asset_id})")

    def send_to_iphone(self, files):
        """Windows에서 변환된 파일 폴더 열기"""
        folder = os.path.dirname(files[0])
        subprocess.run(['explorer', folder])
        self.progress.emit("파일 변환이 완료되었습니다. 폴더를 열었습니다.")

    def send_to_iphone_mac(self, files):
        """AirDrop으로 iPhone 전송"""
        for file in files:
            subprocess.run(['osascript', '-e', f'tell application "Finder" to open POSIX file "{file}"'])
        self.progress.emit("AirDrop 전송 준비 완료. iPhone에서 수락하세요!")

    def convert_mp4_to_live_photo(self, mp4_path):
        """MP4 파일을 Live Photo로 변환"""
        file_name = os.path.splitext(os.path.basename(mp4_path))[0]
        safe_name = self.sanitize_filename(file_name)  # 파일명 안전하게 변환
        output_folder = os.path.join(self.output_dir, safe_name)
        os.makedirs(output_folder, exist_ok=True)

        jpg_path = os.path.join(output_folder, 'cover.jpg')
        heic_path = os.path.join(output_folder, 'cover.heic')
        mov_path = os.path.join(output_folder, 'live.mov')
        asset_id = self.generate_asset_identifier()

        self.extract_cover_image(mp4_path, jpg_path)
        self.convert_to_heic(jpg_path, heic_path)
        self.convert_to_mov(mp4_path, mov_path)
        self.add_metadata(heic_path, mov_path, asset_id)
        self.send_to_iphone([heic_path, mov_path])

        self.progress.emit(f"[{file_name}] Live Photo 변환 완료!\n")

# GUI 구성
class LivePhotoConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP4 → Live Photo 변환기 (OpenCV + Pillow)")
        self.setGeometry(300, 300, 600, 400)

        self.layout = QVBoxLayout()

        self.info_label = QLabel("MP4 파일을 선택하세요.")
        self.layout.addWidget(self.info_label)

        self.select_button = QPushButton("파일 선택")
        self.select_button.clicked.connect(self.select_files)
        self.layout.addWidget(self.select_button)

        self.start_button = QPushButton("변환 시작")
        self.start_button.clicked.connect(self.start_conversion)
        self.layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        self.setLayout(self.layout)
        self.selected_files = []

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "MP4 파일 선택", "", "MP4 Files (*.mp4)")
        if files:
            self.selected_files = files
            self.info_label.setText(f"{len(files)}개의 파일이 선택되었습니다.")

    def start_conversion(self):
        if not self.selected_files:
            self.log_output.append("MP4 파일을 먼저 선택하세요.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "결과 저장 폴더 선택")
        if not output_dir:
            self.log_output.append("결과 저장 폴더를 선택하세요.")
            return

        self.converter_thread = ConverterThread(self.selected_files, output_dir)
        self.converter_thread.progress.connect(self.update_log)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.start()

        self.progress_bar.setMaximum(len(self.selected_files))
        self.progress_bar.setValue(0)
        self.log_output.append("변환을 시작합니다...\n")

    def update_log(self, message):
        self.log_output.append(message)
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def conversion_finished(self):
        self.log_output.append("\n모든 파일의 변환이 완료되었습니다!")

# 프로그램 실행
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LivePhotoConverter()
    window.show()
    sys.exit(app.exec())