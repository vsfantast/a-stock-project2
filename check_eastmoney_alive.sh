#!/bin/bash
# 监测东财数据是否断流：超过5分钟未更新 → 飞书告警
BLOB="https://jsonblob.com/api/jsonBlob/019e7703-88cd-7afc-9d79-696ad1993c7a"
ALERT_FILE="/tmp/.eastmoney_alerted"
WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/f281cf20-e638-494c-b1d7-29742c3fa8b2"

# 只在交易时段检查
H=$(date +%H%M)
DAY=$(date +%u)
[ $DAY -gt 5 ] && exit 0
[ $H -lt 0925 ] && exit 0
[ $H -gt 1505 ] && exit 0

# 获取更新时间
UPDATED=$(curl -s "$BLOB" 2>/dev/null | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('updated',''))" 2>/dev/null)

if [ -z "$UPDATED" ]; then
    # 完全没数据
    if [ ! -f "$ALERT_FILE" ]; then
        curl -s -X POST "$WEBHOOK" -H "Content-Type: application/json" \
          -d '{"msg_type":"text","content":{"text":"🚨 东财数据断流！jsonblob完全无数据，Mac可能关机了"}}' > /dev/null
        touch "$ALERT_FILE"
    fi
    exit
fi

# 解析时间差
NOW_SEC=$(date +%s)
DATA_H=$(echo "$UPDATED" | cut -d: -f1)
DATA_M=$(echo "$UPDATED" | cut -d: -f2)
DATA_SEC=$((10#$DATA_H * 3600 + 10#$DATA_M * 60))
NOW_H=$(date +%H)
NOW_M=$(date +%M)
NOW_S=$((10#$NOW_H * 3600 + 10#$NOW_M * 60))
DIFF=$((NOW_S - DATA_SEC))
[ $DIFF -lt 0 ] && DIFF=$((DIFF + 86400))

if [ $DIFF -gt 300 ]; then
    if [ ! -f "$ALERT_FILE" ]; then
        curl -s -X POST "$WEBHOOK" -H "Content-Type: application/json" \
          -d "{\"msg_type\":\"text\",\"content\":{\"text\":\"🚨 东财数据延迟${DIFF}秒！上次更新:${UPDATED}，Mac可能休眠或断网\"}}" > /dev/null
        touch "$ALERT_FILE"
    fi
else
    rm -f "$ALERT_FILE"  # 恢复了，清除告警标记
fi
