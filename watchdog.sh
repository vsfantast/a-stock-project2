#!/bin/bash
# 每5分钟检查cc-connect是否在8080监听，不在就重启
ss -tlnp | grep -q ":8080 " || {
    echo "[$(date)] 8080端口丢失，重启服务" >> /tmp/watchdog.log
    sudo systemctl restart a-stock-bot
}
