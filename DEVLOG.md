# ClawTracker DEVLOG

## 2026-03-22 ~ 2026-03-23 진행 현황

### 완료
1. 프로젝트 초기화 및 GitHub 업로드
   - repo: https://github.com/voix-sys/clawtracker
   - 초기 커밋 완료 (main)

2. MVP 대시보드 구현 (`app.py`)
   - OpenClaw session/status 패널
   - gateway healthz/readyz 체크
   - 최근 로그 패널
   - 5초 자동 새로고침

3. 알림 모듈 뼈대 구현
   - `notifier.py`: Telegram sendMessage 래퍼
   - `watch_usage.py`: session_status 파싱 후 임계치 알림
   - `.env.example` 추가

4. 기본 문서화
   - `README.md` 실행 방법/구성 반영
   - `requirements.txt` 정리

### 현재 진행 중 (대표님 지시 반영)
- 우선순위: 가독성 강화(v1.1)
- 목표:
  1) KPI 위계 강화 (비용/장애 우선)
  2) Live feed 텍스트 대비/가독성 개선
  3) 색상 규칙 정리 (#FF0000 = critical only)
  4) 로컬 우선 + Tailscale 외부 접근 전제 유지

### 대기 항목
- Telegram 신규 봇 토큰 수령 후 실알림 활성화
- SSE/WebSocket 실시간 스트림 고도화
- sanitize view(외부 공유용 마스킹)

### 리스크/메모
- GitHub 토큰은 채팅으로 전달받아 사용됨 → 작업 후 회전(폐기/재발급) 권장
- 현재는 로컬 MVP 중심, 외부 공개는 Tailscale 전제
