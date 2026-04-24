import requests

r = requests.get(f'http://127.0.0.1:8000/tts?key=PGOLmdOuRa5yvfeoqy1krXMhf233yIysyGwAnhpGzyY&message=Example Message :)')
data: dict = r.json()
print(data["detail"])