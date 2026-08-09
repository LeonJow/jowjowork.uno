#!/data/data/com.termux/files/usr/bin/sh
# Termux:Boot 开机自启脚本：拉起 JowOS 同步服务器
# 安装 Termux:Boot 后，把它放到 ~/.termux/boot/ 下并 chmod +x
# 同步口令由同目录 jowos-key.txt 提供（jowos_setup.sh 首次部署时已写入），
# 服务端会自动读取，无需在此硬编码。如需临时覆盖，可在此前 export JOWOS_KEY=...
termux-wake-lock
cd "$HOME"
nohup python3 "$HOME/jowos-sync-server.py" \
  --host 0.0.0.0 --port 8765 --data "$HOME/jowos-data.json" \
  > "$HOME/jowos-sync.log" 2>&1 &
echo "started jowos sync server, pid $!"
