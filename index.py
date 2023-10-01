### モジュールの取得 ###
import os
import discord
from discord.ext import tasks
import datetime, asyncio, random, hashlib
from google.oauth2.service_account import Credentials
from config import *
from commands import *
from events import *
from server import keep_alive


### ログイン成功のログ ###
@client.event
async def on_ready():  # イレイナさんがログインした時に実行する
  await on_ready_.on_ready()


### hello コマンド ###
@commandTree.command(name="hello", description="Hello world.")
async def hello(ctx: discord.Interaction):  # helloコマンドが送られたら
  await ctx.response.send_message("¡Hello world!")  # 「¡Hello world!」と送る


### confirm コマンド ###
@commandTree.command(
  name="confirm",
  description="新規参加者の承認をします",
)
@discord.app_commands.describe(  # 引数指定
  member="承認したいユーザーを選んでください")
@discord.app_commands.guild_only()
@discord.app_commands.checks.has_any_role(999258786449604708,
                                          985148474687373374
                                          )  # 指定したロールの人だけがコマンド実行できる
async def commandConfirm(ctx: discord.Interaction,
                         member: discord.Member):  # confirmコマンドが実行されたら
  await confirm.confirm(ctx,
                        member)  # commands ファイルの confirm.py にある confirm を実行する


@commandTree.context_menu(name='confirm'
                          )  # 人を右クリックしたときに「アプリ」に confirm ボタンを表示する
async def contextConfirm(ctx: discord.Interaction, member: discord.Member):
  await confirm.confirm(ctx,
                        member)  # commands ファイルの confirm.py にある confirm を実行する


### roll コマンド ###
@commandTree.command(name="dice", description="指定された数の中からランダムな数を表示します")
@discord.app_commands.describe(dice="さいころの最小値と最大値をカンマで区切ってください")
@discord.app_commands.rename(dice="さいころの目")
@discord.app_commands.choices(dice=[
  discord.app_commands.Choice(name="1,6", value="1,6"),
  discord.app_commands.Choice(name="1,10", value="1,10"),
])
async def commandRoll(ctx: discord.Interaction, dice: str):  # roll コマンドが実行されたら
  await roll.roll(ctx, dice)  # commands ファイルの roll.py にある roll を実行する


### fortune コマンド ###
@commandTree.command(
  name="fortune",
  description="イレイナさんが今日のあなたの運勢を占います。日替わりです。",
)
async def commandFortune(ctx: discord.Interaction):  # fortune コマンドが実行されたら
  await fortune.fortune(ctx)


### weather コマンド ###
@commandTree.command(name="weather", description="指定した県の天気が見れます")
@discord.app_commands.describe(city="天気を知りたい県の名前を選んでください")
@discord.app_commands.rename(city="県")
async def commandWeather(ctx: discord.Interaction,
                         city: str):  # weather コマンドが実行されたら
  await weather.weather(ctx,
                        city)  # commands ファイルの weather.py にある weather を実行する


### character コマンド ###
@commandTree.command(name="character", description="魔女の旅々の登場人物を紹介します")
@discord.app_commands.describe(name="誰を紹介してほしいか選んでください", char="誰が紹介するか選んでください")
@discord.app_commands.choices(char=[
  discord.app_commands.Choice(name="イレイナさん", value="イレイナ"),
  discord.app_commands.Choice(name="サヤさん", value="サヤ")
])
async def commandCharacter(ctx: discord.Interaction,
                           name: str,
                           char: str = "イレイナ"):  # character コマンドが実行されたら
  await character.character(
    ctx, name, char)  # commands ファイルの character.py にある character を実行する


### report コマンド ###
@commandTree.context_menu(name='report')
async def contextReport(interaction: discord.Interaction,
                        message: discord.Message):  # report コマンドが実行されたら
  await report.report(interaction,
                      message)  # commands ファイルの report.py にある report を実行する


### help コマンド ###
@commandTree.command(name="help", description="コマンドのヘルプを表示します")
@discord.app_commands.describe(name="詳細を表示したいコマンドの名前を書いてください")
async def commandHelp(ctx: discord.Interaction, name: str = None):
  await ctx.response.defer()
  await asyncio.sleep(4)
  await helpCommand.help(ctx, name)


### tts 系統のコマンド ###
@commandTree.command(name="join", description="ボイスチャンネルに接続します")
async def commandJoin(ctx: discord.Interaction):
  await ctx.response.defer()
  await asyncio.sleep(4)
  await tts.join(ctx)


@commandTree.command(name="leave", description="ボイスチャンネルから退出します")
async def commandLeave(ctx: discord.Interaction):
  await ctx.response.defer()
  await asyncio.sleep(4)
  await tts.leave(ctx)


@commandTree.command(name="dict", description="辞書を操作")
@discord.app_commands.describe(type="操作のモード",
                               word="操作したい言葉を指定します",
                               pseud="addの場合、読み仮名を指定します")
async def commandDict(ctx: discord.Interaction,
                      type: str,
                      word: str = None,
                      pseud: str = None):
  await ctx.response.defer()
  await asyncio.sleep(4)
  await tts.dict(ctx, type, word, pseud)


@commandTree.command(name="speaker", description="読み上げボットの話者を追加します")
@discord.app_commands.describe(speaker="話者を選んでください")
@discord.app_commands.choices(speaker=[
  discord.app_commands.Choice(name="ずんだもん", value=3),
  discord.app_commands.Choice(name="ずんだもん（あまあま）", value=1),
  discord.app_commands.Choice(name="ずんだもん（ツンツン）", value=7),
  discord.app_commands.Choice(name="ずんだもん（セクシー）", value=5),
  discord.app_commands.Choice(name="春日部つむぎ", value=8),
  discord.app_commands.Choice(name="四国めたん", value=2),
  discord.app_commands.Choice(name="四国めたん（あまあま）", value=0),
  discord.app_commands.Choice(name="四国めたん（ツンツン）", value=6),
  discord.app_commands.Choice(name="四国めたん（セクシー）", value=4),
  discord.app_commands.Choice(name="雨晴はう", value=10),
  discord.app_commands.Choice(name="波音リツ", value=9),
  discord.app_commands.Choice(name="剣崎雌雄", value=21)
])
async def commandSpeaker(ctx: discord.Interaction, speaker: int):
  await ctx.response.defer()
  await asyncio.sleep(4)
  await tts.speaker(ctx, speaker)


### メッセージイベント ###
@client.event  # 発言時に実行されるイベントハンドラを定義
async def on_message(message): # メッセージが送信されたときに
    await on_message_.on_message(message)


### メンバーイベント ###
@client.event
async def on_member_update(memberBefore: discord.Member, memberAfter: discord.Member):
    if memberBefore.nick != memberAfter.nick:
        await common.changedLog(memberBefore, memberAfter, 'ニックネーム')
    if memberBefore.roles != memberAfter.roles:
        await common.changedLog(memberBefore, memberAfter, '権限')
    if memberBefore.premium_since != memberAfter.premium_since:
        await common.changedLog(memberBefore, memberAfter, 'Nitro')


### サーバーの設定が変更されたとき ###
@client.event
async def on_guild_role_create(role):
  await common.changedLog(role, 'created', 'ロール')


@client.event
async def on_guild_role_delete(role):
  await common.changedLog(role, 'deleted', 'ロール')


@client.event
async def on_guild_role_update(before, after):
  await common.changedLog(before, after, 'ロール')


@client.event
async def on_guild_update(before, after):
  await common.changedLog(before, after, 'サーバー設定')


@client.event
async def on_guild_channel_create(channel):
  await common.changedLog(channel, 'created', 'チャンネル')


@client.event
async def on_guild_channel_delete(channel):
  await common.changedLog(channel, 'deleted', 'チャンネル')


@client.event
async def on_voice_state_update(member, before, after):
  await common.changedLog([member, before], after, 'ボイスチャンネル')


@client.event
async def on_stage_instance_create(stage_instance):
  await common.changedLog(stage_instance, 'created', 'ステージ')


@client.event
async def on_stage_instance_delete(stage_instance):
  await common.changedLog(stage_instance, 'deleted', 'ステージ')


@client.event
async def on_stage_instance_update(before, after):
  await common.changedLog(before, after, 'ステージ')


@client.event
async def on_scheduled_event_create(event):
  await common.changedLog(event, 'created', 'イベント')


@client.event
async def on_scheduled_event_delete(event):
  await common.changedLog(event, 'deleted', 'イベント')


@client.event
async def on_scheduled_event_update(before, after):
  await common.changedLog(before, after, 'イベント')


@tasks.loop(seconds=60)
async def loop():
  await task_loop.loop()


### Botの実行 ###
keep_alive()
client.run(token)
