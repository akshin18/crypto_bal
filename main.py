from threading import Thread as th
from datetime import datetime, timedelta
from time import sleep

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI
import shutil


from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine
from func import add_address_to_db

import uvicorn
#0x76691696dE14216AE1810Bd25117B843029E936B

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def add_csv_to_db(csv_name,db):
    add_address_to_db(csv_name,db)

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/login_page")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})
@app.post("/login_page")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.post("/login")
async def login_post(request: Request,username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin":
        headers = {"set-cookie":"auth=sad"}
        return RedirectResponse("/",headers=headers)
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
@app.post("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/get_currecies", response_model=list[schemas.GetCurrency])
async def get_currecies(db: Session = Depends(get_db)):
    currencies = crud.get_currencies(db)
    return currencies

@app.get("/get_wallets", response_model=list[schemas.Statistics])
async def get_wallets(sub,db: Session = Depends(get_db)):
    data = crud.get_wallets(sub, db)
    return data

@app.post("/add_address")
async def add_address(address:schemas.Address,db: Session = Depends(get_db)):
    crud.add_address_db(db,address)
    return {"data":[1,2,3,4]}

@app.post("/add_file")
async def add_file(background_tasks: BackgroundTasks,data= Form(...), db: Session = Depends(get_db)):
    with open("data.csv", "wb") as f:
        shutil.copyfileobj(data.file, f)
    background_tasks.add_task(add_csv_to_db,"data.csv",db)
    return {"status":"ok"}


@app.post("/create_currency")
async def create_currency(currency:schemas.CreateCurrency, db: Session = Depends(get_db)):
    crud.create_currency(db,currency)
    return {"status":"Successfully"}


@app.post("/create_sub_currency")
async def create_sub_currency(sub_currency:schemas.CreateSubCurrency, db: Session = Depends(get_db)):
    crud.create_sub_currency(db,sub_currency)
    return {"status":"Successfully"}


@app.middleware("http")
async def middleware(request: Request, call_next):
    response = await call_next(request)
    auth = request.cookies.get("auth",None)
    if auth != "sad" and not (str(request.url).endswith("/login") or str(request.url).endswith("/login_page")):
        return RedirectResponse("/login_page")
    return response

@app.on_event("startup")
def some_task():
    print("strted")
    targ = datetime.now() + timedelta(days=1)
    crud.check_and_update_balances(get_db())

    while True:
        now = datetime.now()
        if now > targ:
            targ = now + timedelta(days=1)
            crud.check_and_update_balances(get_db())
        sleep(10)
        
if __name__ == "__main__":
    
    uvicorn.run("main:app", reload=True)
