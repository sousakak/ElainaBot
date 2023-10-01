import discord
import asyncio
from config import *
import utility

async def errorHandler(error, args = None):
    match error:
        case 'notFoundGuild':
            return ttsNotFoundGuild
        case 'commanderNotVoiceCh':
            if args.guild.afk_channel is not None:
                await args.guild.afk_channel.connect(timeout=60.0, self_deaf=True)
            return ttsCommanderNotVoiceCh
        case 'alreadyConnected':
            return ttsAlreadyConnected
        case 'NotConnected':
            return ttsNotConnected
        case 'UnknownSpecifiedWord':
            return ttsUnknownSpecifiedWord
        case 'dictUnknownType':
            return ttsDictUnknownType
        case _:
            return ttsUnknownErrorMessage

### join 関数 ###
# ボイスチャンネルに参加する
async def join(ctx: discord.Interaction):
    if ctx.guild:
        if ctx.user.voice is None:
            errorMessage = await errorHandler('commanderNotVoiceCh', ctx)
            await ctx.send(errorMessage)
            return
        else:
            if ctx.guild.voice_client:
                if ctx.user.voice.channel == ctx.guild.voice_client.channel:
                    errorMessage = await errorHandler('alreadyConnected')
                    await ctx.followup.send(errorMessage)
                    return
                else:
                    await ctx.client.voice_clients[0].disconnect()
                    await asyncio.sleep(0.5)
                    await ctx.user.voice.channel.connect()
            else:
                await ctx.user.voice.channel.connect()
    else:
        errorMessage = await errorHandler('notFoundGuild')
        await ctx.followup.send(errorMessage)
        return
    await ctx.followup.send(ttsJoinedVC)

### leave 関数 ###
# ボイスチャンネルを退出する
async def leave(ctx: discord.Interaction):
    if ctx.guild:
        if ctx.guild.voice_client.channel is None:
            errorMessage = await errorHandler('NotConnected')
            await ctx.send(errorMessage)
            return
        else:
            await ctx.client.voice_clients[0].disconnect()
    await ctx.followup.send(ttsLeavedVC)

### dict 関数 ###
# 単語を読上げ辞書に追加する
async def dict(ctx: discord.Interaction, type, word, pseud):
    dictDatabase = utility.database("ttsDict", type="dict", guild=ctx.guild_id)
    # 追加モードの場合
    if type == 'add':
        # add pseud to dict
        dictDatabase.SetDictValue(word, pseud)
        await ctx.followup.send(ttsAddWordToDictDone)

    # 除去モードの場合
    if type == 'remove':
        # remove pseud from dict
        dictDatabase.DeleteDictData(word)

    # 表示モードの場合
    if type == 'view':
        # view pseud in dict
        embed = discord.Embed(title=ttsViewDictEmbedTitle, description=ttsViewDictEmbedDesc)
        embed.set_author(name=client.get_user(botId).name + '#' + client.get_user(botId).discriminator, url="https://discord.com/developers/applications/1073762890445766656/information", icon_url=client.get_user(botId).avatar)
        dataListOfGuild = dictDatabase.GetAllDict
        for oneAddedWord in dataListOfGuild:
            pairOfOneWord = oneAddedWord.split(':', 1)
            embed.add_field(name=pairOfOneWord[0], value=pairOfOneWord[1])
        await ctx.followup.send(embed=embed)

    # 不明なモードの時
    else:
        errorMessage = await errorHandler('dictUnknownType')
        await ctx.followup.send(errorMessage)
        return errorMessage

async def speaker(ctx: discord.Interaction, speaker: int):
    speakerData = utility.database("user", type="list", guild=ctx.user.id)
    speakerData.SetListValue(3, data=speaker)
    await ctx.channel.send(ttsSpeakerSetCorrectly)

### read 関数 ###
# 読み上げのユーザー設定を確認
def getConfigList(message: discord.Message):
    contentConfig = message.content
    userid = message.author.id
    speakerConfig = utility.database("user", type="list", guild=userid).GetListValue(3)
    if speakerConfig is None:
        speakerConfig = 8
    keyConfig = VOICEVOXkey
    speed = 0.7
    return contentConfig, speakerConfig, keyConfig, speed

# 読み上げをする関数の本体
async def read(message: discord.Message):
    if message.guild.voice_client.channel == message.author.voice.channel:
        content, speaker, key,speed = getConfigList(message)
        mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={content}&key={key}&speaker={speaker}&intonationScale=1&speed={speed}'
        source = discord.FFmpegOpusAudio(executable="ffmpeg.exe", source=mp3url)
        message.guild.voice_client.play(source)
    else:
        return