import requests
import os

from utils import path_join

def verify(server_ip, server_port):
    root_url = f"http://{server_ip}:{server_port}"
    resp = requests.get(url=path_join(root_url, "ping"))
    try:
        if resp.json()["message"] != "ping!":
            raise Exception(f"Invalid reply: {resp.json()['reply']}")
    except Exception as e:
        print(f"Error while verifying server: {e}.\nTry restarting the server.")
    return root_url

def send_file(root_url, filepath):
    ''' Send a single file to server '''
    url = path_join(root_url, "upload")
    file = {'file': open(filepath, 'rb')}
    payload = {"parent_dir":os.path.dirname(filepath)}
    response = requests.post(url=url, files=file, data=payload)
    return response

def send_item(root_url, path):
    ''' Recursively send a file or folder to server. '''
    responses = []
    if os.path.isfile(path):
        responses.append(send_file(root_url, path))
    else:
        contents = os.listdir(path)
        for item in contents:
            if os.path.isfile(path_join(path, item)):
                responses.append(send_file(root_url, path_join(path, item)))
            else:
                responses += send_item(root_url, path_join(path, item))
    return responses