# 📘 Sonnuri_Server

이 프로젝트는 수어(수화) 학습 웹 애플리케이션의 백엔드 API입니다.  
FastAPI 기반으로 구축되었으며, 수어 단어 조회, 영상 제공, 업로드, 번역 및 정확도 측정 기능을 포함합니다.

---

## 🚀 주요 기능

| 엔드포인트               | 메서드 | 설명                                                |
|--------------------------|--------|-----------------------------------------------------|
| `/`                      | GET    | 기본 확인용                                         |
| `/learn/{lang}/{text}`  | GET    | 특정 언어의 수어 영상 제공                          |
| `/upload`               | POST   | 사용자 영상 업로드                                  |
| `/translate`            | POST   | 수어 ↔ 텍스트 변환 (샘플 반환)                      |
| `/accuracy`             | POST   | 업로드된 영상과 목표 단어 비교 정확도 평가 (미구현) |
| `/words`                | GET    | 수어 단어 목록 조회                                 |
| `/words/{word_id}`      | GET    | 단어 상세 정보 조회                                 |

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
