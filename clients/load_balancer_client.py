import requests

base_url = "http://demo-fast-api-lb-1119634285.us-west-2.elb.amazonaws.com"

response = requests.get(f"{base_url}/")
print(response.json())

response = requests.get(f"{base_url}/hi")
print(response.json())

data = {"name": "ABC"}
response = requests.post(f"{base_url}/name", json=data)
print(response.json())

response = requests.get(f"{base_url}/hello")
print(response.json())
