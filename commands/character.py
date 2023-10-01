import asyncio, datetime
from config import *

### character コマンド ###
async def character(ctx, name, char):
  async with ctx.channel.typing():
    workbook = gc.open_by_key(fileOfIntro)
    def conv_num_to_col(num): # 列も数字で返ってくるため、アルファベットに直す関数を定義しておく
      if num <= 26:
        return chr(64 + num)
      else:
        if num % 26 == 0:
          return conv_num_to_col(num//26-1) + 'Z'
        else:
          return conv_num_to_col(num//26) + chr(64+num%26)

    try: # char に指定された名前が無効だった場合の例外処理
      dataOfIntro = workbook.worksheet(char) # char に指定された名前のシートを開く
      dataOfName = dataOfIntro.col_values(1) # 登録されているキャラの名前の一覧を取得
      if name in dataOfName:
        rowOfName = dataOfIntro.find(name).row
        dataOfRow = dataOfIntro.row_values(rowOfName) # キャラの情報のリストを取得
        dataOfRow += ['' for i in range(5 - len(dataOfRow))] # リストの長さが足りず (一部の情報が欠けていて) エラーが起きてしまう場合の対処
        bodyEmbed = discord.Embed(title=name, description=dataOfRow[3])
        bodyEmbed.set_author(
          name=client.user,
          url="https://discord.com/developers/applications/1073762890445766656/information",
          icon_url=client.get_user(botId).avatar
        )
        bodyEmbed.add_field(
          name='魔女名',
          value=dataOfRow[1]
        )
        bodyEmbed.add_field(
          name='呼び名',
          value=dataOfRow[2]
        )
        bodyEmbed.add_field(
          name='初出作',
          value=dataOfRow[4]
        )
        bodyEmbed.set_footer(
          text=char + 'による' + name + 'の紹介です'
        )
        bodyEmbed.timestamp = datetime.datetime.now()
        await ctx.response.defer()
        await asyncio.sleep(1)
        await ctx.followup.send(embed=bodyEmbed)
      else:
        await ctx.response.defer()
        await asyncio.sleep(1)
        await ctx.followup.send(charNameNotFound[char])
    except gspread.WorksheetNotFound:
        await ctx.response.defer()
        await asyncio.sleep(1)
        await ctx.followup.send(charIntroNotFound)