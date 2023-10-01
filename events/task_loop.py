from config import *
import utility
import discord
import datetime

async def loop():
    now = datetime.datetime.now()
    if now.minute == 0:
        client.get_channel(logChannel).send(utility.replace(timeSignalMessage, now.hour))