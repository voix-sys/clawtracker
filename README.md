# ClawTracker (MVP)

OpenClaw 운영 상태를 실시간에 가깝게 보여주는 로컬 대시보드.

## MVP 기능
- 모델/세션 사용량 패널
- OpenClaw 상태 요약 (`openclaw status`)
- Gateway healthz/readyz 체크
- 최근 로그 스냅샷
- 5초 자동 새로고침
- 가독성 강화 UI(v0.2): KPI 우선 영역 + 상태 레벨(NORMAL/WARNING/CRITICAL)

## 실행
```bash
cd clawtracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8507
```

브라우저: `http://localhost:8507`

## 사용량 경고 알림(시범)
```bash
cd clawtracker
source .venv/bin/activate
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python watch_usage.py
```

## 사용량 모니터 루프(5분 간격)
```bash
cd clawtracker
source .venv/bin/activate
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python monitor_loop.py
```
- 경고 기준: 5h 또는 week 잔량 30% 이하
- 위험 기준: 5h 또는 week 잔량 15% 이하

## 운영 가이드
- 상세 실행/장애 대응: `RUNBOOK.md`

## 보안
- 기본 로컬 전용(127.0.0.1)
- 토큰/비밀키 저장 안 함 (`.env.local`은 git 제외)
- 외부 공개 전 sanitization 권장
