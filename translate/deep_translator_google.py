"""
Description : A Python program to translate text in a file from one language to another using Google Translator.
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""

# pip install deep-translator

from deep_translator import GoogleTranslator

def translate_file(input_file, output_file, source_lang, target_lang):
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Performing translation
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated_text = translator.translate(text)
        
        # Save translation results
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_text)
        
        print(f"Translation completed. Translated file saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

input_file = 'C:\\Users\\aaa\\Downloads\\source.txt'          # Original file to be translated
output_file = 'C:\\Users\\aaa\\Downloads\\source_trans.txt'   # Translated result file
source_lang = 'ko'            # Original language (e.g. Korean)
target_lang = 'en'            # Translation language (e.g. English)

translate_file(input_file, output_file, source_lang, target_lang)
