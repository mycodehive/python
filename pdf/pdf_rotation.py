from PyPDF2 import PdfReader, PdfWriter

def rotate_specific_pages(input_path, output_path, pages_to_rotate, rotation_angle):
    pdf_reader = PdfReader(input_path)
    pdf_writer = PdfWriter()
    
    # 모든 페이지 처리
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        if page_num in pages_to_rotate:  # 특정 페이지 번호일 경우만 회전
            page.rotate(rotation_angle)
        pdf_writer.add_page(page)
    
    # 새 PDF 파일로 저장
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

# 사용 예시
if __name__ == "__main__":
    input_pdf = r"C:\\Users\\sandan\\Downloads\\출장교통비.pdf"
    output_pdf = r"C:\\Users\\sandan\\Downloads\\출장교통비2.pdf"
    pages = [0]  # 1번째와 3번째 페이지(0부터 시작)만 회전
    angle = 180
    
    rotate_specific_pages(input_pdf, output_pdf, pages, angle)
    print(f"지정된 페이지가 {angle}도 회전되어 {output_pdf}로 저장되었습니다.")