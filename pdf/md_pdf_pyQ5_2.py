"""
Description : This program converts Markdown content to PDF.
Location : https://github.com/sahuni/python
Date : 2024.12.28
"""

import sys, os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog, QStatusBar, QMessageBox
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class MarkdownToPDFConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown to PDF 변환기")
        self.resize(600, 400)

        # 메인 위젯 및 레이아웃 설정
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        # 텍스트 입력 영역
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("여기에 Markdown 내용을 붙여넣으세요.")
        self.layout.addWidget(self.text_edit)

        # 저장 위치 선택 버튼
        self.save_button = QPushButton("저장 위치 선택 및 변환")
        self.save_button.clicked.connect(self.convert_and_save)
        self.layout.addWidget(self.save_button)

        # 상태 표시줄
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 한글 폰트 등록
        self.register_korean_font()

    def register_korean_font(self):
        # 한글 폰트 파일 경로 (시스템에 설치된 폰트 경로로 변경 필요)
        font_path = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
        pdfmetrics.registerFont(TTFont('NanumGothic', font_path))

    def convert_and_save(self):
        # 사용자가 입력한 Markdown 내용 가져오기
        markdown_content = self.text_edit.toPlainText()
        if not markdown_content:
            QMessageBox.warning(self, "경고", "Markdown 내용을 입력하세요.")
            return

        # 저장 위치 선택
        save_dir = QFileDialog.getExistingDirectory(self, "저장 위치 선택")
        if not save_dir:
            return

        # 파일명 생성 (오늘 날짜 YYYYMMDD)
        today = QDate.currentDate().toString("yyyyMMdd")
        pdf_file_path = f"{save_dir}/{today}.pdf"

        # Markdown을 HTML로 변환
        html_content = markdown.markdown(markdown_content)

        # PDF 생성
        try:
            self.create_pdf(html_content, pdf_file_path)
            self.status_bar.showMessage(f"파일이 저장되었습니다: {pdf_file_path}")
            self.status_bar.setStyleSheet("color: blue;")
            self.status_bar.mousePressEvent = lambda event: QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_file_path))
        except Exception as e:
            QMessageBox.critical(self, "오류", f"PDF 변환 중 오류가 발생했습니다: {str(e)}")

    def create_pdf(self, html_content, pdf_file_path):
        # PDF 문서 설정 (A4 크기, 여백 25mm)
        doc = SimpleDocTemplate(
            pdf_file_path,
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm
        )

        # 스타일 시트
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='KoreanStyle',
            fontName='NanumGothic',
            fontSize=12,
            leading=18,  # 줄간격 조정 (기본값 12보다 크게 설정)
            parent=styles['Normal']
            ))

        # HTML 내용을 Paragraph로 변환
        story = []
        for line in html_content.splitlines():
            if line.strip():  # 빈 줄은 무시
                story.append(Paragraph(line, styles["KoreanStyle"]))
                story.append(Spacer(1, 12))  # 줄 간격

        # PDF 생성
        doc.build(story)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarkdownToPDFConverter()
    window.show()
    sys.exit(app.exec_())