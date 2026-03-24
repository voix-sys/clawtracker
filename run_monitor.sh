#!/usr/bin/env bash
set -euo pipefail
cd /home/k1/.openclaw/workspace/clawtracker
source .venv/bin/activate
set -a
[ -f .env.local ] && source .env.local
set +a
exec python monitor_loop.py
