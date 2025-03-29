# nekora-discordbot

## 概要

Vtuberの[猫羅サキ](https://x.com/nekoneko_nekora)さんのDiscordサーバーで使用している歓迎用DiscordBOTです。基本的に自分用に公開しています。

## サーバー内での動き

* 新規入室者がいた場合、ようこそメッセージを送りつつ規約チャンネルを読むように促します。  
* 規約チャンネルで、ロール付与BOTがつけたリアクションを押すと参加者ロールが付与され、雑談チャンネルに「〇〇さんが非常食民になりました！」というテキストを流して参加者に新規参加者を通知します。
* ボイスチャンネルに参加した人がいた場合、指定したテキストチャンネルに入室と退室の通知を行います。
* ログも出します。同じディレクトリ内に指定したログを出力します。
* 起動時に運営チャンネルに起動メッセージを出します。  
* proxmox上にあるLXCコンテナでsystemctlを使用して立ち上げています。

## デプロイ方法

* initファイルをいい感じに書いてsystemd/system配下に何かしらの形で置きます。

* 【一例】discord_nekora_discordbot.service

```initfile
[Unit]
Description=discord_nekora_discordbot
After=network.target

[Service]
Type=simple

WorkingDirectory=/home/yuri/bin/nekora_discordbot

Environment=BOT_ENV=production

ExecStart=/home/yuri/bin/nekora_discordbot/.nekora_venv/bin/python3 /home/yuri/bin/nekora_discordbot/main.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

StandardOutput=append:/home/yuri/bin/nekora_discordbot/bot.log
StandardError=append:/home/yuri/bin/nekora_discordbot/bot_error.log
```