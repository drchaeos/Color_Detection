import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import pandas as pd
from pydantic import BaseModel

# FastAPI
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# 업로드 이미지 저장 디렉토리 설정
UPLOAD_DIRECTORY = "./static/uploaded_images"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# colors.csv 로드
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"])) + abs(B- int(csv.loc[i,"B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
@app.post("/upload/", response_class=HTMLResponse)
async def upload_image(request: Request, file: UploadFile = File(None)):
    filename = None
    color_name = None
    classification = None
    r = g = b = 0
    if request.method == "POST" and file:
        filename = file.filename
        file_location = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(file_location, "wb+") as buffer:
            buffer.write(file.file.read())


    return templates.TemplateResponse("upload.html", {
        "request": request, 
        "filename": filename, 
        "color_name": color_name, 
        "classification": classification, 
        "r": r, "g": g, "b": b
    })

class Color(BaseModel):
    r: int
    g: int
    b: int

@app.post("/get_color_name")
async def get_color_name(color: Color):
    color_name = getColorName(color.r, color.g, color.b)
    if color_name:
        return {"color_name": color_name}
    raise HTTPException(status_code=404, detail="Color not found")


def upload_image(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_location, "wb+") as buffer:
            buffer.write(file.file.read())
        return RedirectResponse(url=f"/detect_color/{file.filename}", status_code=302)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
