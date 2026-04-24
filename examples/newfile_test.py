import requests

file_data = "Test File Data :)"
r = requests.get(f'http://127.0.0.1:8000/newfile/desktop/test?key=PGOLmdOuRa5yvfeoqy1krXMhf233yIysyGwAnhpGzyY&data={file_data}')
data: dict = r.json()
print(data["detail"])