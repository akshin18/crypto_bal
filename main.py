from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, HTTPException
import shutil

from sqlalchemy.orm import Session
from db import crud, models, schemas
from db.database import SessionLocal, engine

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
async def add_file(data= Form(...)):
    with open("data.csv", "wb") as f:
        shutil.copyfileobj(data.file, f)

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



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
