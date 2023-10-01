import discord
from config import *
from commands import make_it_a_quote, tts
import random

# reply 関数
async def reply(message):  # 呼ばれたときに返事する
    reply = f'{message.author.mention}' + supMessage  # 返信メッセージ
    await message.channel.send(reply)  # メッセージ送信

# react 関数
async def react(message: discord.Message):
    # メッセージ集
    replyMessage0 = ['サヤさんみたいなこと言わないでください', '何言ってるんですか？(ㅎ.ㅎ)']
    replyMessage1 = 'そう、私です。'
    replyMessage2 = ['おはようございます', 'ふあぁ、おはようございます', 'いい朝ですね…']
    replyMessage3 = 'いくら払ってくれるんですか？'
    replyMessage4 = '呼びましたか？'
    replyMessage5 = [
        'イタリア', 'フランス', 'チェコ', 'ドイツ', 'アメリカ', '日本', 'アゼルバイジャン', 'イングランド', '台湾',
        '中国', '韓国', 'イギリス', 'ロシア', 'アイルランド'
    ]
    replyMessage6 = ['何恥ずかしいことを言っているんですか、こわ', '急にどうしたんですか、変態ですか？', '`(イレイナはあなたをブロックしています)`', 'え、言うとでも思ったんですか？\n金貨1017枚払ってくれるなら考えますよ']
    replyMessage7 = ['それほどでもありますが...///', 'いざ面と向かって言われると恥ずかしいものですね…', 'もっとほめてもいいんですよ？', 'お世辞を言っても何も出てきませんよ？']
    replyMessage8 = '私のフィギュアですぎですよね…流石世界で一番の美少女'
    replyMessage9 = 'ｱｳﾞｨｱｳﾞｨ…( ˘ω˘ )'
    replyMessage10 = ['おやすみなさい', '今日も一日お疲れ様です', 'え、もう寝ちゃうんですか？', '私はもう少し本を読んでから寝ることにします']
    replyMessage11 = '2期は気長にゆっくり待ってください。旅はまだまだ終わりませんから。\nそれとも、「待て」もできないんですか…？'
    replyMessage12 = 'うっ…なんでしょう…嫌な記憶が…'
    replyMessage13 = ['はい？何かおっしゃいましたか？^^', 'その気なら……ぶっ飛ばしますよ', '淑女に向かって何を言っているんですか']
    replyMessage14 = '嘘つきというものはいつだって平然とした顔をしているものですよ'
    replyMessage15 = '魔女ならこれぐらい普通です'
    replyMessage16 = '気にしていませんよ。嘘ですけどね'
    replyMessage17 = '私もよく他の国で買ったものを道の高値で売り付けるという詐欺…ｺﾞﾎﾝｺﾞﾎﾝ商売をしたことがありますが、未だに目立って怒られたことはありませんからね。'
    replyMessage18 = '流石の私もお金がない人からはそんなに大量には絞り上げ…ｺﾞﾎﾝｺﾞﾎﾝ いただきませんよ？'
    replyMessage19 = ['なんだかお金の臭いがしますね…？', 'お金って言いました？言いましたよね？いくら、持ってるんですか？', 'なんだかこっちの方からお金の匂いがしてきますね…']
    replyMessage20 = '占いしてほしいんですか？よければ私がしますよ。こう見えて私の占い、よく当たるんです。え？いらない？まあまあ、そうおっしゃらず、さぞお疲れでしょうから、まあ、おかけください。'
    replyMessage21 = 'お疲れ様です。え？イレイナさんに癒してほしい、ですか？別にいいですよ。そこにかけてください。その代わり、お金は、ね？'

    if "イレイナさん大好き" in message.content or "イレイナ大好き" in message.content or "イレイナさんだいすき" in message.content:
        content = random.choice(replyMessage0)
        await message.channel.send(content)
    if message.content.endswith('誰？'):
        await message.channel.send(replyMessage1)
    if "おはよ" in message.content or "オハヨ" in message.content or "ｵﾊﾖ" in message.content:
        content = random.choice(replyMessage2)
        await message.channel.send(content)
    if message.content.endswith('してよ') or message.content.endswith('いてよ') or message.content.endswith('ってよ') or message.content.endswith('くれん？'):
        await message.channel.send(replyMessage3)
    if "1017" in message.content:
        await message.channel.send(replyMessage4)
    if message.content.startswith('イレイナ') and "国が好き？" in message.content:
        content = '一番は決められませんが、今は' + random.choice(replyMessage5) + 'に行ってみようかと思っています'
        await message.channel.send(content)
    if "イレイナ" in message.content and "スリーサイズ" in message.content and message.content.endswith('？'):
        content = random.choice(replyMessage6)
        await message.channel.send(content)
    if "イレイナさんかわいいイレイナさんかわいい" in message.content:
        await message.channel.send(replyMessage12)
    elif "イレイナさんかわいい" in message.content or "イレイナかわいい" in message.content or "イレイナさん可愛い" in message.content:
        content = random.choice(replyMessage7)
        await message.channel.send(content)
    if "フィギュア" in message.content and "イレイナ" in message.content:
        await message.channel.send(replyMessage8)
    if "ｱｳﾞｨｱｳﾞｨ" in message.content or "アヴィリア" in message.content:
        await message.channel.send(replyMessage9)
    if "おやすみ" in message.content:
        content = random.choice(replyMessage10)
        await message.channel.send(content)
    if "2期" in message.content and ("魔女の旅々" in message.content or "魔女旅" in message.content):
        await message.channel.send(replyMessage11)
    if "貧乳" in message.content:
        content = random.choice(replyMessage13)
        await message.channel.send(content)
    if "嘘つき" in message.content:
        await message.channel.send(replyMessage14)
    if "イレイナ" in message.content and (message.content.endswith("すご！") or "すごくね" in message.content):
        await message.channel.send(replyMessage15)
    if "ごめん" in message.content:
        await message.channel.send(replyMessage16)
    if "ばれなきゃ犯罪じゃ" in message.content:
        await message.channel.send(replyMessage17)
    if "金ない" in message.content or "金がない" in message.content:
        await message.channel.send(replyMessage18)
    elif "お金" in message.content:
        content = random.choice(replyMessage19)
        await message.channel.send(content)
    if "占い" in message.content:
        await message.channel.send(replyMessage20)
    if "疲れた" in message.content or "がこおわ" in message.content or "学校終" in message.content or "バイトおわ" in message.content or "バイト終" in message.content or "部活おわ" in message.content or "仕事おわ" in message.content:
        await message.channel.send(replyMessage21)
    if "暑" in message.content or "ｱﾂ" in message.content:
        content = random.choice(["最近本当に暑いですよねー…。全く<@562284321235402762>さんは何をしているんですか？", "", "", "", "", "", "", "", "", "", ""])
        await message.channel.send(content)
    if "fuck" in message.content or "f**k" in message.content or "ファッ" in message.content:
        await message.channel.send("言葉遣いが汚いですねーやだなーもー…ふぁっきゅーですよ")
    if "とーふ" in message.content and "変態" in message.content:
        await message.channel.send("私健全ですので変態とは何かわからず辞書で調べたのですが、どうやらとーふさんの様な人を言う言葉の様です。冗談はさておき… <@985877116581191731> さん、変態さんなんですね！")
    elif "とーふ" in message.content and "健全" in message.content:
        await message.channel.send("嘘はよくありませんよ？")
    if "さかな" in message.content and "食べ" in message.content:
        await message.channel.send("なんか美味しそうな話してますね…。私も混ぜてくれません？")
    if message.author.id == 831456419228155936 and "男の娘" in message.content:
        await message.channel.send("私も男の娘だったりして…？\n　　　　　　　　　　　　　　　冗談ですよ。")
    if message.author.id == 514565498311016459 and "( ˙꒳​˙  )" in message.content:
        await message.channel.send("( ˙꒳​˙  )")
    if message.author.id == 916963273612623883 and "久" in message.content:
        await message.channel.send("かーふさんお久しぶりです")
    if message.author.id == 965872176546848790 and "彼女" in message.content:
        await message.channel.send("彼女さん、いいですね。お幸せにしてください。||別に羨ましいとかじゃないので。||")
    if message.author.id == 960805585920602142 and "ぼっち" in message.content:
        await message.channel.send("ゆうーかさんのひとりさん愛もすごいですね…。||昔は私アイコンだったのに…||")
    if message.author.id == 1071725674915709019 and "笑" in message.content:
        content = random.choice(["", "", "", "", "", "", "", "", "私人生で笑いながら「笑」打ってる人見たことないんですよね…", "ずっきーさん「笑」大好きですね笑"])
        if content != "":
            await message.channel.send(content)
    if message.author.id == 562284321235402762 and ("神" in message.content or "上位存在" in message.content):
        await message.channel.send("あれ、食いしん坊で名の通っているこゆきさんじゃないですか！そんなに食べてると太りまｓ…えあなた神だったんですか！どうりで私の次くらいに可愛いと思いましたよ！失言？何言ってるんですかやだなも〜")
    if message.author.id == 759229682989662259 and "風俗" in message.content and "紹介" in message.content:
        await message.channel.send("ここなっつさん定期的に紹介おじさんになりますね...")


# メッセージ受信時に実行
async def on_message(message: discord.Message): # メッセージが送信されたときに
    if message.author.bot:
        return

    if client.user in message.mentions and client.user.mention in message.content:  # メンションをされたら
        if message.reference is not None:
            if message.guild.get_member(botId):
                listOfCommand = message.content.split(' ', 1)
                quoteCommand = listOfCommand[1:]
                quoteMessage = await message.channel.fetch_message(message.reference.message_id)
                if not quoteCommand:
                    await make_it_a_quote.makeItAQuote(None, quoteMessage, '')
                else:
                    await make_it_a_quote.makeItAQuote(None, quoteMessage, quoteCommand[0])
        else:
            await reply(message)  # 上で作った reply 関数の実行
            await tts.read(message)
    else:
        if message.guild.voice_client is not None and message.author.voice.channel is not None:
            await tts.read(message)
        await react(message)
