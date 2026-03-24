from datetime import datetime
import json
import re
import subprocess
from urllib.request import Request, urlopen
from urllib.error import URLError

import streamlit as st

st.set_page_config(page_title="ClawTracker", page_icon="🦞", layout="wide")

REFRESH_SEC = 5


def run_cmd(cmd: str) -> str:
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=12)
        return out.strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR]\n{e.output.strip()}"
    except Exception as e:
        return f"[ERROR] {e}"


def run_json(cmd: str) -> dict | None:
    raw = run_cmd(cmd)
    if raw.startswith("[ERROR"):
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def check_http(url: str) -> tuple[bool, str]:
    try:
        req = Request(url, headers={"User-Agent": "ClawTracker/0.2"})
        with urlopen(req, timeout=3) as r:
            return True, f"{r.status} {r.reason}"
    except URLError as e:
        return False, f"DOWN ({e.reason})"
    except Exception as e:
        return False, f"DOWN ({e})"


def parse_usage(text: str) -> dict:
    out = {"h5": None, "week": None, "context": None, "model": "unknown"}

    m_model = re.search(r"Model:\s*([^\n]+)", text)
    if m_model:
        out["model"] = m_model.group(1).strip()
    else:
        m_model2 = re.search(r"\b(gpt-[\w\.-]+|gemini-[\w\.-]+|claude-[\w\.-]+|openai-codex/[\w\.-]+)\b", text)
        if m_model2:
            out["model"] = m_model2.group(1)

    m_h5 = re.search(r"5h\s+(\d+)%\s+left", text)
    m_week = re.search(r"Week\s+(\d+)%\s+left", text)
    if m_h5:
        out["h5"] = int(m_h5.group(1))
    if m_week:
        out["week"] = int(m_week.group(1))

    m_ctx = re.search(r"Context:\s*([^\n]+)", text)
    if m_ctx:
        ctx = m_ctx.group(1).strip()
        out["context"] = ctx.split("·")[0].strip()
    else:
        m_ctx2 = re.search(r"\b\d+k/\d+k\s*\(\d+%\)\b", text)
        if m_ctx2:
            out["context"] = m_ctx2.group(0)

    return out


def usage_from_status_json(payload: dict | None) -> dict:
    out = {"h5": None, "week": None, "context": None, "model": "unknown"}
    if not payload:
        return out

    # provider usage windows (usedPercent => convert to left)
    providers = (payload.get("usage") or {}).get("providers") or []
    if providers:
        windows = providers[0].get("windows") or []
        for w in windows:
            label = str(w.get("label", "")).lower()
            used = w.get("usedPercent")
            if isinstance(used, (int, float)):
                left = max(0, min(100, int(round(100 - used))))
                if label == "5h":
                    out["h5"] = left
                elif label == "week":
                    out["week"] = left

    sessions = (payload.get("sessions") or {}).get("recent") or []
    if sessions:
        s0 = sessions[0]
        out["model"] = s0.get("model") or out["model"]
        total = s0.get("totalTokens")
        ctx = s0.get("contextTokens")
        used_pct = s0.get("percentUsed")
        if isinstance(total, int) and isinstance(ctx, int):
            if isinstance(used_pct, int):
                out["context"] = f"{total}/{ctx} ({used_pct}%)"
            else:
                out["context"] = f"{total}/{ctx}"

    return out


def health_level(health_ok: bool, ready_ok: bool, h5: int | None) -> tuple[str, str]:
    if not health_ok or not ready_ok:
        return "🔴 CRITICAL", "critical"
    if h5 is not None and h5 <= 20:
        return "🟠 WARNING", "warning"
    return "🟢 NORMAL", "normal"


# ---------- Data collection ----------
status_text = run_cmd("openclaw status 2>/dev/null || true")
status_json = run_json("openclaw status --usage --json 2>/dev/null || true")

# `openclaw session_status` may be unavailable in some installs.
session_text = run_cmd("openclaw session_status 2>/dev/null || true")
if "unknown command" in session_text.lower() or "[error" in session_text.lower() or not session_text.strip():
    session_text = status_text

logs_text = run_cmd("openclaw logs --tail 120 2>/dev/null || true")

health_ok, health_msg = check_http("http://127.0.0.1:18789/healthz")
ready_ok, ready_msg = check_http("http://127.0.0.1:18789/readyz")

usage = usage_from_status_json(status_json)
if usage.get("h5") is None and usage.get("week") is None:
    usage = parse_usage(session_text)

level_text, level_class = health_level(health_ok, ready_ok, usage.get("h5"))

# ---------- UI ----------
st.markdown(
    """
    <style>
    .stApp { background: #0f172a; color: #e2e8f0; }
    .card {
      background: rgba(15, 23, 42, 0.82);
      border: 1px solid rgba(100, 116, 139, 0.28);
      border-radius: 10px;
      padding: 14px;
      margin-bottom: 10px;
    }
    .kpi { font-size: 2rem; font-weight: 800; line-height: 1.15; }
    .muted { color: #94a3b8; font-size: 0.84rem; }
    .critical { color: #ff0000; }
    .warning { color: #f59e0b; }
    .normal { color: #10b981; }
    .logbox {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.88rem;
      line-height: 1.45;
      background: #020617;
      border: 1px solid rgba(51,65,85,0.8);
      border-radius: 8px;
      padding: 10px;
      max-height: 360px;
      overflow-y: auto;
      white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🦞 ClawTracker — OpenClaw Operations")

c1, c2, c3, c4 = st.columns([1.4, 1.1, 1.1, 1.2])
with c1:
    st.markdown(f"<div class='card'><div class='muted'>GLOBAL STATUS</div><div class='kpi {level_class}'>{level_text}</div><div class='muted'>Refresh: {REFRESH_SEC}s</div></div>", unsafe_allow_html=True)
with c2:
    h5 = usage.get("h5")
    h5_text = f"{h5}%" if h5 is not None else "N/A"
    st.markdown(f"<div class='card'><div class='muted'>5H QUOTA LEFT</div><div class='kpi'>{h5_text}</div></div>", unsafe_allow_html=True)
with c3:
    wk = usage.get("week")
    wk_text = f"{wk}%" if wk is not None else "N/A"
    st.markdown(f"<div class='card'><div class='muted'>WEEK QUOTA LEFT</div><div class='kpi'>{wk_text}</div></div>", unsafe_allow_html=True)
with c4:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<div class='card'><div class='muted'>LAST REFRESH</div><div class='kpi' style='font-size:1.35rem'>{now}</div><div class='muted'>{usage.get('model','unknown')}</div></div>", unsafe_allow_html=True)

if not health_ok or not ready_ok:
    st.error("Gateway Unreachable or Not Ready. Dashboard is in degraded/offline mode.")
    st.markdown("<div class='card critical'><b>OFFLINE MODE</b> · 실시간 수집이 중단되었습니다. gateway/daemon 상태를 확인하세요.</div>", unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

with left:
    st.subheader("🎯 Priority Panel")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("<div class='card'><div class='muted'>HEALTHZ</div><div class='kpi' style='font-size:1.15rem'>" + health_msg + "</div></div>", unsafe_allow_html=True)
    with p2:
        st.markdown("<div class='card'><div class='muted'>READYZ</div><div class='kpi' style='font-size:1.15rem'>" + ready_msg + "</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='muted'>SESSION STATUS RAW</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='logbox'>{session_text}</div>", unsafe_allow_html=True)

    st.subheader("📡 Live Activity (Recent Logs)")
    st.markdown(f"<div class='logbox'>{logs_text}</div>", unsafe_allow_html=True)

with right:
    st.subheader("🧵 Sessions / Runtime")
    st.markdown(f"<div class='logbox'>{status_text}</div>", unsafe_allow_html=True)

    st.subheader("🧠 Context")
    st.markdown(f"<div class='card'><div class='muted'>Current Context</div><div style='font-size:1rem;font-weight:700'>{usage.get('context') or 'N/A'}</div></div>", unsafe_allow_html=True)

st.caption("v0.2 readability mode · red color is reserved for CRITICAL only")

# auto refresh
st.markdown(
    f"""
    <script>
      setTimeout(function() {{ window.location.reload(); }}, {REFRESH_SEC * 1000});
    </script>
    """,
    unsafe_allow_html=True,
)
