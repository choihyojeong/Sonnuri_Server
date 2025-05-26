# api.py
from fastapi.staticfiles import StaticFiles
import os
import shutil
import json
from fastapi import FastAPI, APIRouter, UploadFile, File, WebSocket, Request
from fastapi.responses import JSONResponse
from typing import Dict, List
from typing import Any
import atexit

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
async def upload_and_evaluate_sign_video(
    file: UploadFile = File(...),
    target: str = File(...)
):
    save_path = os.path.join(UPLOADS_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # TODO: 여기에 실제 AI 모델 평가 로직 추가
    # 예시: 정답 영상과 비교한 후 정확도/정오 판단
    # 지금은 임시로 파일명 기준으로 판단
    is_correct = target in file.filename.lower()
    result = "정답" if is_correct else "오답"

    return {
        "message": "업로드 완료",
        "file_url": f"/uploads/{file.filename}",
        "result": result
    }


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
def list_sign_words() -> Dict[str, List[Dict[str, Any]]]:
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


def cleanup_uploads():
    for f in os.listdir(UPLOADS_DIR):
        file_path = os.path.join(UPLOADS_DIR, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("uploads 폴더 정리 완료")

atexit.register(cleanup_uploads)
