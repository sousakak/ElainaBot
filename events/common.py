from config import *
import datetime, re

async def changedLog(changedContent, logType, changedThing):
    match changedThing:
        case "ニックネーム":
            embed = discord.Embed(title="名前" + 'の変更', description=f'{changedContent.mention} が名前を `{logType.nick}` に変更しました')
            embed.set_footer(text='ID: ' + str(changedContent.id))
            embed.timestamp = datetime.datetime.now()
            await client.get_channel(logChannel).send(embed=embed)
        case "権限":
            diff = list(set(changedContent.roles) ^ set(logType.roles))
            beforeRole = afterRole = []
            b = a = ""
            for r in diff:
                if r in changedContent.roles:
                    beforeRole.append(r)
                    b += " ," + r.mention
                elif r in logType.roles:
                    afterRole.append(r)
                    a += " ," + r.mention
                else:
                    continue
            if len(beforeRole) != 0 and len(afterRole) != 0:
                embed = discord.Embed(title="ロール" + 'の変更', description=f'{logType.mention} が {b[2:]} を剥奪され、{a[2:]} を与えられました')
            elif len(beforeRole) != 0 and len(afterRole) == 0:
                embed = discord.Embed(title="ロール" + 'の変更', description=f'{logType.mention} が {b[2:]} を剥奪されました')
            elif len(beforeRole) == 0 and len(afterRole) != 0:
                embed = discord.Embed(title="ロール" + 'の変更', description=f'{logType.mention} が {a[2:]} を与えられました')
            embed.set_footer(text='ID: ' + str(logType.id))
            embed.timestamp = datetime.datetime.now()
            await client.get_channel(logChannel).send(embed=embed)
        case "Nitro":
            embed = discord.Embed(title="ニトロ", description=f'{changedContent.mention} がサーバーをブーストしました')
            embed.set_footer(text='ID: ' + str(changedContent.id))
            embed.timestamp = datetime.datetime.now()
            await client.get_channel(logChannel).send(embed=embed)
        case "ロール":
            if logType == 'created':
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.mention} が作成されました')
                embed.set_footer(text='ID: ' + str(changedContent.id))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
            elif logType == 'deleted':
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.name} が削除されました')
                embed.set_footer(text='ID: ' + str(changedContent.id))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
            else:
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.mention} が {logType.mention} に変更されました')
                embed.set_footer(text='ID: ' + str(changedContent.id))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
        case "サーバー設定":
            pass
        case "チャンネル":
            if logType == 'created':
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.mention}が作成されました')
                embed.set_footer(text='ID: ' + re.sub("https?://(www\.|)discord\.com/channels/\d+/", "", changedContent.jump_url))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
            elif logType == 'deleted':
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.mention}が削除されました')
                embed.set_footer(text='ID: ' + re.sub("https?://(www\.|)discord\.com/channels/\d+/", "", changedContent.jump_url))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
            else:
                embed = discord.Embed(title=changedThing + 'の変更', description=f'{changedContent.mention}が変更されました')
                embed.set_footer(text='ID: ' + re.sub("https?://(www\.|)discord\.com/channels/\d+/", "", changedContent.jump_url))
                embed.timestamp = datetime.datetime.now()
                await client.get_channel(logChannel).send(embed=embed)
        case "ボイスチャンネル":
            member = changedContent[0]
            before = changedContent[1]
            after = logType
            if (before.channel != after.channel):
                now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
                alert_channel = client.get_channel(logChannel)
            if before.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
                await alert_channel.send(msg)
            elif after.channel is None:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
                await alert_channel.send(msg)
            else:
                msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から {after.channel.name} に移動しました。'
                await alert_channel.send(msg)
        case "ステージ":
            pass
        case "イベント":
            pass
