import discord
import gspread, os, pyglet
from google.oauth2.service_account import Credentials

### 変数の指定 (カスタムしたいときは基本ここいじればいい) ###
loginMessage = '魔女の旅々より来た、\n　通りを歩けば誰もが振り返るような、\n　　そんな美少女はいったい誰でしょう？\n　　　——そう、私です！'
supMessage = 'どうされましたか？'  # メンションされた際に返すメッセージ
gmMessageChannel = 985316722556936273  # 起動時にメッセージを送信するチャンネル
configChannel = 985311430481969203  # ユーザーがロール等の設定をできるチャンネル
logChannel = 985316722556936273  # Botがログを流すチャンネル
guildId = 985146054297141298
botId = 1073762890445766656  # BotのユーザーID
timeSignalMessage = 'あ、$1時ですよ'
helpCommandData = { # アルファベット順にソート
  'character': ('魔女の旅々のキャラクターの辞典です。nameに見たいキャラを入れると、情報が出ます', 'nameの他にcharというものがあり、これを変更すると口調が指定した人のものにかわります'),
  'confirm': ('新規ユーザーを認証します。member に承認するユーザーへのメンションを書いてください。', '承認したいユーザーを右クリックか長押しして、アプリからconfirmを選んでも使えます'),
  'dict': ('読み上げる際の辞書を登録します。wordに言葉を、pseudに読み仮名を振ってください', '辞書とは、登録された単語を登録された読み仮名で読み上げる、その単語のリストです'),
  'fortune': ('おみくじコマンドです。イレイナさんがあなたの運勢を占ってくれますよ', ''),
  'help': ('このコマンドです。様々なコマンドのヘルプを表示します', ''),
  'join': ('ボイスチャンネルに接続します', ''),
  'leave': ('ボイスチャンネルを退出します', ''),
  'speaker': ('読み上げボットに読んでもらうときの話者を設定します。', ''),
  'quote': ('日本人おなじみのMake it a Quoteです。コマンドでやるほか、メッセージ長押し/右クリックで出てくるアプリのconfirmも使えたり、ボットへのメンションを付けてメッセージに返信することでも利用できます', 'オプションは以下の通りです: ,**s**:影を付ける,**color**:モノクロからカラーになります。`color=`のあとにrainbowやcolorful、lightと指定することもできます,**font**:フォントを指定できます。現在指定できるフォントはこちらです：maka、kaisyo、gothic、hui、kyokasyo、yuji、mohitu'),
  'roll': ('さいころをふるコマンドです。1,10のように2つの数字をカンマで区切ってください。すると、1～10の中からランダムな数が選ばれます。', ''),
  'weather': ('天気予報を見ることができるコマンドです。県を指定してください', 'コマンドを実行すると今日から3日の天気と、3つのボタンが表示されます。ボタンを押すと詳細情報が見れます。'),
}
commandListTitle = 'Elainaのコマンドの一覧です'
commandListDesc = '/help の後にコマンドの名前を指定するとそのコマンドについてのより詳細な情報が得られます'
commandListFooter = 'ご要望等は管理者まで'
officialMemberRole = 985306418712289350  # 承認ユーザーに付けられるロール
roleOfAgreed = 1049292362494525510
roleOfUnagreed = 1052518774621872230
confirmedMessage = '新規ユーザーを認証しました！'  # confirmコマンドで実行が成功した際に表示されるメッセージ
confirmedDMContent = 'あなたは正式メンバーとして認証されました！\nhttps://discord.com/channels/' + str(
  guildId) + '/' + str(
    configChannel) + ' で様々なロールの設定ができますよ！'  # confirmコマンドが実行された際に対象者にdmで送るメッセージ
fortuneTelling = [
  ('大吉', 'お、大吉です…ってあれ？おかしいですね～、この占い大吉は出ないはｚ…ｹﾞﾌﾝｹﾞﾌﾝなんでもありませんよ？',
   0xff6347),
  ('中吉', '中吉じゃないですか！どれどれー、ふんふん、どうやら今日はボーナスがたくさん出るらしいですよ！よかったですね！ところで私も最近ボーナスが欲しいな～と思っていたところでしてね。占いのお金、いただけますか？ね？', 0xffd700),
  ('小吉',
   '小吉っていまいちぱっとしませんよね。そんな微妙な顔しないでくださいよ、私の占いなら小吉なんてめったに出ないんですよ？え？大吉はって？よくわかりませんね…',
   0xadff2f),
  ('末吉', 'ふつーです。あなたの昨日までの日々とおんなじで、なんもぱっとしないふつーの日々です。ふつーのあなたにはお似合いですよ。冗談です。まあまあ、私の美しい顔でも見て元気出してくださいよ',
   0x00ff7f),
  ('平',
   '平が出ましたね…。平ってなんですｋ…ｹﾞﾌﾝｹﾞﾌﾝなんでもないです。まあ読んで字のごとく、平らな日になるんじゃないのでしょうか。私は本でも読んで過ごしましょうか。',
   0x48d1cc), ('凶', '凶ですね…。ほうきに乗ってる途中に変な人に出会わないように気を付けてください。そうですね、具体的に言えば魔物を食べる人とか魔物の調理人とかナナマさんとかですかね。え？ほうきに乗れないって？それは失礼しました、魔法の使えない一般人さん（笑）', 0x87cefa),
  ('大凶', 'うわーすっごく運がいいんですねー！皮肉？なんのことでしょうか', 0x191970)
]
weatherUnkownCity = 'ちょっとそこは知らないですね'
weatherDescText = 'の天気ですよ。さて明日はどこへ行きましょうか…'
charNameNotFound = {
  'イレイナ': 'その子は知りませんね…お名前書き間違えてないですか…？',
  'サヤ': 'ボクはその人は知りませんね…書き間違えとかはしてないですか？'
}
nameOfWitchTitle = '魔女名'
calledNameTitle = '呼び名'
firstEntryTitle = '初出作'
charIntroNotFound = '誰かを紹介するキャラが見つかりませんね…'
defaultFont = './commands/Fonts/UDDIGIKYOKASHON-R.TTC'
listOfFont = {
  'maka': './commands/Fonts/851MKPOP.TTF',
  'kaisyo': './commands/Fonts/HGRSKP.TTF',
  'gothic': './commands/Fonts/HGRSMP.TTF',
  'hui': './commands/Fonts/HUIFONT29.TTF',
  'kyokasyo': './commands/Fonts/UDDIGIKYOKASHON-R.TTC',
  'yuji': './commands/Fonts/YUJISYUKU-REGULAR.TTF',
  'mohitu': './commands/Fonts/衡山毛筆フォント.TTF'
}
fontIsNotFound = '指定されたフォントが見つかりませんでした'
colorIsNotFound = '指定された色の設定が見つかりませんでした'
unknownQuoteCommand = '不明なコマンドが渡されました'
quoteErrorTitle = '以下のエラーが起きました'
ttsNotFoundGuild = 'サーバー以外でこのコマンドを実行することはできませんよ'
ttsJoinedVC = 'ボイスチャンネルに参加しました'
ttsCommanderNotVoiceCh = 'ボイスチャンネルに接続してから呼び出してくださいね'
ttsAlreadyConnected = 'もういますよ。いないと思ってたんですか、失礼ですね'
ttsNotConnected = 'ボイスチャンネルに接続していません。'
ttsLeavedVC = 'ボイスチャンネルから退出しました'
ttsAddWordToDictDone = '単語を辞書に登録しておきましたよ'
ttsViewDictEmbedTitle = '登録単語の一覧'
ttsViewDictEmbedDesc = 'このサーバーで辞書に登録されてる単語の一覧ですよ'
ttsUnknownSpecifiedWord = '指定された単語は見つかりませんね…'
ttsDictUnknownType = '登録されてない操作ですね…typeのとこ、見直してみてください'
ttsUnknownErrorMessage = '不明なエラーが起きましたね…コマンドミスとかないですか？わからなければ管理者に確認してください'
ttsSpeakerSetCorrectly = '読み上げるキャラクターが正常にセットされました'

### 基本の設定 ###
myGuild = discord.Object(id=guildId)

intents = discord.Intents.all()
intents.typing = False
client = discord.Client(intents=intents)
commandTree = discord.app_commands.CommandTree(client)

scope = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('client_secret.json',
                                                    scopes=scope)
gc = gspread.authorize(credentials)

token = os.getenv("DiscordBotToken")  # Botのトークン
fileOfIntro = os.getenv("fileOfIntro") # キャラ紹介のデータが入っているファイル
fileOfVar = os.getenv("fileOfVar")
VOICEVOXkey = os.getenv("VOICEVOXkey")