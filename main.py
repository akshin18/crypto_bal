from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/ping")
async def ping():
    return "pong"

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse("index.html",context={"request":request})

@app.get("/get_currecies")
async def get_currecies():
    data = [
            "Etherium",
            "BTC",
            "Polygon",
            "Something",
            "Fantom",
            "Something",
            "Optimism",
          ]
    data_2 = [
        ["usdt","busd"],["usdt1","busd"],["usdt2","busd"]
    ]
    return {"data":[data,data_2]}

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)