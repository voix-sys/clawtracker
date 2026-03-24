# ClawTracker Runbook

## 1) 로컬 실행
```bash
cd /home/k1/.openclaw/workspace/clawtracker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8507
```
접속: http://localhost:8507

## 2) 알림 봇 테스트
```bash
cd /home/k1/.openclaw/workspace/clawtracker
source .venv/bin/activate
export TELEGRAM_BOT_TOKEN=... 
export TELEGRAM_CHAT_ID=...
python watch_usage.py
```

## 3) 자동 모니터 루프(5분 간격)
```bash
cd /home/k1/.openclaw/workspace/clawtracker
source .venv/bin/activate
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_CHAT_ID=...
python monitor_loop.py
```

## 4) Tailscale로 외부 보기 (선택)
로컬 실행 후 Tailscale이 켜져 있으면, 해당 노드의 tailnet IP로 8507 포트 접근.
보안상 공개 인터넷 노출 금지.

## 5) 장애 대응
- healthz/readyz DOWN: `openclaw gateway status` 확인
- session_status 실패: OpenClaw 세션 활성 여부 확인
- Telegram 알림 실패: bot token/chat_id 확인 (`getUpdates`)
