import sys, os, subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    progress_signal = pyqtSignal(str)

    def __init__(self, url, ffmpeg_path, download_path, parent=None):
        super().__init__(parent)
        self.url = url
        self.ffmpeg_path = ffmpeg_path
        self.download_path = download_path

    def run(self):
        try:
            # Check download path
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)

            # Run the yt-dlp command
            command = [
                "yt-dlp",
                "--ffmpeg-location", self.ffmpeg_path,
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
                "-o", os.path.join(self.download_path, "%(title)s.mp4"),
                self.url
            ]
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Continue reading the log while the command is running and passing it as a signal
            for line in iter(process.stdout.readline, ""):
                if line:
                    self.progress_signal.emit(line.strip())

            process.stdout.close()
            process.wait()
            if process.returncode == 0:
                self.progress_signal.emit("Download completed successfully!")
            else:
                self.progress_signal.emit("Error occurred during download.")
        except Exception as e:
            self.progress_signal.emit(f"Error: {str(e)}")


class YouTubeDownloaderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:\\Users\\sandan\\Documents\\github\\codesample\\dev\\web\\youtube_ui.ui", self)

        # Get UI elements
        self.youtube_url_input = self.findChild(QtWidgets.QLineEdit, "youtubeUrlInput")
        self.ffmpeg_path_input = self.findChild(QtWidgets.QLineEdit, "ffmpegPathInput")
        self.download_path_input = self.findChild(QtWidgets.QLineEdit, "DownloadPathInput")
        self.download_button = self.findChild(QtWidgets.QPushButton, "downloadButton")
        self.output_console = self.findChild(QtWidgets.QTextEdit, "outputConsole")

        # Connect the download button click event
        self.download_button.clicked.connect(self.start_download)

    def start_download(self):
        # Get input values
        url = self.youtube_url_input.text()
        ffmpeg_path = self.ffmpeg_path_input.text()
        download_path = self.download_path_input.text()

        if not url or not ffmpeg_path or not download_path:
            self.output_console.append("Error: All fields (URL, FFmpeg path, download path) are required.")
            return

        # Run download thread
        self.download_thread = DownloadThread(url, ffmpeg_path, download_path)
        self.download_thread.progress_signal.connect(self.update_console)
        self.download_thread.start()

    def update_console(self, message):
        # Update the output console
        self.output_console.append(message)
        self.output_console.ensureCursorVisible()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
