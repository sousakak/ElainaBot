from config import *
import asyncio, datetime

async def on_ready(): # イレイナさんがログインした時に実行する
  print('{0.user}としてログインしています'.format(client)) # ログインのログを流す
  channel = client.get_channel(gmMessageChannel) # log メッセージを流すチャンネルを決める
  async with channel.typing(): # 「イレイナが入力中」を表示する
    await asyncio.sleep(1)
    # await channel.send(loginMessage)
  activity = discord.Game(name="魔女の旅々", start=datetime.datetime.now()) # 「魔女の旅々をプレイ中」を表示する
  await client.change_presence(activity=activity, status=discord.Status.idle)
  await commandTree.sync() # コマンド一覧を同期する