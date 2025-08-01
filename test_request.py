import requests

res = requests.post("http://127.0.0.1:5000/evaluate")  # no data sent
print(res.status_code)
print(res.json())
