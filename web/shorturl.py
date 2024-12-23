"""
Description : Code to get a short address using the shorturl API
Location : https://github.com/sahuni/python
Date : 2024.12.18
"""
import requests
from bs4 import BeautifulSoup

def shorten_url(long_url):
    try:
        # API 엔드포인트
        api_url = "https://www.shorturl.at/shortener.php"
        
        # 요청 데이터
        data = {
            "u": long_url
        }
        
        # POST 요청
        response = requests.post(api_url, data=data)
        
        # 응답 상태 확인
        if response.status_code == 200:
            # 응답에서 결과 URL 추출
            shortened_url = response.text
            if "https://" in shortened_url:

                # BeautifulSoup으로 HTML 파싱
                soup = BeautifulSoup(shortened_url, "html.parser")

                # id="shortenurl"인 input 태그의 value 속성 추출
                shorten_url_input = soup.find("input", {"id": "shortenurl"})
                if shorten_url_input and "value" in shorten_url_input.attrs:
                    shortened_url = shorten_url_input["value"]
                    print(f"Shortened URL: {shortened_url}")
                else:
                    print("Shortened URL not found.")

                return shortened_url
            else:
                print("Failed to shorten URL. Response:", response.text)
        else:
            print(f"Request failed with status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 사용 예시
long_url = "https://ko.wikipedia.org/wiki/address"
shorten_url(long_url)
