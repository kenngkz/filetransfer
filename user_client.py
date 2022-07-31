''' Text user interface for client - sending files '''

import requests
import os

from utils import path_join
from client_utils import send_item, verify

def user_setup():
    ''' Prompt user to set the server ip address and port and checks if the server if active '''
    server_ip = input("Server ip address: ")
    server_port = input("Server port: ")
    root_url = verify(server_ip, server_port)
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

def main():
    '''
    Repeatedly ask for input from user to specify a file or folder path to send to client
    '''
    root_url = user_setup()
    while True:
        path = user_select()
        if path:
            responses = send_item(root_url, path)
            for resp in responses:
                print(resp["message"])
        else:
            break

if __name__ == "__main__":
    main()