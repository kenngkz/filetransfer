from tkinter import EXCEPTION
import requests

from utils import path_join

def user_setup():
    server_ip = input("Please specify the server ip address: ")
    server_port = input("Please specify the server port: ")
    root_url = f"http://{server_ip}:{server_port}"
    resp = requests.get(url=path_join(root_url, "ping"))
    try:
        if resp.json()["reply"] != "ping!":
            raise Exception(f"Invalid reply: {resp.json()['reply']}")
    except Exception as e:
        print(f"Error while verifying server: {e}")

    return server_ip, server_port