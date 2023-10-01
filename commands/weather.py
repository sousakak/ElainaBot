from discord import Interaction, ButtonStyle
import json, requests, datetime, asyncio
from config import *

citycodes = {
  "北海道": "016010",
  "青森": "020010",
  "岩手": "030010",
  "宮城": "040010",
  "秋田": "050010",
  "山形": "060010",
  "福島": "070010",
  "茨城": "080010",
  "栃木": "090010",
  "群馬": "100010",
  "埼玉": "110010",
  "熊谷": "110020",
  "秩父": "110030",
  "千葉": "120010",
  "東京": "130010",
  "大島": "130020",
  "八丈島": "130030",
  "父島": "130040",
  "神奈川": "140010",
  "新潟": "150010",
  "富山": "160010",
  "石川": "170010",
  "福井": "180010",
  "山梨": "190010",
  "長野": "200010",
  "岐阜": "210010",
  "静岡": "220010",
  "愛知": "230010",
  "三重": "240010",
  "滋賀": "250010",
  "京都": "260010",
  "大阪": "270000",
  "兵庫": "280010",
  "奈良": "290010",
  "和歌山": "300010",
  "鳥取": "310010",
  "島根": "320010",
  "岡山": "330010",
  "広島": "340010",
  "山口": "350010",
  "徳島": "360010",
  "香川": "370000",
  "愛媛": "380010",
  "高知": "390010",
  "佐賀": "410010",
  "長崎": "420010",
  "熊本": "430010",
  "大分": "440010",
  "宮崎": "450010",
  "鹿児島": "460010",
  "奄美": "460040",
  "奄美諸島": "460040",
  "沖縄": "471010",
}


async def weather(ctx, city):
  if city in citycodes.keys():
    citycode = citycodes[city]
    resp = requests.get(
      f"https://weather.tsukumijima.net/api/forecast/city/{citycode}")
    data = json.loads(resp.text)
    titleLink = data["link"]
    bodyText = data["description"]["bodyText"]
    descText = data["location"]["prefecture"] + 'の' + data["location"][
      "city"] + weatherDescText
    bodyEmbed = discord.Embed(title=city + 'の天気',
                              description=descText,
                              url=titleLink)
    bodyEmbed.set_author(
      name=client.get_user(botId).name + '#' +
      client.get_user(botId).discriminator,
      url=
      "https://discord.com/developers/applications/1073762890445766656/information",
      icon_url=client.get_user(botId).avatar)
    bodyEmbed.set_thumbnail(url=data["forecasts"][0]["image"]["url"])
    for forecast in data["forecasts"]:
      bodyEmbed.add_field(name=forecast["dateLabel"] + 'の天気',
                          value=forecast["telop"])
    bodyEmbed.set_footer(text=data["copyright"]["title"],
                         icon_url=data["copyright"]["image"]["url"])
    bodyEmbed.timestamp = datetime.datetime.now()
    async with ctx.channel.typing():

      class todayButton(discord.ui.Button):

        def __init__(self,
                     *,
                     style: ButtonStyle = ButtonStyle.secondary,
                     label: str = "今日の詳細"):
          super().__init__(style=style, label=label)

        async def callback(self, interaction: Interaction):
          todayDescText = data["location"]["city"] + 'の今日の天気です'
          todayEmbed = discord.Embed(title=city + 'の天気',
                                     description=todayDescText,
                                     url=titleLink)
          todayEmbed.set_author(
            name=client.get_user(botId).name + '#' +
            client.get_user(botId).discriminator,
            url=
            "https://discord.com/developers/applications/1073762890445766656/information",
            icon_url=client.get_user(botId).avatar)
          todayEmbed.set_thumbnail(url=data["forecasts"][0]["image"]["url"])
          todayEmbed.add_field(name='天気',
                               value=data["forecasts"][0]["detail"]["weather"])
          todayEmbed.add_field(name='風の強さ',
                               value=data["forecasts"][0]["detail"]["wind"])
          todayEmbed.add_field(name='波の高さ',
                               value=data["forecasts"][0]["detail"]["wave"])
          await interaction.response.send_message(embed=todayEmbed)

      class tomorrowButton(discord.ui.Button):

        def __init__(self,
                     *,
                     style: ButtonStyle = ButtonStyle.secondary,
                     label: str = "明日の詳細"):
          super().__init__(style=style, label=label)

        async def callback(self, interaction: Interaction):
          async with ctx.channel.typing():
            tomorrowDescText = data["location"]["city"] + 'の明日の天気です'
            tomorrowEmbed = discord.Embed(title=city + 'の天気',
                                          description=tomorrowDescText,
                                          url=titleLink)
            tomorrowEmbed.set_author(
              name=client.get_user(botId).name + '#' +
              client.get_user(botId).discriminator,
              url=
              "https://discord.com/developers/applications/1073762890445766656/information",
              icon_url=client.get_user(botId).avatar)
            tomorrowEmbed.set_thumbnail(
              url=data["forecasts"][1]["image"]["url"])
            tomorrowEmbed.add_field(
              name='天気', value=data["forecasts"][1]["detail"]["weather"])
            tomorrowEmbed.add_field(
              name='風の強さ', value=data["forecasts"][1]["detail"]["wind"])
            tomorrowEmbed.add_field(
              name='波の高さ', value=data["forecasts"][1]["detail"]["wave"])
            await interaction.response.send_message(embed=tomorrowEmbed)

      class dayAftTomorrowButton(discord.ui.Button):

        def __init__(self,
                     *,
                     style: ButtonStyle = ButtonStyle.secondary,
                     label: str = "明後日の詳細"):
          super().__init__(style=style, label=label)

        async def callback(self, interaction: Interaction):
          async with ctx.channel.typing():
            dayAftTomorrowDescText = data["location"]["city"] + 'の明後日の天気です'
            dayAftTomorrowEmbed = discord.Embed(
              title=city + 'の天気',
              description=dayAftTomorrowDescText,
              url=titleLink)
            dayAftTomorrowEmbed.set_author(
              name=client.get_user(botId).name + '#' +
              client.get_user(botId).discriminator,
              url=
              "https://discord.com/developers/applications/1073762890445766656/information",
              icon_url=client.get_user(botId).avatar)
            dayAftTomorrowEmbed.set_thumbnail(
              url=data["forecasts"][2]["image"]["url"])
            dayAftTomorrowEmbed.add_field(
              name='天気', value=data["forecasts"][2]["detail"]["weather"])
            dayAftTomorrowEmbed.add_field(
              name='風の強さ', value=data["forecasts"][2]["detail"]["wind"])
            dayAftTomorrowEmbed.add_field(
              name='波の高さ', value=data["forecasts"][2]["detail"]["wave"])
            await interaction.response.send_message(embed=dayAftTomorrowEmbed)

      view = discord.ui.View()
      view.add_item(todayButton(style=discord.ButtonStyle.primary))
      view.add_item(tomorrowButton(style=discord.ButtonStyle.primary))
      view.add_item(dayAftTomorrowButton(style=discord.ButtonStyle.primary))
      await ctx.response.defer()
      await asyncio.sleep(1)
      await ctx.followup.send(embed=bodyEmbed, view=view)

  else:
    async with ctx.channel.typing():
      await ctx.response.defer()
      await asyncio.sleep(1)
      await ctx.followup.send(weatherUnkownCity)
