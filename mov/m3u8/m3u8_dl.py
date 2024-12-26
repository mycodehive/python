"""
Description: Download m3u8 streaming video and save it as a local file while displaying progress and status
Location: https://github.com/sahuni/python
Date: 2024.12.25
"""

import subprocess
import re

def download_m3u8_stream(m3u8_url, ffmpeg_path, output_file):
    """
    Download m3u8 streaming video and save it as a local file while displaying progress and status
    :param m3u8_url: m3u8 file URL
    :param ffmpeg_path: Path to FFmpeg executable (e.g., "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe")
    :param output_file: Name of the local file to save (e.g., "output.mp4")
    """
    # Create FFmpeg command
    command = [
        ffmpeg_path,             # User-specified FFmpeg path
        "-i", m3u8_url,           # Input file (m3u8 URL)
        "-c", "copy",             # Copy original stream (no transcoding)
        "-bsf:a", "aac_adtstoasc",  # Audio format conversion (if needed)
        output_file               # Output file
    ]

    duration_pattern = re.compile(r"Duration: (\d+):(\d+):(\d+\.\d+)")  # Extract total duration
    time_pattern = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")           # Extract current time

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr into stdout
            text=True,
            bufsize=1                 # Read output in real-time
        )

        total_duration = None

        # Read and display real-time output
        for line in iter(process.stdout.readline, ""):
            if line:  # Skip empty lines
                print(line.strip())  # Print FFmpeg log

                # Extract total duration
                if not total_duration:
                    match = duration_pattern.search(line)
                    if match:
                        hours, minutes, seconds = map(float, match.groups())
                        total_duration = hours * 3600 + minutes * 60 + seconds
                        print(f"Total duration: {total_duration:.2f} seconds")

                # Extract current time
                match = time_pattern.search(line)
                if match and total_duration:
                    hours, minutes, seconds = map(float, match.groups())
                    current_time = hours * 3600 + minutes * 60 + seconds
                    progress = (current_time / total_duration) * 100
                    print(f"Progress: {progress:.2f}%")

        process.stdout.close()
        process.wait()

        if process.returncode == 0:
            print(f"Download completed successfully. Saved as {output_file}")
        else:
            print("Error occurred during download.")

    except FileNotFoundError:
        print(f"Error: FFmpeg not found at {ffmpeg_path}. Please check the path.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


# Test run
if __name__ == "__main__":
    m3u8_url = "video.m3u8"
    ffmpeg_path = r"C:\\Program Files\\ffmpeg\bin\\ffmpeg.exe"  # User-specified FFmpeg path
    output_file = "output.mp4"  # Name of the file to be downloaded
    download_m3u8_stream(m3u8_url, ffmpeg_path, output_file)
