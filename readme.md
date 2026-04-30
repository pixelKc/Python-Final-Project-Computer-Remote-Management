# Remote Computer Access (Python Final Project)

## Endpoints
### /me
Displays info about the API key owner
#### Usage
localhost:8000/me/me?key={apikey}
### /newfile
Creates a new file (Limited to .txt extension, only Desktop and Downloads folders are allowed for security)
#### Usage
localhost:8000/newfile/{root (desktop or downloads)}/{filename}?key={apikey}&data={file data}
### /readfile
Reads the data of a file (Limited to .txt extension, only Desktop and Downloads folders are allowed for security)
#### Usage
### /deletefile
Deletes a file (Limited to .txt extension, only Desktop and Downloads folders are allowed for security)
#### Usage
localhost:8000/deletefile/{root (desktop or downloads)}/{filename}?key={apikey}
### /listfiles
Lists the files in a directory (only Desktop and Downloads folders are allowed for security)
#### Usage
localhost:8000/deletefile/{root (desktop or downloads)}?key={apikey}
### /sendpopup
Sends a popup to the server
#### Usage
localhost:8000/sendpopup?key={apikey}&message={message}
### /lock
Locks the computer
#### Usage
localhost:8000/lock?key={apikey}
### /tts
Plays text to speech audio
#### Usage
localhost:8000/tts?key={apikey}&message={message}