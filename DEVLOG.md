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

### 2026-03-24 08:xx 업데이트
- `app.py` v0.2 반영 완료
  - Global status 레벨 배지(NORMAL/WARNING/CRITICAL)
  - 5h/Week quota KPI 카드 추가
  - healthz/readyz Priority 패널 강화
  - 로그 가독성(폰트/행간/컨테이너) 개선
  - Gateway 비정상 시 degraded/offline 경고 표시
- 색상 규칙 반영: 빨강은 critical 의미로만 사용

### 2026-03-24 08:1x 업데이트
- `watch_usage.py` 경고/위험 임계치 2단계로 개선
  - 주의: 30% 이하, 위험: 15% 이하
- `monitor_loop.py` 추가
  - 5분 간격 자동 체크
  - 레벨 변경 시 Telegram 자동 알림

### 2026-03-24 10:xx 업데이트
- `app.py` OFFLINE MODE 경고 카드 추가
- `RUNBOOK.md` 추가 (실행/운영/장애 대응/Tailscale 접근 요약)
- README에서 운영 가이드 연결

### 대기 항목
- Telegram 신규 봇 토큰 수령 후 실알림 활성화
- SSE/WebSocket 실시간 스트림 고도화
- sanitize view(외부 공유용 마스킹)

### 리스크/메모
- GitHub 토큰은 채팅으로 전달받아 사용됨 → 작업 후 회전(폐기/재발급) 권장
- 현재는 로컬 MVP 중심, 외부 공개는 Tailscale 전제
