from fastapi import FastAPI, HTTPException
from colorama import Fore
import json
import uvicorn
import os
import tkinter as tk
from tkinter import messagebox
import threading
import platform
import pyttsx3

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

@app.get("/sendpopup")
def sendpopup(key: str = "", message: str = ""):
    def show_async_popup(message, username):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True) 
        messagebox.showinfo(f"Popup from {username}", message)
        root.destroy()
    user_data: dict = check_access(key)
    threading.Thread(target=show_async_popup, args=(message,user_data["User"]), daemon=True).start()
    
    return {"detail": "Popup trigger sent"}

@app.get("/lock")
def lock(key: str = ""):
    user_data: dict = check_access(key)
    system = platform.system()
    if system == "Windows":
        import ctypes
        ctypes.windll.user32.LockWorkStation()
    elif system == "Darwin":
        os.system("pmset displaysleepnow")
    elif system == "Linux":
        os.system("xdg-screensaver lock") 
    return {"detail": "Logout Successfull"}

@app.get("/tts")
def tts(key: str = "", message: str = ""):
    def send_async_popup(message, username):
        engine = pyttsx3.init()
        engine.say(f"Message from {username}: {message}")
        engine.runAndWait()
    user_data: dict = check_access(key)
    threading.Thread(target=send_async_popup, args=(message,user_data["User"]), daemon=True).start()

    return {"detail": "Message Successfully Sent"}

@app.get("/me")
def me(key: str = "") -> dict:
    user_data: dict = check_access(key)
    return {"detail": user_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)