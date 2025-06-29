from contextlib import asynccontextmanager
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
from io import BytesIO
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from data.orm import Orm
import xlrd
from pydantic import BaseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Orm.create_all()
    yield 
    
    
app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все домены, можно указать список доменов, например: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешены все методы HTTP
    allow_headers=["*"],  # Разрешены все заголовки
)

class LoginData(BaseModel):
    username: str
    password: str

def read_excel(file):
    cont = file.read()
    file = BytesIO(cont)
    df = pd.read_excel(file)
    return df
    
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    print('catched')
    # try:
    order = read_excel(file1.file)
    info = read_excel(file2.file)
    await Orm.insert_or_upd_info(info)
    order_id = await Orm.get_order_num()   
    await Orm.insert_order(order)
    return JSONResponse(status_code=200, content=await Orm.calc_time_and_volume(order_id + 1))
    
@app.get("/get_res")
async def get_res():
    order_id = await Orm.get_order_num()
    file_path = await Orm.calc_time_and_volume(order_id, flag=True)
    return StreamingResponse(
        open(file_path, "rb"),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"result{order_id}.xlsx",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@app.post("/login")
async def login(data: LoginData):
    res = await Orm.check_if_admin(data.username, data.password)
    if res:
        return JSONResponse(status_code=200, content=res)
    raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


