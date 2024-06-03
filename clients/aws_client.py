import requests

base_url = "http://18.237.36.173:80"

response = requests.get(f"{base_url}/")
print(response.json())

response = requests.get(f"{base_url}/hi")
print(response.json())

data = {"name": "ABC"}
response = requests.post(f"{base_url}/name", json=data)
print(response.json())

response = requests.get(f"{base_url}/hello")
print(response.json())
