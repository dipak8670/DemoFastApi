import requests

base_url = "http://ecsclu-stude-ppqkcetcwuvg-1908943909.us-west-2.elb.amazonaws.com/"

response = requests.get(f"{base_url}")
print(response.json())


data = {"name": "ABC", "roleNumber": "2"}
response = requests.post(f"{base_url}add_student", json=data)
print(response.json())

response = requests.get(f"{base_url}health")
print(response.json())
