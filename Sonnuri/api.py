# api.py
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json
from fastapi import FastAPI, APIRouter, UploadFile, File, WebSocket, Request
from fastapi.responses import JSONResponse
from typing import Dict, List

router = APIRouter()

UPLOADS_DIR = "uploads"
STATIC_DIR = "static"
SIGN_DICT_PATH = os.path.join(STATIC_DIR, "data", "sign_dictionary.json")

def load_sign_dictionary():
    try:
        with open(SIGN_DICT_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

sign_dictionary = load_sign_dictionary()

@router.get("/")
def read_root():
    return {"message": "Welcome"}

@router.get("/learn/{lang}/{text}")
async def get_sign_video(lang: str, text: str):
    video_path = os.path.join(STATIC_DIR, "videos", lang, f"{text}.mp4")
    if not os.path.exists(video_path):
        return JSONResponse(status_code=404, content={"detail": "영상 파일을 찾을 수 없습니다."})
    return {"video_url": f"/static/videos/{lang}/{text}.mp4"}

@router.post("/upload")
async def upload_sign_video(file: UploadFile = File(...)):
    save_path = os.path.join(UPLOADS_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "업로드 완료", "file_url": f"/uploads/{file.filename}"}

@router.post("/accuracy")
async def check_accuracy(target: str, video: UploadFile = File(...)):
    save_path = os.path.join(UPLOADS_DIR, video.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    similarity_score = 0.0  # TODO: 유사도 계산
    return {"target": target, "accuracy": similarity_score}

@router.post("/translate")
async def translate_sign(input_type: str, payload: UploadFile = File(...)):
    save_path = os.path.join(UPLOADS_DIR, payload.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(payload.file, buffer)
    if input_type == "text":
        return {"video_url": "/static/videos/translated/sample.mp4"}
    return {"text": "번역된 문장 예시"}

@router.get("/words")
def list_sign_words() -> Dict[str, List[Dict[str, str]]]:
    return {"words": [{"id": w["id"], "word": w["word"]} for w in sign_dictionary]}

@router.get("/words/{word_id}")
def get_sign_word_detail(word_id: int) -> Dict:
    word = next((w for w in sign_dictionary if w["id"] == word_id), None)
    if not word:
        return JSONResponse(status_code=404, content={"detail": "단어를 찾을 수 없습니다."})
    return {
        "id": word["id"],
        "word": word["word"],
        "video_url": word["video_url"],
        "description": word["description"]
    }
    
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os
import asyncio
import cv2
import numpy as np
receive_clients = set()
send_clients = set()

def draw_heart(img, center, size=50, color=(0, 0, 255), thickness=-1):
    x, y = center
    radius = size // 3
    cv2.circle(img, (x - radius, y - radius), radius, color, thickness)
    cv2.circle(img, (x + radius, y - radius), radius, color, thickness)
    pts = np.array([
        [x - size, y - radius],
        [x + size, y - radius],
        [x, y + size]
    ])
    cv2.fillPoly(img, [pts], color)

def process_frame(frame_bytes: bytes) -> bytes:
    
    # 받은 프레임을 처리하는 로직 -> AI 구현

    return frame_bytes  # 가공 없이 그대로 반환

@router.websocket("/stream/receive")
async def websocket_receive(websocket: WebSocket):
    await websocket.accept()
    receive_clients.add(websocket)
    try:
        while True:
            frame = await websocket.receive_bytes()
            processed_frame = process_frame(frame)  # 처리된 프레임

            # 모든 send 클라이언트에 처리된 프레임 전송
            disconnected = []
            for client in send_clients:
                try:
                    await client.send_bytes(processed_frame)
                except Exception:
                    disconnected.append(client)
            for dc in disconnected:
                send_clients.remove(dc)
    except WebSocketDisconnect:
        receive_clients.remove(websocket)

@router.websocket("/stream/send")
async def websocket_send(websocket: WebSocket):
    await websocket.accept()
    send_clients.add(websocket)
    try:
        while True:
            # 송신 클라이언트가 연결 유지용으로 텍스트 메시지 보내주거나
            # 그냥 연결 유지만 할 수도 있음
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        send_clients.remove(websocket)
        
@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket 연결됨")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"받은 메시지: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("WebSocket 연결 끊김")

