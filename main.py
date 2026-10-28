from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from checker import check_url

app = FastAPI(title="BD Phishing Link Checker")

class UrlIn(BaseModel):
    url: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/check")
def check(data: UrlIn):
    return check_url(data.url)