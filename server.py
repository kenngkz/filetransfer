''' API for server - recieving files '''

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import os
from pydantic import BaseModel

from utils import path_join
from constants import SERVER_HOST, SERVER_PORT, SAVE_FOLDER

app = FastAPI()

# create save_folder if does not exists and change current working directory to save_folder
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
os.chdir(SAVE_FOLDER)

@app.get("/")
def root():
    ''' Returns a welcome message '''
    return {"message": "Welcome to File Transfer Server. To upload files to the server, send a request to {SERVER_IP}:{SERVER_PORT}/upload/ and attach a single file and data specifying the parent_dir in which to save the file"}

@app.get("/ping")
def ping():
    ''' Returns a ping '''
    return {"reply": "ping!"}

@app.post("/upload/")
async def upload_file(file:UploadFile = File(...), parent_dir:str = Form(...)):
    ''' Receive files from client and save locally in the server '''
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    # load file contents and write to file with the same name
    try:
        contents = await file.read()
        with open(path_join(parent_dir, file.filename), "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": f"There was an error while uploading the file. Filename: {file.filename}",
                "error": str(e)}
    finally:
        await file.close()

    return {"message": f"File {file.filename} uploaded successfully to {path_join(parent_dir, file.filename)}"}

def main():
    # private ip address
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:    
        s.connect(("8.8.8.8", 80))
        print(f"[+] Server running on private ip address {s.getsockname()[0]} and port {SERVER_PORT} - discoverable only by any device on the same network")
        s.close()
    except Exception as e:
        print(f"Error occured while attempting to retrieve private ip_address: {e}\nServer may not be accessible from other machines.")
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)

if __name__ == "__main__":
    main()