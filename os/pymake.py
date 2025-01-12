"""
Description :  pyinstaller GUI application using PySide6
Location : https://github.com/sahuni/python
Date : 2025.01.10
"""
import sys
import os
import subprocess
from datetime import datetime
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QTextEdit, QLineEdit, QSizePolicy
from PySide6.QtCore import QThread, Signal, Qt

class BuildThread(QThread):
    progress = Signal(str)

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        try:
            process = subprocess.Popen(self.command, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                self.progress.emit(line)
            process.stdout.close()
            process.wait()
        except Exception as e:
            self.progress.emit(f"Error during build: {e}")

class ExeBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyInstaller EXE Builder")
        self.setMinimumSize(500, 500)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.file_label = QLabel("Select a Python file to build into EXE")
        self.select_button = QPushButton("Select Python File")
        self.exe_name_label = QLabel("Enter EXE filename (without extension):")
        self.exe_name_input = QLineEdit()
        self.options_label = QLabel("Enter additional PyInstaller options (excluding -w, -F):")
        self.options_input = QLineEdit()
        self.build_button = QPushButton("Build EXE")
        self.build_button.setEnabled(False)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.exe_name_label)
        self.layout.addWidget(self.exe_name_input)
        self.layout.addWidget(self.options_label)
        self.layout.addWidget(self.options_input)
        self.layout.addWidget(self.build_button)
        self.layout.addWidget(self.log_output)
        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.select_file)
        self.build_button.clicked.connect(self.build_exe)

        self.selected_file = ""
        self.build_thread = None

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Python File", "", "Python Files (*.py)")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Selected File: {file_path}")
            self.build_button.setEnabled(True)

    def validate_options(self, options):
        forbidden_options = ["-w", "--windowed", "-F", "--onefile"]
        return [opt for opt in options if opt not in forbidden_options]

    def build_exe(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Warning", "Please select a Python file first.")
            return
        
        exe_name = self.exe_name_input.text().strip()
        if not exe_name:
            QMessageBox.warning(self, "Warning", "Please enter a name for the EXE file.")
            return
        
        user_options = self.options_input.text().strip().split()
        additional_options = self.validate_options(user_options)
        
        target_dir = os.path.dirname(self.selected_file)
        command = [
            "pyinstaller",
            "-w",
            "-F",
            "--name", exe_name
        ] + additional_options + [self.selected_file]

        self.log_output.clear()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_output.append(f"[{timestamp}] Starting build process...\n")
        
        self.build_button.setEnabled(False)
        self.build_thread = BuildThread(command, target_dir)
        self.build_thread.progress.connect(self.update_log)
        self.build_thread.finished.connect(self.build_finished)
        self.build_thread.start()

    def update_log(self, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_output.append(f"[{timestamp}] {text}")

    def build_finished(self):
        QMessageBox.information(self, "Finished", "Build process completed.")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_output.append(f"\n[{timestamp}] Build process completed.")
        self.build_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = ExeBuilder()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
