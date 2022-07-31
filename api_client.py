''' API for client - sending files '''

'''
PLANNING

required endpoints
 - home page at root: describes the endpoints
 - specify path to file/folder to be sent to server

in main() before launching app, pass IP and port as arguments, default being SERVER_HOST and SERVER_PORT
'''

from fastapi import FastAPI, Form
import os
import argparse
import uvicorn

from client_utils import verify, send_item
from constants import SERVER_HOST, SERVER_PORT, CLIENT_PORT, CLIENT_HOST

app = FastAPI()

@app.get("/")
def home():
    return {
        "message":"Welcome! You are the file sender (client). Please pick a file/folder and use the endpoint to send files to the file reciever (server)",
        "endpoint": {"relative_url": "/send", "required_data":{"path":"str"}}
    }

@app.get("/send")
def send(path:str = Form(...)):
    if not os.path.exists(path):
        return {"message": "There was an error while selecting file to send", "error": f"Path {path} does not exist"}
    send_item(root_url, path)
    
def get_shell_args():
    '''
    Get the command line arguments
    :return:(ArgumentParser) The command line arguments as an ArgumentParser
    '''
    parser = argparse.ArgumentParser(description='File sender')
    parser.add_argument('--ip', help='Server private ip address', type=str, default=SERVER_HOST)
    parser.add_argument('--port', help='Server port', type=int, default=SERVER_PORT)
    args = parser.parse_args()

    return args

def main():
    args = get_shell_args()
    global root_url  # server root url
    root_url = verify(args.ip, args.port)
    uvicorn.run(app, host=CLIENT_HOST, port=CLIENT_PORT)

if __name__ == "__main__":
    main()