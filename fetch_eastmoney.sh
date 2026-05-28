#!/bin/bash
# 交易时段自动拉取东财数据到本地缓存
BLOB_URL="https://jsonblob.com/api/jsonBlob/019e6c05-9fb5-784c-b0b6-1c2f159a84ee"
CACHE_FILE="/home/ubuntu/.eastmoney_cache/latest.json"

while true; do
    H=$(date +%H%M)
    DAY=$(date +%u)
    
    # 周一至周五 9:25-15:05
    if [ $DAY -le 5 ] && [ $H -ge 0925 ] && [ $H -le 1505 ]; then
        curl -s "$BLOB_URL" -o "$CACHE_FILE" 2>/dev/null
    fi
    sleep 120
done
