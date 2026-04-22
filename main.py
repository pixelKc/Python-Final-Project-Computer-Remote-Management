from fastapi import FastAPI, Response, HTTPException, status
from colorama import init, Fore, Style
import json
import uvicorn
import os

app = FastAPI(docs_url=None)

keys: dict
if os.path.exists("keys.json"):
    with open("keys.json") as f:
        keys = json.loads(f.read())
else:
    keys = {}
    print(f"{Fore.YELLOW}WARNING{Fore.RESET}: keys.json does not exist, using empty object")

def check_access(key: str) -> dict:
    if not key or key not in keys:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = keys[key]
    if data["limit"] is not None and data["requests"] >= data["limit"]:
        raise HTTPException(status_code=429, detail="Limit Reached!")
    
    data["requests"] += 1
    
    with open("keys.json", 'w') as f:
        json.dump(keys, f, indent=4)
        
    return data

valid_roots = {"desktop": "/Users/KCKan/Desktop", "downloads": "/Users/KCKan/Downloads"}

@app.get("/")
def root():
    return {"detail": "Welcome to the Root... it's boring here, go find a URL to request"}

@app.get("/newfile/{root}/{name}")
def newfile(root: str = "", name: str = "", key: str = "", data: str = "") -> dict:
    user_data: dict = check_access(key)
    if not root in valid_roots:
        return {"detail": f"Error: {root} is not valid root"}
    with open(f"{valid_roots[root]}/{name}.txt", 'w') as f:
        f.write(data)
    return {"detail": f"Wrote {data} to {name}.txt"}

@app.get("/readfile/{root}/{name}")
def readfile(root: str = "", name: str = "", key: str = "") -> dict:
    user_data: dict = check_access(key)
    if not root in valid_roots:
        return {"detail": f"Error: {root} is not valid root"}
    if not os.path.exists(f"{valid_roots[root]}/{name}.txt"):
        return {"detail": f"Error: {name}.txt was not found"}
    with open(f"{valid_roots[root]}/{name}.txt") as f:
        data: list = []
        for line in f:
            data.append(line)
    return {"detail": ''.join(data)}

@app.get("/me")
def me(key: str = "") -> dict:
    user_data: dict = check_access(key)
    return {"detail": user_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)