생성된 파일을 ffmpeg로 따로 Merge하는 명령어

ffmpeg -i downloaded_video_1080p.f137.mp4 -i downloaded_video_1080p.f140.m4a -c:v copy -c:a aac -b:a 192k merged_output.mp4
