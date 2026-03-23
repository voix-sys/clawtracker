import time
import subprocess
from watch_usage import parse_usage
from notifier import send_telegram

CHECK_EVERY_SEC = 300  # 5m
WARN_5H = 30
CRIT_5H = 15
WARN_WEEK = 30
CRIT_WEEK = 15


def run_status() -> str:
    return subprocess.check_output("openclaw session_status", shell=True, text=True, stderr=subprocess.STDOUT, timeout=12)


def classify(h5: int | None, week: int | None) -> tuple[str, bool]:
    if h5 is None or week is None:
        return "unknown", False
    if h5 <= CRIT_5H or week <= CRIT_WEEK:
        return "critical", True
    if h5 <= WARN_5H or week <= WARN_WEEK:
        return "warning", True
    return "normal", False


def main():
    last_sent_level = None
    while True:
        try:
            text = run_status()
            h5, week = parse_usage(text)
            level, should_alert = classify(h5, week)
            if should_alert and level != last_sent_level:
                icon = "🔴" if level == "critical" else "🟠"
                ok, msg = send_telegram(f"{icon} ClawTracker 사용량 {level.upper()}\n5h={h5}% / week={week}%")
                print("alert", level, ok, msg)
                if ok:
                    last_sent_level = level
            elif level == "normal":
                last_sent_level = None
            print(f"status: level={level}, 5h={h5}, week={week}")
        except Exception as e:
            print("loop_error", e)
        time.sleep(CHECK_EVERY_SEC)


if __name__ == "__main__":
    main()
