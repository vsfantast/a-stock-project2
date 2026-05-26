#!/usr/bin/env python3
"""检查 cc-connect 是否有未回复的消息，有的话通知用户重发（同一问题不重复通知）"""
import json, subprocess, os
from datetime import datetime

SESSION_FILE = "/home/ubuntu/.cc-connect/sessions/a-stock-bot_a4e5b03f.json"
TRACKER_FILE = "/home/ubuntu/.cc-connect/missed_tracker.json"
PROJECT = "a-stock-bot"
GRACE_SECONDS = 120  # 2分钟内不算漏

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE) as f:
            return json.load(f)
    return {}

def save_tracker(t):
    os.makedirs(os.path.dirname(TRACKER_FILE), exist_ok=True)
    with open(TRACKER_FILE, "w") as f:
        json.dump(t, f)

def check_missed():
    if not os.path.exists(SESSION_FILE):
        return

    with open(SESSION_FILE) as f:
        data = json.load(f)

    tracker = load_tracker()
    active = data.get("active_session", {})
    sessions = data.get("sessions", {})

    for user_key, session_id in active.items():
        sdata = sessions.get(session_id, {})
        history = sdata.get("history", [])

        if not history:
            continue

        last_msg = history[-1]
        role = last_msg.get("role", "")
        content = last_msg.get("content", "")[:200]
        ts = last_msg.get("timestamp", "")

        # 跳过飞书（管理员终端）和 ssh 终端消息
        if user_key.startswith("feishu:"):
            continue
        if any(kw in content for kw in ["ubuntu@", "curl ", "cc-connect", "python3"]):
            continue

        # 有回复了，清除追踪
        if role != "user":
            if user_key in tracker:
                del tracker[user_key]
                save_tracker(tracker)
            continue

        # 计算等待时间
        try:
            msg_time = datetime.fromisoformat(ts.split("+")[0].split("[")[0])
            elapsed = (datetime.now().astimezone() - msg_time.replace(tzinfo=None)).total_seconds()
        except:
            elapsed = 999

        if elapsed < GRACE_SECONDS:
            continue

        # 同一个问题不重复通知
        if user_key in tracker:
            if tracker[user_key].get("content") == content:
                continue

        tracker[user_key] = {
            "content": content,
            "first_seen": datetime.now().isoformat(),
            "elapsed_min": round(elapsed / 60, 1),
        }
        save_tracker(tracker)

        platform, name = user_key.split(":", 1) if ":" in user_key else ("?", user_key)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ 漏消息！{name}({platform}) {round(elapsed/60,1)}分钟前: {content[:80]}")

        # 静默记录，不发提醒


if __name__ == "__main__":
    check_missed()
