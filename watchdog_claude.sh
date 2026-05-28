#!/bin/bash
# Claude进程卡死检测：超过180秒未更新session → 重启
SESSION="/home/ubuntu/.cc-connect/sessions/a-stock-bot_a4e5b03f.json"
MAX_AGE=180

if [ -f "$SESSION" ]; then
    NOW=$(date +%s)
    FILE_AGE=$(stat -c %Y "$SESSION" 2>/dev/null || echo $NOW)
    AGE=$((NOW - FILE_AGE))
    if [ $AGE -gt $MAX_AGE ]; then
        echo "[$(date)] Claude卡死${AGE}秒，强制重启" >> /tmp/claude_watchdog.log
        sudo systemctl restart a-stock-bot
    fi
fi
