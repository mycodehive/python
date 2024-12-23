"""
Description : This program generates a QR code for a given text.
Location : https://github.com/sahuni/python
Date : 2024.12.23
"""
import qrcode, os

def generate_qr_code(text, file_path):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    
    # Add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)
    
    # Create an image from the QR code instance
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image to the specified file path
    img.save(file_path)

if __name__ == "__main__":
    print("Hello, this is a QR code!")
    text = input("Enter the value to be converted to qr code : ")
    file_path = input("Enter the path where you want to save the QR code image : ")
    file_path = os.path.join(file_path, "qr_code.png")
    generate_qr_code(text, file_path)
    print(f"QR code generated and saved to {file_path}")