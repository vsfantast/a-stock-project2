#!/bin/bash
# 自动检测：session文件超过600秒没更新 → 触发自救
SESSION_FILE="/home/ubuntu/.cc-connect/sessions/a-stock-bot_a4e5b03f.json"
MAX_AGE=600  # 10分钟

if [ -f "$SESSION_FILE" ]; then
    NOW=$(date +%s)
    FILE_AGE=$(stat -c %Y "$SESSION_FILE" 2>/dev/null || echo $NOW)
    AGE=$((NOW - FILE_AGE))
    if [ $AGE -gt $MAX_AGE ]; then
        echo "[$(date)] Session ${AGE}秒未更新，触发自救" >> /tmp/auto_heal.log
        bash /home/ubuntu/a-stock-project/rescue.sh >> /tmp/auto_heal.log 2>&1
    fi
fi
