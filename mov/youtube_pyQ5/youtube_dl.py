"""
Description : Code to download YouTube videos in the highest quality using the PyQt5 module.
Location : https://github.com/sahuni/python
Date : 2024.12.24
"""
# pyuic5 -o youtube_downloader_ui.py youtube_downloader.ui
import subprocess
import os, re, importlib, time, threading
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

def P_From_n_Import(xModule_Name):
    vModule = importlib.import_module(xModule_Name)
    globals().update({n: getattr(vModule, n) for n in dir(vModule)})

def P_Import(xModule_Name):
    return importlib.import_module(xModule_Name)

def F_Is_Exist_Module(xModule_Name):
    return importlib.util.find_spec(xModule_Name) is not None

def long_initialization():
    # Example of a complex initialization task
    time.sleep(3)  # Example: time-consuming task
    print("Initialization complete.")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # YouTube URL Input
        self.label_url = QtWidgets.QLabel(self.centralwidget)
        self.label_url.setText("YouTube URL:")
        self.verticalLayout.addWidget(self.label_url)

        self.lineEdit_url = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.lineEdit_url)

        # FFmpeg Path Input
        self.label_ffmpeg = QtWidgets.QLabel(self.centralwidget)
        self.label_ffmpeg.setText("FFmpeg Path:")
        self.verticalLayout.addWidget(self.label_ffmpeg)

        self.lineEdit_ffmpeg = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.lineEdit_ffmpeg)

        # Download Path Input
        self.label_download_path = QtWidgets.QLabel(self.centralwidget)
        self.label_download_path.setText("Download Path:")
        self.verticalLayout.addWidget(self.label_download_path)

        self.lineEdit_download_path = QtWidgets.QLineEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.lineEdit_download_path)

        # Download Button
        self.pushButton_download = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_download.setText("Download")
        self.verticalLayout.addWidget(self.pushButton_download)

        # Output Text Edit
        self.textEdit_output = QtWidgets.QTextEdit(self.centralwidget)
        self.verticalLayout.addWidget(self.textEdit_output)

        MainWindow.setCentralWidget(self.centralwidget)


class DownloadThread(QThread):
    log_signal = pyqtSignal(str)  # 로그를 GUI로 전달하는 시그널

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW  # 콘솔 창 숨기기
            )

            # 실시간 로그 전달
            for line in iter(process.stdout.readline, ""):
                if line:
                    self.log_signal.emit(line.strip())

            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                self.log_signal.emit("Download completed successfully!")
            else:
                self.log_signal.emit("Error occurred during download.")

        except Exception as e:
            self.log_signal.emit(f"Unexpected error: {str(e)}")


class YouTubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 버튼 클릭 이벤트 연결
        self.ui.pushButton_download.clicked.connect(self.start_download)

    def sanitize_filename(self, filename):
        return re.sub(r'[\\/*?:"<>|]', "", filename)

    def start_download(self):
        # textEdit_output 초기화
        self.ui.textEdit_output.clear()

        youtube_url = self.ui.lineEdit_url.text()
        ffmpeg_path = self.ui.lineEdit_ffmpeg.text()
        download_path = self.ui.lineEdit_download_path.text()

        # 입력값 검증
        if not youtube_url or not ffmpeg_path or not download_path:
            self.ui.textEdit_output.append("Error: All fields (URL, FFmpeg path, download path) are required.")
            return

        if not os.path.exists(download_path):
            self.ui.textEdit_output.append("Error: The download path does not exist.")
            return

        self.ui.textEdit_output.append("Starting download...")

        # yt-dlp 명령어 생성
        command = [
            "yt-dlp",
            "--ffmpeg-location", ffmpeg_path,
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "-o", os.path.join(download_path, "%(title)s.mp4"),
            youtube_url
        ]

        # 다운로드 스레드 시작
        self.download_thread = DownloadThread(command)
        self.download_thread.log_signal.connect(self.update_output)  # 로그 연결
        self.download_thread.start()

    def update_output(self, message):
        # 로그를 textEdit_output에 추가
        self.ui.textEdit_output.append(message)
        self.ui.textEdit_output.ensureCursorVisible()


if __name__ == "__main__":
    app = QApplication([])
    init_thread = threading.Thread(target=long_initialization)
    init_thread.start()
    window = YouTubeDownloaderApp()
    window.show()
    app.exec_()
