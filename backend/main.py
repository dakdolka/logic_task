from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# from data.orm import Orm
import xlrd


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await Orm.create_all()
#     yield 
    
    
app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешает все домены, можно указать список доменов, например: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешены все методы HTTP
    allow_headers=["*"],  # Разрешены все заголовки
)

def read_excel(file):
    cont = file.read()
    file = BytesIO(cont)
    df = pd.read_excel(file)
    return df
    
@app.get("/test")
async def root():
    return {"message": "Hello World"}


# @app.post("/upload")
# async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
#     # try:
#     order = read_excel(file1.file)
#     info = read_excel(file2.file)
#     # await Orm.upd_info()
#     # await Orm.insert_or_upd_info(info)   
#     # await Orm.insert_order(order)
#     # return {"data1": data1, "data2": data2}
#     # except Exception as e:
#     #     return JSONResponse(status_code=400, content={"message": str(e)})
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

