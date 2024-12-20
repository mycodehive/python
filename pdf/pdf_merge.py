"""
Description : A Python program to merge multiple PDF files into a single PDF file.
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""

import PyPDF2  # Import the PyPDF2 library for PDF manipulation
import os  # Import the os library for file and directory operations

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()  # Create a PdfMerger object
    
    for pdf in pdf_list:  # Iterate through the list of PDF files
        pdf_merger.append(pdf)  # Append each PDF to the merger
    
    with open(output_path, 'wb') as output_file:  # Open the output file in write-binary mode
        pdf_merger.write(output_file)  # Write the merged PDF to the output file

if __name__ == "__main__":
    download_folder = 'C:\\Users\\aaa\\Downloads'  # Directory containing the PDF files
    
    # List all PDF files in the download folder
    pdf_files = [os.path.join(download_folder, f) for f in os.listdir(download_folder) if f.endswith('.pdf')]
    
    output_pdf = 'merged.pdf'  # Output path for the merged PDF
    
    merge_pdfs(pdf_files, output_pdf)  # Merge the PDFs
    
    print(f'Merged PDF saved as {output_pdf}')  # Print a message indicating the output file path
