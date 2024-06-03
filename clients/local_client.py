import requests

base_url = "http://127.0.0.1:80"

response = requests.get(f"{base_url}/")
print(response.json())

response = requests.get(f"{base_url}/hi")
print(response.json())

data = {"name": "ABC", "phone": "9hghgvvjbjhb"}
response = requests.post(f"{base_url}/add", json=data)
print(response.json())

response = requests.get(f"{base_url}/hello")
print(response.json())
