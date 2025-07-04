import requests

url = "https://google.com"

response = requests.get(url)
print(f"Status code: {response.status_code}")

print("\nRequest headers:")
for k, v in response.request.headers.items():
    print(f"{k}: {v}")

print("\nResponse headers:")
for k, v in response.headers.items():
    print(f"{k}: {v}")
