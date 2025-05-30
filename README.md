# 📘 Sonnuri_Server

이 프로젝트는 수어(수화) 학습 웹 애플리케이션의 백엔드 API입니다.  
FastAPI 기반으로 구축되었으며, 수어 단어 조회, 영상 제공, 업로드, 번역 및 정확도 측정 기능을 포함합니다.

---
## 📘 API 명세서

### 1. 학습하기

| 메소드       | 경로                | 설명                 | 파라미터                        | 응답 예시                                         |
| --------- | ----------------- | ------------------ | --------------------------- | --------------------------------------------- |
| GET       | `/learn/{char}`   | 자모 학습 영상 제공        | `char`: 자모 (e.g., ㄱ)        | `{ "video_url": "/static/videos/ㄱ/ㄱ_1.mp4" }` |
| POST      | `/learn/accuracy` | 영상 업로드 → AI 정확도 반환 | `target`: 자모<br>`video`: 파일 | `{ "gesture": "ㄱ", "confidence": 0.932 }`     |
| WebSocket | `/stream/learn`   | 실시간 영상으로 정확도 계산    | 바이너리 프레임 전송                 | `{ "gesture": "ㄱ", "confidence": 0.951 }`     |

---

### 2. 학습 테스트하기

| 메소드  | 경로             | 설명          | 파라미터                                   | 응답 예시                                           |
| ---- | -------------- | ----------- | -------------------------------------- | ----------------------------------------------- |
| GET  | `/test/random` | 랜덤 자모 단어 제공 | 없음                                     | `{ "id": 1, "word": "가다", "video_url": "..." }` |
| POST | `/test/submit` | 테스트 정답 체크   | `word_id`: 단어 ID<br>`selected`: 선택한 단어 | `{ "correct": true, "answer": "가다" }`           |

---

### 3. 번역하기

| 메소드       | 경로                  | 설명                  | 파라미터                     | 응답 예시                                                                        |
| --------- | ------------------- | ------------------- | ------------------------ | ---------------------------------------------------------------------------- |
| GET       | `/translate/reset`  | 번역 초기화              | 없음                       | `{ "message": "초기화 완료" }`                                                    |
| POST      | `/translate/char`   | 자모 하나 저장            | `generated_char`: 인식된 자모 | `{ "current_word": "ㄱ" }`                                                    |
| GET       | `/translate/result` | 누적된 자모 → 번역 결과      | 없음                       | `{ "word": "가", "translated": "[가]에 대한 번역 예시" }`                             |
| WebSocket | `/stream/translate` | 실시간 영상 → 자모 누적 및 번역 | 바이너리 프레임 전송              | `{ "char": "ㄱ", "confidence": 0.93, "accepted": true, "current_word": "가" }` |


---

## 🛠️ 로컬 개발 환경

### 1. 필수 패키지 설치

pip install fastapi uvicorn

### 2. 서버 실행

python main.py

### 3. 접속 확인

브라우저에서 http://localhost:8000 로 이동하여 API 문서 확인

---

## ⚠️ 주의사항

- pyngrok 설치 및 사용은 필요하지 않습니다.
- 본 API는 로컬 테스트 전용으로 설계되어 있습니다.
- /accuracy 기능은 추후 AI 모델 연동이 필요합니다.

---

## 개발자 정보
- 이름: 최효정
- 이메일: chj030405@yu.ac.kr
- GitHub: [github.com/hyoje](https://github.com/choihyojeong)
