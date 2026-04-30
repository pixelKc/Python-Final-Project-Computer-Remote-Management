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
from pathlib import Path
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

keys: dict[str, dict[str, str | None | int]]
if os.path.exists("keys.json"):
    with open("keys.json") as f:
        keys = json.loads(f.read())
else:
    keys = {}
    print(f"{Fore.YELLOW}WARNING{Fore.RESET}: keys.json does not exist, using empty object")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        logger.info(f"REQUEST: {request.url.path} | Client: {keys.get(request.query_params.get('key', ''), {'User': 'unknown'})['User']}")
        
        try:
            response = await call_next(request)
            
            duration = time.time() - start_time
            logger.info(f"RESPONSE: {request.url.path} | Status: {response.status_code} | Duration: {duration:.3f}s")
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"ERROR: {request.method} {request.url.path} | Status: 500 | Duration: {duration:.3f}s | Error: {str(e)}")
            raise

app = FastAPI(docs_url=None)
app.add_middleware(LoggingMiddleware)
file_lock = threading.Lock()

def check_access(key: str) -> dict:
    if not key or key not in keys:
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = keys[key]
    if data["limit"] is not None and data["requests"] >= data["limit"]:
        raise HTTPException(status_code=429, detail="Limit Reached!")
    
    data["requests"] += 1
    
    with file_lock:
        with open("keys.json", 'w') as f:
            json.dump(keys, f, indent=4)
        
    return data

valid_roots: dict[str, Path] = {"desktop": Path.home() / "Desktop", "downloads": Path.home() / "Downloads"}

@app.get("/")
def root():
    return {"detail": "Welcome to the Root... it's boring here, go find a URL to request"}

@app.get("/newfile/{root}/{name}")
def newfile(root: str = "", name: str = "", key: str = "", data: str = "") -> dict:
    user_data: dict = check_access(key)
    if not root in valid_roots:
        raise HTTPException(status_code=400, detail=f"Error: {root} is not valid root")
    file_path: Path = valid_roots[root] / f"{key} {name}.txt"
    with open(file_path, 'w') as f:
        f.write(data)
    return {"detail": f"Wrote {data} to {name}.txt"}

@app.get("/readfile/{root}/{name}")
def readfile(root: str = "", name: str = "", key: str = "") -> dict:
    user_data: dict = check_access(key)
    if not root in valid_roots:
        raise HTTPException(status_code=400, detail=f"Error: {root} is not valid root")
    file_path: Path = valid_roots[root] / f"{key} {name}.txt"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Error: {name}.txt was not found")
    with open(file_path) as f:
        data: list = []
        for line in f:
            data.append(line)
    return {"detail": ''.join(data)}

@app.get("/deletefile/{root}/{name}")
def deletefile(root: str = "", name: str = "", key: str = ""):
    user_data: dict = check_access(key)
    if not root in valid_roots:
        raise HTTPException(status_code=400, detail=f"Error: {root} is not valid root")
    file_path: Path = valid_roots[root] / f"{key} {name}.txt"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Error: {name}.txt was not found")
    os.remove(file_path)
    return {"detail": "File removed successfully"}

@app.get("/listfiles/{root}")
def listfiles(root: str = "", key: str = ""):
    user_data: dict = check_access(key)
    if not root in valid_roots:
        raise HTTPException(status_code=400, detail=f"Error: {root} is not valid root")
    folder_path: Path = valid_roots[root]
    files: list[str] = os.listdir(folder_path)
    returnlist = []
    for filename in files:
        if filename.startswith(f"{key} "):
            returnlist.append(filename.replace(f"{key} ", ""))
    return {"detail": returnlist}

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
    return {"detail": "Logout Successful"}

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
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="critical",
        access_log=False
    )