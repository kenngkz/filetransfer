# Description
Transfers files from client to server. Requires both client and server to be on the same network.

## Installing Dependencies
Ensure Python3 is installed. Then run `pip3 install -r requirements.txt` in terminal.

## How To Launch
Change ROLE in constants.py to set whether you want to recieve/send files.
Valid values:
1. "R" : recieve files
2. "S" : API for sending files
3. "US": text user interface for sending files 

After that, run `python main.py` if R or US, or `python main.py --ip <SERVER_PRIVATE_IP> --port <SERVER_PORT>`

---
# Dev
#### TODO
test on windows laptop