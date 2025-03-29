#coding:UTF-8
# インストールした discord.py を読み込む
import discord
import asyncio
import logging
from dotenv import load_dotenv
import os

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

# 変数の読み込み(BOT_ENV=production python bot.py)
env = os.getenv("BOT_ENV", "development")
load_dotenv(dotenv_path=f".env.{env}")

logger.info('load_dotenv:.env.{env}')

# Bot Token
TOKEN = os.getenv("DISCORD_TOKEN")

# チャンネルID
AISATSU_CHANNEL_ID = int(os.getenv("AISATSU_CHANNEL_ID"))
UNEI_CHANNEL_ID = int(os.getenv("UNEI_CHANNEL_ID"))
TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID"))
TALK_CHANNEL_ID = int(os.getenv("TALK_CHANNEL_ID"))

# 権限関連
ID_CHANNEL_README = int(os.getenv("ID_CHANNEL_README"))
ID_ROLE_WELCOME = int(os.getenv("ID_ROLE_WELCOME"))
TARGET_MESSAGE_ID = int(os.getenv("TARGET_MESSAGE_ID"))

# リアクション絵文字
REACTION_EMOJI = os.getenv("REACTION_EMOJI")

# 接続に必要なオブジェクトを生成
Intents = discord.Intents.default()
Intents.members = True
Intents.message_content = True
client = discord.Client(intents=Intents)

## 起動時の挨拶をする
@client.event
async def on_ready():
    # 起動したらアクティビティを変更する
    await client.change_presence(activity=discord.Game(name='Discord'))
    # 挨拶する
    test_channel = client.get_channel(TEST_CHANNEL_ID)
    if not test_channel:
        return
    
    await test_channel.send('案内BOTが起動しました。ｺﾝﾁﾊ!')
    read_me_channel = client.get_channel(ID_CHANNEL_README)
    
    if not read_me_channel:
        return

    # すでにリアクションがあるか確認し、なければ追加
    notice_message = await read_me_channel.fetch_message(TARGET_MESSAGE_ID)

    has_reaction = False

    for reaction in notice_message.reactions:
        if str(reaction.emoji) == REACTION_EMOJI:
            has_reaction = True
            # Bot以外の 😎 リアクションは削除
            async for user in reaction.users():
                if user != client.user:
                    await notice_message.remove_reaction(reaction.emoji, user)
        else:
            # 😎 以外のリアクションは全削除
            async for user in reaction.users():
                await notice_message.remove_reaction(reaction.emoji, user)

    # 😎 が付いていなければ、Botが付ける
    if not has_reaction:
        await notice_message.add_reaction(REACTION_EMOJI)

# Discordから終了させる場合の処理
# @client.event
# async def on_message(message):
#     # メッセージ送信者がBotだった場合は無視する
#     if message.author.bot:
#         return
#     if message.author == client.user:
#         return
#     if message.content =='/bot_shutdown':
#         unei_channel = client.get_channel(UNEI_CHANNEL_ID)
#         await unei_channel.send('案内BOTを終了します。ｻｲﾅﾗ!')
#         exit()

# メンバー参加時に案内をする。
@client.event
async def on_member_join(member):
    # 5秒間待つ
    await asyncio.sleep(5)
    # 挨拶チャンネルに発言する
    aisatsu_channel = client.get_channel(AISATSU_CHANNEL_ID)
    join_message = member.mention + 'さん\n猫羅のファンミーティングサーバーへようこそ！\nまずは<#1087067734828925119>をお読みください。\n<#1087067734828925119>でリアクションをすることによって各チャンネルへアクセスできるようになります。\nよろしくおねがいします。m(__)m\nﾋﾟﾎﾟ'
    logger.info('YOKOSO')
    await aisatsu_channel.send(join_message)

# 非常植民ロールがついたら告知する
@client.event
async def on_member_update(before, after):
    ROLEID = 1087302848393531453
    Guild = before.guild
    Role = Guild.get_role(ROLEID)

    if not Role in before.roles and Role in after.roles:
        TALK_channel = client.get_channel(TALK_CHANNEL_ID)
        welcome_message = '@everyone\n' + after.name + 'さんが非常食民になりました。ようこそ！みんな仲良くしてね。'
        await TALK_channel.send(welcome_message)

# ボイスチャンネルに参加した場合の通知
@client.event
async def on_voice_state_update(user, before, after):
    if before.channel != after.channel:
        botRoom = client.get_channel(TALK_CHANNEL_ID)
        if after.channel is not None:
            await botRoom.send("【VC】**" + after.channel.name + "** に、__" + user.display_name + "__  が入室しました")
            logger.info(user.display_name + 'in voice chat')
        else:
            await botRoom.send("【VC】**" + before.channel.name + "** から、__" + user.display_name + "__  が退室しました")
            logger.info(user.display_name + 'leave voice chat')

# リアクションをつけたユーザーに自動でロールをつけるためのメソッド
@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != ID_CHANNEL_README:
        return
    if payload.message_id != TARGET_MESSAGE_ID:
        return
    if payload.user_id == client.user.id:
        return  # Bot自身のリアクションは無視
    
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    read_me_channel = client.get_channel(ID_CHANNEL_README)
    test_channel = client.get_channel(TEST_CHANNEL_ID)
    message = await read_me_channel.fetch_message(payload.message_id)
    
    if str(payload.emoji) != REACTION_EMOJI:
        await message.remove_reaction(payload.emoji, member)
        return
    
    role = guild.get_role(ID_ROLE_WELCOME)
    if not member or not role:
        return

    if role in member.roles:
        # 既にロールを持っている → 外す
        await member.remove_roles(role)
        await test_channel.send(f"{member.mention} のロールを外しました。")
    else:
        # ロールを持っていない → 付ける
        await member.add_roles(role)
        await test_channel.send(f"{member.mention} にロールを付与しました。")

    # ユーザーの😎リアクションを削除（Botのだけ残す）
    await message.remove_reaction(REACTION_EMOJI, member)
 

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
