"""
Description : This script generates a random password of the desired length with the option to include letters, digits, and punctuation.
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""

import random
import string

def generate_password(length=12, use_letters=True, use_digits=True, use_punctuation=True):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_punctuation:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character set must be selected")

    password = ''.join(random.choice(characters) for i in range(length))
    return password

if __name__ == "__main__":
    length = int(input("Enter the desired length of the password: "))
    use_letters = input("Include letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_punctuation = input("Include punctuation? (y/n): ").lower() == 'y'

    try:
        print("Generated Password:", generate_password(length, use_letters, use_digits, use_punctuation))
    except ValueError as e:
        print(e)