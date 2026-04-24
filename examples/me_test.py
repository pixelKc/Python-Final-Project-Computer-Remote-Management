import requests

r = requests.get('http://127.0.0.1:8000/me?key=PGOLmdOuRa5yvfeoqy1krXMhf233yIysyGwAnhpGzyY')
print(r.text)