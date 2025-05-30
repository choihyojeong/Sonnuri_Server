# api.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Dict
import os, json, shutil, random, asyncio, cv2, numpy as np

router = APIRouter()

STATIC_DIR = "static"
UPLOADS_DIR = "uploads"
SIGN_DICT_PATH = os.path.join(STATIC_DIR, "data", "sign_dictionary.json")

# Load dictionary
def load_sign_dictionary():
    try:
        with open(SIGN_DICT_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

sign_dictionary = load_sign_dictionary()

# ---------------------- 1. 학습하기 ----------------------

@router.get("/learn/{char}")
def get_learning_video(char: str):
    """자모 학습용 영상 제공"""
    #video_path = os.path.join(STATIC_DIR, "videos", "{char}", f"{char}_1.mp4")
    #if not os.path.exists(video_path):
    #    return JSONResponse(status_code=404, content={"detail": "영상이 존재하지 않습니다."})
    return {"video_url": f"/static/videos/{char}/{char}_1.mp4"}

# 1-1. ---------------- 업로드 형식
@router.post("/learn/accuracy")
async def check_learning_accuracy(target: str, video: UploadFile = File(...)):
    """AI에게 영상 전달하여 정확도 및 자모 반환"""
    save_path = os.path.join(UPLOADS_DIR, video.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # TODO: AI 판단 로직 호출 → 예시 반환
    result = {"gesture": target, "confidence": round(random.uniform(0.85, 0.98), 3)}
    return result

# 1-2. ---------------- 실시간 형식
@router.websocket("/stream/learn")
async def websocket_learn(websocket: WebSocket):
    """학습 모드: 실시간 영상 프레임 받아서 정확도 계산"""
    await websocket.accept()
    try:
        while True:
            frame = await websocket.receive_bytes()
            processed_frame = process_frame(frame)  # AI 분석

            # 임시 정확도 및 제스처 판단 (예시)
            result = {
                "gesture": "ㄱ",  # 실제 모델 결과
                "confidence": round(random.uniform(0.85, 0.98), 3)
            }

            await websocket.send_text(json.dumps(result))
    except WebSocketDisconnect:
        print("웹소켓 연결 종료 (학습)")


# ---------------------- 2. 학습 테스트하기 ----------------------

@router.get("/test/random")
def get_random_test_word():
    """랜덤 자모 반환 (객관식 제공용)"""
    random_word = random.choice(sign_dictionary)
    return {"id": random_word["id"], "word": random_word["word"], "video_url": random_word["video_url"]}

@router.post("/test/submit")
def check_test_answer(word_id: int, selected: str):
    """정답 체크"""
    word = next((w for w in sign_dictionary if w["id"] == word_id), None)
    if not word:
        return JSONResponse(status_code=404, content={"detail": "단어를 찾을 수 없습니다."})
    is_correct = word["word"] == selected
    return {"correct": is_correct, "answer": word["word"]}

# ---------------------- 3. 번역하기 ----------------------

@router.get("/translate/reset")
def reset_translation():
    translated_chars.clear()
    return {"message": "초기화 완료"}

# ---------------- 3-1. 업로드 형식
translated_chars = []

@router.post("/translate/char")
def receive_char(generated_char: str):
    """자모 누적 저장"""
    translated_chars.append(generated_char)
    return {"current_word": "".join(translated_chars)}

@router.get("/translate/result")
def get_translated_result():
    """누적 자모 → 단어 반환 및 외부 API 번역 결과 전달"""
    word = "".join(translated_chars)
    # TODO: 실제 번역 API 사용
    translated = f"[{word}]에 대한 번역 예시"
    return {"word": word, "translated": translated}

# ---------------- 3-2. 실시간 형식
@router.websocket("/stream/translate")
async def websocket_translate(websocket: WebSocket):
    """번역 모드: 실시간 영상으로 자모 누적 처리"""
    await websocket.accept()
    word_builder = []
    CONFIDENCE_THRESHOLD = 0.90  # 일정 정확도 이상일 때만 저장
    SEQ_LENGTH = 10 # 필요한 프레임 개수
    try:
        while True:
            frame = await websocket.receive_bytes()
            processed_frame = process_frame(frame)

            # 인식된 자모 결과 (예시로 랜덤)
            detected_char = random.choice(["ㄱ", "ㄴ", "ㅏ", "ㅓ", "ㅗ"])
            confidence = round(random.uniform(0.0, 1.0), 3)

            if confidence >= CONFIDENCE_THRESHOLD:
                word_builder.append(detected_char)

            await websocket.send_text(json.dumps({
                "char": detected_char,
                "confidence": confidence,
                "accepted": confidence >= CONFIDENCE_THRESHOLD,
                "current_word": "".join(word_builder)
            }))
    except WebSocketDisconnect:
        print("웹소켓 연결 종료 (번역)")


# ---------------------- 4. 웹소켓 (실시간 영상 처리) ----------------------

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
