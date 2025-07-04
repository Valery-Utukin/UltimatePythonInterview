import requests

url = "https://google.com"

response = requests.get(url)
print(f"Status code: {response.status_code}")
