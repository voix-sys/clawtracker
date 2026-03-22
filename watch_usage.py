import re
import subprocess
from notifier import send_telegram


def run(cmd: str) -> str:
    return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=10)


def parse_usage(txt: str):
    # Example: 📊 Usage: 5h 98% left ... · Week 95% left ...
    m = re.search(r"5h\s+(\d+)%\s+left.*Week\s+(\d+)%\s+left", txt, re.DOTALL)
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))


def main():
    out = run("openclaw session_status")
    h5, week = parse_usage(out)
    if h5 is None:
        print("parse failed")
        return

    if h5 <= 20 or week <= 20:
        ok, msg = send_telegram(f"⚠️ ClawTracker 사용량 경고: 5h={h5}% / week={week}%")
        print("notify", ok, msg)
    else:
        print(f"healthy: 5h={h5}% week={week}%")


if __name__ == "__main__":
    main()
