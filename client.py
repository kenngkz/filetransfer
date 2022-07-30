from tkinter import EXCEPTION
import requests
import os

from utils import path_join

def user_setup():
    ''' Prompt user to set the server ip address and port and checks if the server if active '''
    server_ip = input("Server ip address: ")
    server_port = input("Server port: ")
    root_url = f"http://{server_ip}:{server_port}"
    resp = requests.get(url=path_join(root_url, "ping"))
    try:
        if resp.json()["reply"] != "ping!":
            raise Exception(f"Invalid reply: {resp.json()['reply']}")
    except Exception as e:
        print(f"Error while verifying server: {e}")
    return root_url

def user_select():
    ''' Prompt user to select a file or folder to send to server '''
    while True:
        path = input("Please specify a file/directory (as a path) or type ... to abort: ")
        if path == "...":
            return
        if os.path.exists(path):
            break
        else:
            print(f"Path {path} does not exist. Try again.")
    return path

def send_file(root_url, filepath):
    ''' Send a single file to server '''
    url = path_join(root_url, "upload")
    file = {'file': open(filepath, 'rb')}
    payload = {"parent_dir":os.path.dirname(filepath)}
    response = requests.post(url=url, files=file, data=payload)
    print(response.json())

def send_item(root_url, path):
    ''' Recursively send a file or folder to server. '''
    if os.path.isfile(path):
        send_file(root_url, path)
    else:
        contents = os.listdir(path)
        for item in contents:
            if os.path.isfile(path_join(path, item)):
                send_file(root_url, path_join(path, item))
            else:
                send_item(root_url, path_join(path, item))

def main():
    '''
    Repeatedly ask for input from user to specify a file or folder path to send to client
    '''
    root_url = user_setup()
    while True:
        path = user_select()
        if path:
            send_item(root_url, path)
        else:
            break