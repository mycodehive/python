"""
Description : Code that selects and runs functions to enable cutting/merging videos, adjusting image quality, inserting subtitles, etc. using ffmpeg.
Location : https://github.com/sahuni/python
Date : 2024.12.20
"""
import os
import subprocess

def cut_video(input_file, start_time, duration, output_file):
    ffmpeg_path = os.environ.get("FFMPEG", "ffmpeg")
    command = [
        ffmpeg_path, '-i', input_file, '-ss', start_time, '-t', duration, '-c', 'copy', output_file
    ]
    subprocess.run(command)

def merge_videos(input_files, output_file):
    ffmpeg_path = os.environ.get("FFMPEG", "ffmpeg")
    with open('file_list.txt', 'w') as file:
        for input_file in input_files:
            file.write(f"file '{input_file}'\n")
    command = [
        ffmpeg_path, '-f', 'concat', '-safe', '0', '-i', 'file_list.txt', '-c', 'copy', output_file
    ]
    subprocess.run(command)
    os.remove('file_list.txt')

def adjust_quality(input_file, output_file, bitrate):
    ffmpeg_path = os.environ.get("FFMPEG", "ffmpeg")
    command = [
        ffmpeg_path, '-i', input_file, '-b:v', bitrate, output_file
    ]
    subprocess.run(command)

def add_subtitle(input_file, subtitle_file, output_file):
    ffmpeg_path = os.environ.get("FFMPEG", "ffmpeg")
    command = [
        ffmpeg_path, '-i', input_file, '-vf', f"subtitles={subtitle_file}", output_file
    ]
    subprocess.run(command)

def main():
    ffmpeg_path = r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe" 
    os.environ["FFMPEG"] = ffmpeg_path

    print("Select an option:")
    print("0. exit")
    print("1. Cut video")
    print("2. Merge videos")
    print("3. Adjust video quality")
    print("4. Add subtitles")
    choice = input("Enter choice: ")

    if choice == '0':
        exit()
    elif choice == '1':
        input_file = input("Enter input file: ")
        start_time = input("Enter start time (HH:MM:SS): ")
        duration = input("Enter duration (HH:MM:SS): ")
        output_file = input("Enter output file: ")
        cut_video(input_file, start_time, duration, output_file)
    elif choice == '2':
        input_files = input("Enter input files separated by space: ").split()
        output_file = input("Enter output file: ")
        merge_videos(input_files, output_file)
    elif choice == '3':
        input_file = input("Enter input file: ")
        output_file = input("Enter output file: ")
        bitrate = input("Enter bitrate (e.g., 1000k): ")
        adjust_quality(input_file, output_file, bitrate)
    elif choice == '4':
        input_file = input("Enter input file: ")
        subtitle_file = input("Enter subtitle file: ")
        output_file = input("Enter output file: ")
        add_subtitle(input_file, subtitle_file, output_file)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()