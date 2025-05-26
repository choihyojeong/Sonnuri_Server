# main.py
import nest_asyncio
import uvicorn
from fastapi import FastAPI
from api import router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# 라우터 등록
app.include_router(router)

# 정적 파일 mount
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

def run():
    nest_asyncio.apply()
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    run()



#실행방법: 해당 프로젝트 경로에서 cmd에 명령어 python main.py