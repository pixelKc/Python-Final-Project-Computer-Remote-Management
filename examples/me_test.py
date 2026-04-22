import requests

r = requests.get('http://127.0.0.1:8000/me?key=pFsF59ywkbwjwXZxanxOMWHT7NRO5rI5TefnivXbzNs')
print(r.text)