#!/bin/bash
# 会话超过200条自动截断到100条
FILE="/home/ubuntu/.cc-connect/sessions/a-stock-bot_a4e5b03f.json"
COUNT=$(python3 -c "
import json
with open('$FILE') as f:
    d=json.load(f)
print(len(d['sessions']['s1']['history']))
" 2>/dev/null)
if [ -n "$COUNT" ] && [ "$COUNT" -gt 200 ]; then
    cp "$FILE" "$FILE.bak"
    python3 -c "
import json
with open('$FILE') as f: d=json.load(f)
d['sessions']['s1']['history'] = d['sessions']['s1']['history'][-100:]
with open('$FILE','w') as f: json.dump(d,f,ensure_ascii=False)
"
    echo "[$(date)] 截断 $COUNT → 100" >> /tmp/trim.log
fi
