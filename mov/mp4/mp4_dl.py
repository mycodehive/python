import requests

def download_mp4_file(url, output_filename):
    try:
        print("Downloading the MP4 file...")
        # HTTP GET 요청
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 요청에 문제가 있을 경우 예외 발생

        # 파일 쓰기
        with open(output_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # 8KB씩 다운로드
                if chunk:
                    file.write(chunk)
        print(f"File downloaded successfully as {output_filename}")
    except Exception as e:
        print("An error occurred:", e)

# URL 및 출력 파일명 설정
mp4_url = "aaaa.mp4"
output_filename = "aaa.mp4"

# 파일 다운로드 함수 호출
download_mp4_file(mp4_url, output_filename)
