#!/bin/sh
# JowOS 同步服务一键部署脚本（在 Termux 里运行）
# 用法： sh /sdcard/Download/jowos_setup.sh
# 前置：先运行一次 termux-setup-storage（授权访问 /sdcard/Download）
set -e

JOWOS_KEY="d43805430ead8f7eb0e7bd4d7aea9046044cadd1c0bd7187"
SRC=/sdcard/Download/jowos-sync-server.py
HOME_DIR="$HOME/jowos"

echo "==> [1/5] 确保 python3"
if command -v python3 >/dev/null 2>&1; then
  echo "    python3 已存在: $(command -v python3)"
else
  echo "    python3 缺失，安装中（需联网）..."
  pkg update -y && pkg install -y python
fi

echo "==> [2/5] 建立目录并拷贝服务端"
mkdir -p "$HOME_DIR"
if [ ! -f "$SRC" ]; then
  echo "❌ 找不到 $SRC，请确认已 adb push 到手机，且已运行 termux-setup-storage"
  exit 1
fi
cp "$SRC" "$HOME_DIR/jowos-sync-server.py"

echo "==> [3/5] 写入密钥文件"
printf '%s\n' "$JOWOS_KEY" > "$HOME_DIR/jowos-key.txt"
chmod 600 "$HOME_DIR/jowos-key.txt"

echo "==> [4/5] 停止旧实例（如有）"
pkill -f jowos-sync-server.py 2>/dev/null || true
sleep 1

echo "==> [5/5] 后台启动服务"
cd "$HOME_DIR"
nohup python3 "$HOME_DIR/jowos-sync-server.py" --host 0.0.0.0 --port 8765 --data "$HOME_DIR/jowos-data.json" > "$HOME_DIR/server.log" 2>&1 &
sleep 2

echo "---- server.log ----"
cat "$HOME_DIR/server.log" 2>/dev/null
echo "---------------------"
echo "✅ 部署完成。手机内网地址： http://$(ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1):8765"
echo "    如要开机自启，请安装 Termux:Boot，并把本脚本软链到 ~/.termux/boot/ 下。"
