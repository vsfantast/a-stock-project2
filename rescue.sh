#!/bin/bash
# ==========================================
#  自救脚本 — 你唯一需要的一键救活命令
#  用法：bash /home/ubuntu/a-stock-project/rescue.sh
# ==========================================

echo "🚑 A-Stock-Bot 自救中..."

# 1. 强制写入模型环境变量 (防丢失)
mkdir -p /home/ubuntu/.claude
cat > /home/ubuntu/.claude/settings.local.json << 'ENVEOF'
{
  "permissions": {
    "allow": [
      "mcp__plugin_claude-mem_mcp-search__search"
    ]
  },
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_API_KEY": "sk-fefdce131af449638ee96a4692d84c91",
    "ANTHROPIC_AUTH_TOKEN": "sk-fefdce131af449638ee96a4692d84c91",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash",
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS": "1"
  }
}
ENVEOF

# 2. 确保 config.toml 端口是8080
if [ -f /home/ubuntu/a-stock-project/config.toml ]; then
    sed -i 's/port = "8082"/port = "8080"/' /home/ubuntu/a-stock-project/config.toml
fi

# 3. 检查 DeepSeek API 是否可达
echo -n "  DeepSeek API: "
if curl -s --connect-timeout 5 https://api.deepseek.com > /dev/null 2>&1; then
    echo "可达"
else
    echo "不通！请检查网络"
fi

# 4. 重启服务
echo "  重启 cc-connect ..."
sudo systemctl restart a-stock-bot
sleep 3

# 5. 验证
if ss -tlnp | grep -q ":8080 "; then
    echo "  ✅ 8080 端口正常"
else
    echo "  ❌ 8080 端口异常"
fi

if sudo systemctl is-active a-stock-bot | grep -q active; then
    echo "  ✅ 服务已启动"
else
    echo "  ❌ 服务启动失败"
fi

echo "🏁 自救完成。去飞书说句话测试。"
