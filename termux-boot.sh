#!/data/data/com.termux/files/usr/bin/sh
# Termux:Boot 开机自启脚本：拉起 JowOS 同步服务器
# 安装 Termux:Boot 后，把它放到 ~/.termux/boot/ 下并 chmod +x
# 注意：把下面 JOWOS_KEY 换成和你 JowOS 页面里填的同一个长随机口令
termux-wake-lock
cd "$HOME"
export JOWOS_KEY="换成你自己的长随机口令"
nohup python3 "$HOME/jowos-sync-server.py" \
  --host 0.0.0.0 --port 8765 --data "$HOME/jowos-data.json" \
  > "$HOME/jowos-sync.log" 2>&1 &
echo "started jowos sync server, pid $!"
