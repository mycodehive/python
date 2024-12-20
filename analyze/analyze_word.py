"""
Description : A Python program to analyze word frequency in a specific column of an Excel file, excluding specific words.
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""
import pandas as pd
from collections import Counter
import re

def analyze_word_frequency_with_exclusion(excel_file, sheet_name, column_index, exclude_words):
    try:
        # Read Excel file
        data = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        # Get specified column data
        column_data = data.iloc[:, column_index]
        text = " ".join(map(str, column_data.dropna()))  # Convert to string after removing NaN
        
        # Text cleaning and word extraction
        words = re.findall(r'\b\w+\b', text.lower())  # Extract only words using regular expressions (convert to lowercase)
        
        # Exclude specific words
        filtered_words = [word for word in words if word not in exclude_words]
        
        # Word frequency analysis
        word_counts = Counter(filtered_words)
        
        # Output the top 10 words and their frequency
        top_10_words = word_counts.most_common(10)
        print("Top 10 Words (Excluding specific words):")
        for word, count in top_10_words:
            print(f"{word}: {count}")
        
        return top_10_words
    except Exception as e:
        print("An error occurred:", e)

excel_file = 'C:\\Users\\aaaaa\\Downloads\\analyze_target.xlsx'
sheet_name = 'Sheet1'
column_index = 5
# Read exclude words from a file
with open('exclude.txt', 'r', encoding='utf-8') as file:
    exclude_words = [line.strip() for line in file if line.strip()]

analyze_word_frequency_with_exclusion(excel_file, sheet_name, column_index, exclude_words)
