"""
Description : Code to download YouTube videos in the highest quality using the internal module subprocess.
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""

import subprocess
import os, re

def get_video_title(url):
  # Get titles using yt-dlp
    try:
        
        result = subprocess.run(
            ["yt-dlp", "--print", "%(title)s", url],
            text=True, capture_output=True
        )
        title = result.stdout.strip()
        return title
    except Exception as e:
        print("Error while fetching video title:", e)
        return None

def sanitize_filename(filename):
    # Replace characters not allowed in file names
    return re.sub(r'[\\/*?:"<>|]', "", filename)
    
def download_youtube_video_with_yt_dlp(url,ffmpeg_path):
    try:
        # Get Title
        output_filename = sanitize_filename(get_video_title(url))
        if not output_filename:
            output_filename = "downloaded_video"  # Default if title fetching fails

        print("Downloading the video using yt-dlp...")
        os.environ["FFMPEG"] = ffmpeg_path  # Set FFmpeg path in environment variables

        subprocess.run([
            "yt-dlp",
            "--ffmpeg-location", ffmpeg_path,
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",  # Highest quality video + audio
            "-o", f"{output_filename}.mp4",                     # Output file name
            url
        ])
        print(f"Video downloaded successfully as {output_filename}.mp4")
    except Exception as e:
        print("An error occurred:", e)

youtube_url = "https://...youtube address..."
ffmpeg_path = r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe" 

download_youtube_video_with_yt_dlp(youtube_url,ffmpeg_path)
