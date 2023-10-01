import hashlib, datetime
from config import *

### fortune コマンド ###
async def fortune(ctx):
  async with ctx.channel.typing():
    today = str(datetime.date.today())
    hash_num = hashlib.sha1(bytes(str(ctx.user.id) + today, 'utf-8')).digest()[0]
    content = fortuneTelling[hash_num % len(fortuneTelling)]
    fortuneResult = discord.Embed(title=content[0], color=content[2], description=content[1])
    fortuneResult.set_author(name=client.get_user(botId).name + '#' + client.get_user(botId).discriminator, url="https://discord.com/developers/applications/1073762890445766656/information", icon_url=client.get_user(botId).avatar)
    fortuneResult.set_image(url="https://majotabi.jp/assets/story/12_1.jpg")
    fortuneResult.set_footer(
      text="この占いは日替わりです。同じ日に実行すると同じ結果が出ます",
      icon_url="https://cdn.discordapp.com/avatars/714693532777971722/b269c99d5c9aca3a2f2f75c43879774c.webp?size=128"
    )
    await ctx.response.send_message(embed=fortuneResult)