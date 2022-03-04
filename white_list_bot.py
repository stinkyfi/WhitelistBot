import asyncio
from django.template.defaultfilters import upper
from pip._vendor import requests
import discord
from discord.ext import commands
import sqlite3 as sl
import re
import os
import mmap
# Custom Config
import config

# Enter a prefix you would like to use to interact with your bot
client = commands.Bot(command_prefix='$wl ')
# This is your discord bots token
bot_key = config.discord[0]['bot_key']
# Channels ID (int not strings)
whitelist_channel = config.discord['whitelist_channel']


@client.event
async def on_ready():
    print("gm")


@client.event
async def on_message(message):
    if message.author.bot:
        # Bot posted message
        return
    if message.channel.id != whitelist_channel:
        # Ignore other channels
        return
    print(message.author.id)
    id = str(message.author.id)
    username = f"<@{message.author.id}>"
    addr = message.content
    channel = client.get_channel(whitelist_channel)
    # match the regex statements for the input of the ID and the
    if re.match(r"^(0x)[0-9a-fA-F]{40}$", addr) and re.match(r"^[0-9]{18}$", id):
        file = "data.txt"

        # if the file has contents
        if os.path.getsize(file) > 0:
            with open(file, "r+") as f:
                for line in f.read().splitlines():
                    if id in line and addr in line:
                        data = "{} This entry already exist in shortlist.".format(username)
                        await channel.send(data)
                        await message.delete()
                        return
                    elif id in line:
                        await channel.send("{} Contact team to update your address".format(username))
                        await message.delete()
                        return
                    elif addr in line:
                        data = "{} This address is already reported by another user".format(username)
                        await channel.send(data)
                        await message.delete()
                        return
                data = "{} address accepted `{}`".format(username, addr[0:5] + "..." + addr[-4:])
                await channel.send(data)
                await message.delete()
                f.write("\n" + id + ", " + addr)
    else:
        data = "{} address format incorrect, it should be 0x`40 characters as a mix of 0-9 / a-f / A-F`".format(username)
        await channel.send(data)
        await message.delete()
        return


client.run(bot_key)
