#coding:UTF-8
# インストールした discord.py を読み込む
import discord
import time
import logging

# ログの出力名を設定
logger = logging.getLogger('DisbotLogging')

#ログレベルの設定
logger.setLevel(10)

# ログのコンソール出力の設定
sh = logging.StreamHandler()
logger.addHandler(sh)

# ログのファイル出力先を設定
fh = logging.FileHandler('discordbot.log')
logger.addHandler(fh)

# ログの出力形式の設定
formatter = logging.Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.info('DiscordBOT Start')

# 自分のBotのアクセストークンに置き換えてください
TOKEN = "BOTアクセストークン"

# チャンネルID・ロールID
AISATSU_CHANNEL_ID = "挨拶チャンネルのID"
UNEI_CHANNEL_ID = "運営チャンネルのID"
TEST_CHANNEL_ID = "テストチャンネルのID"
TALK_CHANNEL_ID = "雑談チャンネルのID"
ROLEID = "反応させたいロールID"

# 接続に必要なオブジェクトを生成
# client = discord.Client(intents=discord.Intents.all())

Intents = discord.Intents.default()
Intents.members = True
client = discord.Client(intents=Intents)

## 起動時の挨拶をする
@client.event
async def on_ready():
    # 起動したらアクティビティを変更する
    await client.change_presence(activity=discord.Game(name='Discord'))
    # 挨拶する
    channel = client.get_channel(TEST_CHANNEL_ID)
    await channel.send('案内BOTが起動しました。ｺﾝﾁﾊ!')

# メンバー参加時に案内をする。
@client.event
async def on_member_join(member):
    # 5秒間待つ
    time.sleep(5)
    # 挨拶チャンネルに発言する
    channel = client.get_channel(AISATSU_CHANNEL_ID)
    message = member.mention + 'さん\n猫羅のファンミーティングサーバーへようこそ！\nまずは<#1087067734828925119>をお読みください。\n<#1087067734828925119>でリアクションをすることによって各チャンネルへアクセスできるようになります。\nよろ>しくおねがいします。m(__)m\nﾋﾟﾎﾟ'
    await channel.send(message)

@client.event
async def on_member_update(before, after):
    Guild = before.guild
    Role = Guild.get_role(ROLEID)

    if not Role in before.roles and Role in after.roles:
        channel = client.get_channel(TALK_CHANNEL_ID)
        message = '@everyone\n' + after.name + 'さんが非常食民になりました。ようこそ！みんな仲良くしてね。'
        await channel.send(message)

# ボイスチャンネルに参加した場合の通知
@client.event
async def on_voice_state_update(user, before, after):
    if before.channel != after.channel:
        botRoom = client.get_channel(TALK_CHANNEL_ID)
        if after.channel is not None:
            await botRoom.send("**" + after.channel.name + "** に、__" + user.display_name + "__  が入室しました")
        else:
            await botRoom.send("**" + before.channel.name + "** から、__" + user.display_name + "__  が退室しました")

# メンバー退出時に案内をする。
#@client.event
#async def on_member_remove(member):
    # 運営チャンネルに発言する
    #channel = client.get_channel(UNEI_CHANNEL_ID)
    #message = member.display_name + 'さんが退出しました'
    #await channel.send(message)

# Discordから終了させる場合の処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.author == client.user:
        return
    if message.content =='/bot_shutdown':
        channel = client.get_channel(UNEI_CHANNEL_ID)
        await message.channel.send('案内BOTを終了します。ｻｲﾅﾗ!')
        exit()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)