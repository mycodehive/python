"""
Description : This program extracts specified pages from a PDF file.
Location : https://github.com/sahuni/python
Date : 2024.12.23
"""
import PyPDF2
import re, os

def extract_pages_from_pdf(input_pdf_path, output_pdf_path, pages):
    # Parse the pages argument
    page_ranges = pages.split(',')
    page_numbers = set()
    for page_range in page_ranges:
        if '-' in page_range:
            start, end = map(int, page_range.split('-'))
            page_numbers.update(range(start, end + 1))
        else:
            page_numbers.add(int(page_range))

    # Read the input PDF
    with open(input_pdf_path, 'rb') as input_pdf_file:
        reader = PyPDF2.PdfReader(input_pdf_file)
        writer = PyPDF2.PdfWriter()

        # Extract specified pages
        for page_number in sorted(page_numbers):
            if page_number - 1 < len(reader.pages):
                writer.add_page(reader.pages[page_number - 1])

        # Write the output PDF
        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

if __name__ == "__main__":
    input_pdf_path = input("Select a pdf file : ") # Replace with your desired input PDF file path
    input_pdf_dir, input_pdf_filename = os.path.split(input_pdf_path)  

    if input_pdf_filename.endswith('.pdf'):
        output_pdf_filename = input_pdf_filename[:-4] + '_conv.pdf'
    else:
        output_pdf_filename = input_pdf_filename + '_conv.pdf'

    output_pdf_path = os.path.join(input_pdf_dir, output_pdf_filename) #'_conv.pdf'  # Replace with your desired output PDF file path
    print(f"Output PDF path: {output_pdf_path}")
    pages = input("Enter the pages to extract (e.g., 1-3,5): ")  # Replace with your desired pages to extract

    extract_pages_from_pdf(input_pdf_path, output_pdf_path, pages)