from config import *
import datetime

async def confirm(ctx, member):
  await ctx.response.send_message(confirmedMessage, delete_after=10.0)
  roleToAdd = ctx.guild.get_role(officialMemberRole)
  roleToRemove1 = ctx.guild.get_role(roleOfAgreed)
  roleToRemove2 = ctx.guild.get_role(roleOfUnagreed)
  await member.add_roles(roleToAdd)
  await member.remove_roles(roleToRemove1)
  await member.remove_roles(roleToRemove2)
  async with ctx.channel.typing():
    confirmedLogDescription = member.mention + "が認証されました"
  confirmedLog = discord.Embed(title="", color=11111111, description=confirmedLogDescription)
  confirmedLog.set_author(name=member.name, icon_url=member.avatar.url)
  confirmedLog.set_footer(text="ID:" + str(member.id) + "・" + str(datetime.datetime.now()))
  confirmedDM = ctx.guild.name + "において、" + confirmedDMContent
  await client.get_channel(logChannel).send(content=None, embed=confirmedLog)
  await member.send(content=confirmedDM)