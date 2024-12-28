"""
Description : This program converts Markdown content to PDF.
Location : https://github.com/sahuni/python
Date : 2024.12.28
"""

# pyinstaller -w -F --add-data "NanumGothic.ttf;." md2pdf.py

import sys
import os
import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser

# 폰트 경로
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
print(FONT_PATH)

# 한글 폰트 등록
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont('NanumGothic', FONT_PATH))
else:
    raise FileNotFoundError(f"폰트 파일이 {FONT_PATH} 경로에 없습니다. 폰트를 포함하여 배포하세요.")

def md_to_pdf(md_text, output_pdf_path):
    # Convert Markdown to HTML
    html_text = markdown2.markdown(md_text)
    
    # Parse HTML with BeautifulSoup to handle line breaks and structure
    soup = BeautifulSoup(html_text, "html.parser")
    elements = soup.find_all(["p", "h1", "h2", "h3", "ul", "li", "br"])
    
    # Create PDF document with reduced margins
    pdf = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='KoreanNormal', fontName='NanumGothic', fontSize=12, leading=18))
    styles.add(ParagraphStyle(name='KoreanHeading1', fontName='NanumGothic', fontSize=16, leading=22, spaceAfter=12))
    styles.add(ParagraphStyle(name='KoreanHeading2', fontName='NanumGothic', fontSize=14, leading=20, spaceAfter=10))
    
    flowables = []
    
    # Add content with line breaks and proper styling
    for element in elements:
        if element.name in ["h1", "h2", "h3"]:
            style = styles['KoreanHeading1'] if element.name == "h1" else (
                styles['KoreanHeading2'] if element.name == "h2" else styles['KoreanNormal']
            )
            flowables.append(Paragraph(element.text, style))
        elif element.name == "p":
            flowables.append(Paragraph(element.text, styles['KoreanNormal']))
        elif element.name == "li":
            flowables.append(Paragraph(f"• {element.text}", styles['KoreanNormal']))
        elif element.name == "br":
            flowables.append(Spacer(1, 12))  # Add spacing for line breaks
        flowables.append(Spacer(1, 6))  # Add space between paragraphs
    
    # Build the PDF
    pdf.build(flowables)


class PDFConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Markdown to PDF Converter")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        # Text area for input
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("여기에 텍스트를 입력하세요...")
        layout.addWidget(self.text_area)

        # Button to select output location
        self.select_location_button = QPushButton("PDF 저장 위치 선택", self)
        self.select_location_button.clicked.connect(self.select_location)
        layout.addWidget(self.select_location_button)

        # Button to convert text to PDF
        self.convert_button = QPushButton("변환", self)
        self.convert_button.clicked.connect(self.convert_to_pdf)
        layout.addWidget(self.convert_button)

        # Label to display status with clickable functionality
        self.status_label = QLabel(self)
        self.status_label.setText("상태 표시줄")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.status_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.status_label.setStyleSheet("color: blue;")
        self.status_label.mousePressEvent = self.open_pdf  # Add click event
        layout.addWidget(self.status_label)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize output path
        self.output_path = ""

    def select_location(self):
        # Select directory and save file path
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "PDF 저장 위치 선택")
        if directory:
            today_date = datetime.now().strftime("%Y%m%d")
            self.output_path = f"{directory}/오늘의 토플_{today_date}.pdf"
            self.status_label.setText(f"저장 위치 선택됨: {self.output_path}")

    def convert_to_pdf(self):
        if not self.output_path:
            self.status_label.setText("저장 위치를 먼저 선택하세요!")
            return

        md_text = self.text_area.toPlainText()
        if not md_text.strip():
            self.status_label.setText("텍스트를 입력하세요!")
            return

        try:
            md_to_pdf(md_text, self.output_path)
            self.status_label.setText(f"PDF 저장 완료: {self.output_path}")
        except Exception as e:
            self.status_label.setText(f"오류 발생: {str(e)}")

    def open_pdf(self, event):
        if os.path.exists(self.output_path):
            webbrowser.open(self.output_path)
        else:
            self.status_label.setText("PDF 파일이 존재하지 않습니다!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFConverterApp()
    window.show()
    sys.exit(app.exec_())
