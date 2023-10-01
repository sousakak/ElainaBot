from PIL import Image, ImageDraw, ImageFont, ImageOps
from config import *
import re, requests, io, textwrap

# 渡されたコマンドを読んで適切な変数を返す関数
async def commandRead(infoList, commandError):
    textColor = 255
    fontSize = 60
    colorMode = 'L'
    backgroundColor = 0
    shadow = False
    rainbowMode = False
    font = ImageFont.truetype(defaultFont, fontSize)
    if infoList[0]:
        for i, info in enumerate(infoList):
            info = info.replace(' ', '')
            if re.match('font=.+', info):
                fontName = info[5:]
                fontName = fontName.replace('sho', 'syo')
                if fontName in listOfFont:
                    font = ImageFont.truetype(listOfFont[fontName], 60)
                else:
                    commandError.append(fontIsNotFound)
            elif info == "c" or info == "color":
                colorMode = 'RGB'
                textColor = (255, 255, 255)
            elif re.search('color=.+', info):
                colorName = info[6:]
                if colorName == 'colorful':
                    colorMode = 'RGB'
                    textColor = (255, 255, 255)
                elif colorName == 'light':
                    textColor = 0
                    backgroundColor = 255
                elif colorName == 'rainbow':
                    colorMode = 'RGBA'
                    textColor = (255, 255, 255, 1)
                    backgroundColor = (0, 0, 0, 1)
                    rainbowMode = True
                elif colorName == 'grey' or colorName == 'black' or colorName == 'white':
                    pass
                else:
                    commandError.append(colorIsNotFound)
            elif info == "s" or info == "shadow":
                shadow = True
            else:
                commandError.append(unknownQuoteCommand)

    return textColor, fontSize, font, colorMode, textColor, backgroundColor, rainbowMode, shadow

# 渡された引数をもとにテキストを書く関数。モードによるテキスト描画の違いへの対応も関数内で行っています。
async def drawText(message, args):
    # モードによる変数の設定の変更
    draw = args['draw']
    textColor = args['textColor']
    fontColor = ''
    paint = draw
    shadowTextColor = 127
    if args['rainbowMode']:
        colorMode = 'L'
        textColor = 255
        rainbowOverlay = Image.new(colorMode, args['imageSize'], 0)
        paint = ImageDraw.Draw(rainbowOverlay)
    if args['shadow']:
        fontColor = shadowTextColor
    else:
        fontColor = textColor

    # テキストのフォントサイズと一行の文字数を設定する
    font = args['font']
    charInLine = 9
    quoteMessage = message.content
    wrap_list = textwrap.wrap(quoteMessage, charInLine)
    text = '\n'.join(wrap_list)
    boxCoord = (550, 50, 1100, 500) # (left, top, right, bottom)
    textBoxPos = ((boxCoord[2] - boxCoord[0]) / 2 + boxCoord[0], (boxCoord[3] - boxCoord[1]) / 2 + boxCoord[1])
    bbox = draw.multiline_textbbox(textBoxPos, text, font=font, align='center', anchor='mm')
    authorTextDistance = 100
    if bbox[3] < boxCoord[3]:
        paint.text(textBoxPos, text, fontColor, font=font, anchor='mm')
    else:
        authorTextDistance = 50
        while bbox[3] > boxCoord[3] and args['fontSize'] > 5:
            charInLine += 1
            wrap_list = textwrap.wrap(quoteMessage, charInLine)
            text = '\n'.join(wrap_list)
            while bbox[2] > boxCoord[2] and args['fontSize'] > 5:
                args['fontSize'] -= 2
                font = ImageFont.truetype(defaultFont, args['fontSize'])
                bbox = paint.multiline_textbbox(textBoxPos, text, font=font, align='center', anchor='mm')
            bbox = paint.multiline_textbbox(textBoxPos, text, font=font, align='center', anchor='mm')
        paint.text(textBoxPos, text, fontColor, font=font, anchor='mm')
    if args['shadow']:
        shadowTextPos = (textBoxPos[0] - 3, textBoxPos[1] - 3)
        paint.text(shadowTextPos, text, textColor, font=font, anchor='mm')
    rainbow = Image.open('commands/rainbow.png')
    if args['rainbowMode']:
        rainbow = rainbow.convert("RGBA")
        rainbow.putalpha(rainbowOverlay)
        args['quoteBasePicture'].paste(rainbow)
        textColor = (0, 0, 0, 1)
    else:
        draw = paint

    return draw, textColor, bbox, textBoxPos, boxCoord, authorTextDistance

# コマンドエラーが起きている場合に起きているエラーメッセージを含むembedを返します
async def commandErrorChecker(commandError):
    commandErrorMessage = ''
    commandErrorEmbed = ''
    if commandError:
        commandErrorMessage = '```http\n ERROR : '
        commandErrorMessage += '\n ERROR : '.join(commandError)
        commandErrorMessage += '```'
        commandErrorEmbed = discord.Embed(title=quoteErrorTitle, description=commandErrorMessage)
    return commandErrorEmbed

### makeItAQuote コマンド ###
async def makeItAQuote(ctx, message: discord.Message, command):
    typeChannel = ctx.channel if ctx is not None else message.channel
    async with typeChannel.typing():
        infoList = command.split(',')
        commandError = []
        # コマンドに渡された値を読む
        textColor, fontSize, font, colorMode, textColor, backgroundColor, rainbowMode, shadow = await commandRead(infoList, commandError)
        # アイコンの加工
        imageSize = (1200, 630)
        iconUrl = message.author.display_avatar.url
        iconSize = (imageSize[1], imageSize[1])
        prevIcon = Image.open(io.BytesIO(requests.get(iconUrl).content)).resize(iconSize)
        prevIcon = ImageOps.pad(prevIcon, imageSize, centering=(0, 0))
        # 画像のベースの作成
        quoteBasePicture = Image.new(colorMode, imageSize, backgroundColor)
        draw = ImageDraw.Draw(quoteBasePicture)
        # 本文を描く
        drawTextargs = {'draw': draw, 'textColor': textColor, 'rainbowMode': rainbowMode, 'imageSize': imageSize, 'shadow': shadow, 'quoteBasePicture': quoteBasePicture, 'font': font, 'fontSize': fontSize}
        draw, textColor, bbox, textBoxPos, boxCoord, authorTextDistance = await drawText(message, drawTextargs)
        # 発言者を書く
        authorTextPos = bbox[3]
        quoteAuthor = [message.author.display_name, ' (' + message.author.name + '#' + message.author.discriminator + ')']
        authorText = ' - ' + quoteAuthor[0] + quoteAuthor[1]
        authorFontSize = 30
        authorBbox = draw.multiline_textbbox((textBoxPos[0], authorTextPos + 25), authorText, font=ImageFont.truetype(defaultFont, authorFontSize), align='center', anchor='mm')
        if authorBbox[2] < boxCoord[2]:
            authorText = ' - ' + quoteAuthor[0] + quoteAuthor[1]
        else:
            authorText = ' - ' + quoteAuthor[0] + '\n   ' + quoteAuthor[1]
        draw.text((textBoxPos[0], authorTextPos + authorTextDistance), authorText, textColor, font=ImageFont.truetype(defaultFont, authorFontSize), anchor='mm')
        mask = Image.open('commands/mask.png')
        mask = mask.convert('L')
        quoteBasePicture.paste(prevIcon, (0, 0), mask)
        # ファイルを保存
        fileio = io.BytesIO()
        quoteBasePicture.save(fileio, format="png")
        fileio.seek(0)
        fileDiscord = discord.File(fileio,"file.png")
        # エラーをチェック
        commandErrorEmbed = await commandErrorChecker(commandError)
        # 送信
        if commandErrorEmbed:
            await typeChannel.send(embed=commandErrorEmbed, file=fileDiscord)
        else:
            await typeChannel.send(file=fileDiscord)
