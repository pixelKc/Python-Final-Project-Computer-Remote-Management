import requests

r = requests.get(f'http://127.0.0.1:8000/lock?key=PGOLmdOuRa5yvfeoqy1krXMhf233yIysyGwAnhpGzyY')
data: dict = r.json()
print(data["detail"])