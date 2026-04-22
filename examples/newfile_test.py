import requests

file_data = "colleipokie@gmail.com\ncolleepokie@gmail.com\npixelkc@proton.me"
r = requests.get(f'http://127.0.0.1:8000/newfile/desktop/test?key=pFsF59ywkbwjwXZxanxOMWHT7NRO5rI5TefnivXbzNs&data={file_data}')
data: dict = r.json()
print(data["detail"])