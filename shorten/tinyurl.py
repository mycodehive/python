import requests

def shorten_url(long_url):
    api_url = "http://tinyurl.com/api-create.php"
    params = {'url': long_url}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

if __name__ == "__main__":
    long_url = input("Enter the URL to shorten: ")
    short_url = shorten_url(long_url)
    
    if short_url:
        print("Shortened URL:", short_url)
    else:
        print("Error: Unable to shorten the URL.")