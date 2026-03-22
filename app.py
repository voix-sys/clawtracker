import json
import subprocess
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

import streamlit as st

st.set_page_config(page_title="ClawTracker", page_icon="🦞", layout="wide")

REFRESH_SEC = 5


def run_cmd(cmd: str) -> str:
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=8)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {e.output.strip()}"
    except Exception as e:
        return f"[ERROR] {e}"


def check_http(url: str) -> str:
    try:
        req = Request(url, headers={"User-Agent": "ClawTracker/0.1"})
        with urlopen(req, timeout=3) as r:
            return f"{r.status} {r.reason}"
    except URLError as e:
        return f"DOWN ({e.reason})"
    except Exception as e:
        return f"DOWN ({e})"


st.title("🦞 ClawTracker — OpenClaw Live Ops")
st.caption("대표님용 실시간 운영 패널 · 5초 자동 새로고침")

c1, c2, c3, c4 = st.columns(4)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with c1:
    st.metric("Now", now)
with c2:
    st.metric("Refresh", f"{REFRESH_SEC}s")
with c3:
    st.metric("healthz", check_http("http://127.0.0.1:18789/healthz"))
with c4:
    st.metric("readyz", check_http("http://127.0.0.1:18789/readyz"))

st.subheader("📊 Session / Model Usage")
ss = run_cmd("openclaw session_status 2>/dev/null || true")
st.code(ss or "No data", language="text")

left, right = st.columns(2)
with left:
    st.subheader("🧵 Sessions")
    sessions = run_cmd("openclaw status 2>/dev/null || true")
    st.code(sessions, language="text")

with right:
    st.subheader("📜 Recent OpenClaw Logs")
    logs = run_cmd("openclaw logs --tail 80 2>/dev/null || true")
    st.code(logs, language="text")

st.subheader("🎯 Hunt Summary (MVP)")
st.info("오늘 사냥 성공률 87% (임시값) · 다음 단계: 실시간 task 완료율 계산 연결")

st.markdown("---")
st.caption("ClawTracker MVP v0.1 · local-first")

# auto refresh
st.markdown(
    f"""
    <script>
        setTimeout(function() {{
            window.location.reload();
        }}, {REFRESH_SEC * 1000});
    </script>
    """,
    unsafe_allow_html=True,
)
