import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bs4 import BeautifulSoup
from datetime import datetime

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

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
        leftMargin=36,  # 기본 72pt(1 inch)에서 50% 줄인 값
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Add custom styles for Korean text with adjusted line spacing
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

if __name__ == "__main__":
    md_text = """
# 한글 및 줄바꿈 테스트

이 문장은 한글을 포함하고 있습니다.  
줄바꿈 테스트를 진행 중입니다.

## 하위 제목

- 첫 번째 항목
- 두 번째 항목
- 세 번째 항목

---

다음 줄로 넘어가는 예제:  
이것은 다음 줄입니다.

1. What is the main idea of the passage?  
   - (A) The Maya civilization disappeared solely due to environmental factors.  
   - (B) Scholars agree on the exact reasons for the Maya civilization's collapse.  
   - (C) The collapse of the Maya civilization likely resulted from a combination of factors.  
   - (D) The Maya civilization ended because of European colonization.  
"""
    # 날짜 기반 파일명 생성
    today_date = datetime.now().strftime("%Y%m%d")
    output_pdf_path = f"오늘의 토플_{today_date}.pdf"
    
    md_to_pdf(md_text, output_pdf_path)
    print(f"PDF generated at {output_pdf_path}")
