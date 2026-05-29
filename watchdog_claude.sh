#!/bin/bash
# Claude卡死检测：最近有未回复消息 + session超180秒不更新 → 重启
SESSION="/home/ubuntu/.cc-connect/sessions/a-stock-bot_a4e5b03f.json"
MAX_AGE=180
COOLDOWN=600
COOLDOWN_FILE="/tmp/.last_watchdog_restart"

if [ -f "$SESSION" ]; then
    NOW=$(date +%s)
    FILE_AGE=$(stat -c %Y "$SESSION" 2>/dev/null || echo $NOW)
    AGE=$((NOW - FILE_AGE))

    if [ $AGE -gt $MAX_AGE ]; then
        # 检查是否有未回复的用户消息（最后一条是user才算真卡死）
        HAS_UNANSWERED=$(python3 -c "
import json
with open('$SESSION') as f:
    d=json.load(f)
hist=d['sessions'].get('s1',{}).get('history',[])
if hist and hist[-1]['role']=='user':
    print('yes')
" 2>/dev/null)

        if [ "$HAS_UNANSWERED" = "yes" ]; then
            LAST_RESTART=$(cat "$COOLDOWN_FILE" 2>/dev/null || echo 0)
            SINCE_LAST=$((NOW - LAST_RESTART))

            if [ $SINCE_LAST -gt $COOLDOWN ]; then
                echo "[$(date)] 真卡死${AGE}s，有未回复消息，重启" >> /tmp/claude_watchdog.log
                echo "$NOW" > "$COOLDOWN_FILE"
                sudo systemctl restart a-stock-bot
            fi
        fi
    fi
fi
