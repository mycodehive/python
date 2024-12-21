"""
Description : This script validates a URL and checks if the server responds.
Location : https://github.com/sahuni/python
Date : 2024.12.21
"""
import re
import requests
from datetime import datetime
from pytz import timezone

def is_valid_url(url):
    # Regular expression for validating a URL
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, url) is not None

def check_server_response(url):
    try:
        response = requests.get(url)
        server_time = response.headers.get('Date')
        if server_time:
            server_time = datetime.strptime(server_time, '%a, %d %b %Y %H:%M:%S %Z')
            server_time = server_time.astimezone(timezone('Asia/Seoul'))            
        return response.status_code == 200, server_time
    except requests.RequestException:
        return False, None

# Example usage
if __name__ == "__main__":
    test_urls = [
        "http://www.google.com",
        "https://www.naver.com",
        "https://www.facebook.com",
        "ftp://www.example.com",
        "http://localhost",
        "http://127.0.0.1",
        "http://[::1]",
        "invalid_url",
        "http://invalid-url"
    ]

    for url in test_urls:
        is_valid = is_valid_url(url)
        server_responds, server_time = check_server_response(url) if is_valid else (False, None)
        print(f"{url} is valid: {is_valid}, server responds: {server_responds}, server time: {server_time}")