import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
import os

from utils import path_join
from constants import SAVE_FOLDER

app = FastAPI()

# create save_folder if does not exists and change current working directory to save_folder
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
os.chdir(SAVE_FOLDER)

@app.get("/")
def root():
    ''' Returns a welcome message '''
    return {"message": "Welcome to File Transfer Server. To upload files to the server, pray."}

@app.get("/items/")
def read_items():
    ''' Lists items in the save_folder '''
    pass

@app.post("/upload/")
async def upload_file(file:UploadFile = File(...), parent_dir:str=Form(...)):
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

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)