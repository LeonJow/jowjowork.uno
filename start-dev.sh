#!/bin/bash
# JowJow Work 博客 - 本地开发启动脚本
# 同时启动 Hugo 服务器 + Decap CMS 本地代理

set -e

BLOG_DIR="$HOME/Documents/GitHub/jowjowork.uno"

echo "🚀 启动博客开发环境..."
echo ""

# 启动 Decap CMS 本地代理（后台）
echo "📝 启动 Decap CMS 代理..."
npx decap-server &
DECAP_PID=$!
echo "   Decap CMS PID: $DECAP_PID"

# 启动 Hugo 服务器（前台）
echo "🌐 启动 Hugo 服务器 (http://localhost:1313)"
echo "🔐 后台管理: http://localhost:1313/admin/"
echo ""
cd "$BLOG_DIR"
hugo server --buildDrafts --disableFastRender --bind 0.0.0.0

# 退出时清理
kill $DECAP_PID 2>/dev/null
