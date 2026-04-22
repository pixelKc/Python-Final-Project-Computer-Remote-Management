import requests

r = requests.get('http://127.0.0.1:8000/readfile/desktop/test?key=pFsF59ywkbwjwXZxanxOMWHT7NRO5rI5TefnivXbzNs')
data: dict = r.json()
print(data["detail"], end="")