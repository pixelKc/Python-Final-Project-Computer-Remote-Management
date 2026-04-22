# Remote Computer Access (Python Final Project)

## Endpoints
### /me
Displays info about the API key owner
#### Usage
localhost/me:8000/me?key={apikey}
### /newfile
Creates a new file (Limited to .txt extension, only Desktop and Downloads folders are allowed for security)
#### Usage
localhost/newfile/{root (desktop or downloads)}/{filename}:8000?key={apikey}&data={file data}
### /readfile
Reads the data of a file (Limited to .txt extension, only Desktop and Downloads folders are allowed for security)
#### Usage
localhost/readfile/{root (desktop or downloads)}/{filename}:8000?key={apikey}