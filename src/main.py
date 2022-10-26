# インストールした discord.py を読み込む
import discord
import re
import random
import os
from dotenv import load_dotenv

load_dotenv()
# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['TOKEN']
PREFIX = "/"
COMMAND_DICE = "dice"

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    author = message.author
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # メッセージがコマンドPREFIXでない場合無視
    if not message.content.startswith(PREFIX):
        return

    # コマンドの取得
    input = message.content.replace(PREFIX, "").split(" ")
    if not len(input) == 2:
        await message.channel.send("/dice 1d100 の形式で入力してください")
        return

    command = input[0]
    param = input[1]

    print({
        "command": command,
        "param": param,
    })
    # commandがDiceでない場合、終了
    if not command == COMMAND_DICE:
        return
    # パラメータチェック
    # paramを分解([0-9]+d[0-9]+形式：1d100とか 1diceで数字が100まで)
    match = re.match(r'^([1-9]{1}[0-9]?)d([1-9]{1}[0-9]{0,4})$', param)
    if not match:
        await message.channel.send("/dice 1d100 の形式で入力してください")
        return
    print(match.groups(), match.group(1), match.group(2))
    # 乱数を生成
    result = []
    for i in range(int(match.group(1))):
        num = random.randint(1, int(match.group(2)))
        result.append(num)
    print(result)

    # Authorに乱数を返却
    await message.channel.send(f"結果：{result}")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)