# main.py
import nest_asyncio
import uvicorn
from fastapi import FastAPI
from api import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import os

app = FastAPI()

# 라우터 등록
app.include_router(router)

# 정적 파일 mount
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 또는 ["*"] 개발 중에는 * 허용 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run():
    nest_asyncio.apply()
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    run()



#실행방법: 해당 프로젝트 경로에서 cmd에 명령어 python main.py
