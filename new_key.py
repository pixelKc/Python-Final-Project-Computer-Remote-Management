import secrets
import json
import sys
import os

if os.path.exists("keys.json"):
    with open("keys.json") as f:
        keys = json.load(f)
else:
    keys = {}

name: str = input("Enter your name: ")
email: str = input("Enter your email: ")
if any(u['Email'] == email for u in keys.values()):
    print("Email already registered!")
    sys.exit(0)

key = secrets.token_urlsafe(32).replace('_', 'x').replace('-', 'y')
while key in keys:
    key = secrets.token_urlsafe(32).replace('_', 'x').replace('-', 'y')

user = {"User": name, "Email": email, "limit": 100, "requests": 0}

keys[key] = user

with open("keys.json", 'w') as f:
    json.dump(keys, f, indent=4)