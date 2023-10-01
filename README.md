# Discord Multifunctional Bot : Elaina
This is a Discord Bot based on the concept of Elaina, which is protagonist in an anime "The Journey of Elaina".
This Bot was developed as a dedicated bot for the Discord Server "魔女旅界隈変態部" (en: The Witches' Journey Fans' *HENTAI* Club). And for now, supporting only Japanese.
***
The developer of this bot is new to programming and the code is probably very confusing. If you have any very serious concerns, please feel free to contact me.

## FEATURES
- Weather Forecaster
    - `/weather`
    - Displays weather forecast for the next 3 days. Press the button to display detailed information
    - **Note**: Currently, this feature is only available in Japan
- Confirm User
    - `/confirm`
    - Confirm a new user.
- Roll dice
    - `/roll`
- Fortune
    - `/fortune`
    - Predict your fortune today. It is a form of Japanese Omikuji (おみくじ).
- Character
    - `/character`
    - A dictionary about characters in The Journey of Elaina. This is not a complete list, although it includes information on all works, including animated and comicalized versions.
- Tts
    - `/join`
    - `/leave`
    - `/dict`
    - `/speaker`
    - Under development
- Werewolf Game
    - *Comming Soon*
- Reply and Reaction
    - Responds to specific messages. As much as possible, I try to reflect the personality of the original Elaina. I would really like to use AI to talk... I don't know how to :(
- Log Messages
    - Send log messages like member joined/left voice channel. 

## REQUIRES
If you want to run this program in your environment, you will need to load the module written here. If you are using pip, the process is completed with the following line: 
```
$ pip install -r requirements.txt
```
Since module 'cshogi' only supported up to python 3.10 at the time I was developing this, the venv module is used. Instructions for installing this module are below. For more detailed information, please refer to [the official documentation](https://docs.python.org/ja/3/library/venv.html).

- Python
    - discord.py
    - discord.ext.py
    - gspread
    - google.oauth2.service_account
    - pillow
    - cshogi
    - dotenv
    - numpy
    ***
    - os
    - os.path
    - asyncio
    - datetime
    - random
    - typing
    - hashlib
    - re
    - requests
    - io
    - textwrap
    - json
    - threading
    - collections
    - time
    - doctest
- ffmpeg

### venv
This folder in github does not contain any files related to the venv module. If you are using 3.11 or later versions of Python, the cshogi module will not work properly (at least at the time of my development).
- If a cshogi module exists for the version of Python you are using, please ignore what is written here. For the current released version of cshogi, see [here](https://pypi.org/project/cshogi/#files).
- If you do not need the Shogi function, you can skip this step by cutting out the relevant parts from index.py.

Once you have installed a version of Python that is supported by cshogi, go to that Python directory at the command prompt. Then execute the following command there: 
```
python -m venv <path>
```
Specify the location of the Bot program folder in <path>.

If this is successful, you should have several folders in your program's folder, including Scripts.
Note: If you install another version of Python, the modules you previously installed will not be reflected in that version.

***

Before launching the bot, open the program's file at the command prompt and then execute the following: 
```batch
# Windows
Scripts\activate.bat

# Windows PowerShell
Scripts\Activate.ps1

# POSIX PowerShell
bin/Activate.ps1
```
The bot must be run from a command prompt, but some editors, such as VSCode, support venv.

## OUTLOOK
TODO: 
- Support English
- Add operation information
- Further functionality to `/quote`
- Make the code more readable
- Responding to 404 errors for Interaction
- Faster response time for some commands