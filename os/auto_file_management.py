"""
Description :  This script organizes files in a folder based on user input.
Location : https://github.com/sahuni/python
Date : 2024.12.31
"""
import os
import shutil
from datetime import datetime

def log_to_file(log_file, message):
    """Log message to a file"""
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def sort_by_date(folder_path, log_file):
    """Sort files by date"""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # Check the modification date of the file
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            date_folder = modified_time.strftime('%Y-%m-%d')
            destination_folder = os.path.join(folder_path, date_folder)
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(file_path, destination_folder)
            log_to_file(log_file, f"Moved {file_name} to {destination_folder}")

def sort_by_file_type(folder_path, log_file):
    """Sort files by file type"""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            # Classify files by extension
            file_extension = os.path.splitext(file_name)[1][1:].lower()  # Get the extension
            if not file_extension:  # If there is no extension, move to 'NoExtension' folder
                file_extension = 'NoExtension'
            destination_folder = os.path.join(folder_path, file_extension)
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(file_path, destination_folder)
            log_to_file(log_file, f"Moved {file_name} to {destination_folder}")

def list_files(folder_path):
    """Return a list of files in the folder"""
    files = []
    for root, dirs, file_names in os.walk(folder_path):
        for file_name in file_names:
            files.append(os.path.join(root, file_name))
    return files

def main():
    print("=== Automatic File Management Program ===")
    folder_path = input("Enter the path of the folder to organize: ")
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Exiting the program.")
        return

    log_file = os.path.join(folder_path, 'log.txt')

    # Record the state before sorting
    log_to_file(log_file, "=== File list before sorting ===")
    for file in list_files(folder_path):
        log_to_file(log_file, file)

    print("Select sorting option:")
    print("1. Sort by date")
    print("2. Sort by file type")
    choice = input("Choice (1/2): ")

    if choice == '1':
        sort_by_date(folder_path, log_file)
        print("Files have been sorted by date.")
    elif choice == '2':
        sort_by_file_type(folder_path, log_file)
        print("Files have been sorted by file type.")
    else:
        print("Invalid choice. Exiting the program.")
        return

    # Record the state after sorting
    log_to_file(log_file, "\n=== File list after sorting ===")
    for file in list_files(folder_path):
        log_to_file(log_file, file)

    print(f"Sorting is complete. The log file is saved at {log_file}.")

if __name__ == "__main__":
    main()
