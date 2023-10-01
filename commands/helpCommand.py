import discord
from config import *
import datetime

async def help(ctx, command):
    commandList = commandTree.get_commands(type=discord.AppCommandType.chat_input)
    if command is None:
        embed = discord.Embed(title=commandListTitle, description=commandListDesc)
        embed.set_footer(text=commandListFooter)
        embed.timestamp = datetime.datetime.now()
        for commandObject in commandList:
            embed.add_field(name=commandObject.name, value=commandObject.description)
    else:
        if command == "quote":
            detailInfos = helpCommandData[command][1].split(',')
            embedDescText = helpCommandData[command][0]
            embedDescText += '\n' + detailInfos[0]
            footerText = commandListFooter
        else:
            footerText = helpCommandData[command][1]
            embedDescText = helpCommandData[command][0]
        embed = discord.Embed(title="/" + command, description=embedDescText)
        embed.set_author(name=client.get_user(botId).name + '#' + client.get_user(botId).discriminator, url="https://discord.com/developers/applications/1073762890445766656/information", icon_url=client.get_user(botId).avatar)
        if command == "quote":
            detailIndividualInfoDict = {}
            for detailIndividualInfo in detailInfos[1:]:
                detailIndividualInfoDict[detailIndividualInfo.split(':')[0]] = detailIndividualInfo.split(':')[1]
            print(detailIndividualInfoDict)
            for detailInfoTitle, detailInfoContent in detailIndividualInfoDict.items():
                embed.add_field(name=detailInfoTitle, value=detailInfoContent)
        embed.set_footer(text=footerText)
        embed.timestamp = datetime.datetime.now()
    await ctx.followup.send(embed=embed)