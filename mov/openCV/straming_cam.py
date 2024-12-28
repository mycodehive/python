"""
Description : Code to stream live video from the camera using FastAPI.
Location : https://github.com/sahuni/python
Date : 2024.12.28
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import cv2

app = FastAPI()

# 카메라 객체 초기화 (0은 기본 카메라, 외부 카메라는 인덱스를 변경)
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # 카메라에서 프레임 읽기
        success, frame = camera.read()
        if not success:
            break
        else:
            # 프레임을 JPEG로 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # 각 프레임을 바이트 형태로 반환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/", response_class=HTMLResponse)
async def index():
    # HTML 페이지 반환
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Live Streaming</title>
    </head>
    <body>
        <h1>Live Video Streaming</h1>
        <img src="/video_feed" alt="Live Video Feed">
    </body>
    </html>
    """

@app.get("/video_feed")
async def video_feed():
    # StreamingResponse를 사용하여 영상 스트리밍
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")