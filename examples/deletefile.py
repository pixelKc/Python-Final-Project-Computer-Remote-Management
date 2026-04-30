import requests

r = requests.get('http://127.0.0.1:8000/deletefile/desktop/test?key=PGOLmdOuRa5yvfeoqy1krXMhf233yIysyGwAnhpGzyY')
data: dict = r.json()
print(data["detail"], end="")