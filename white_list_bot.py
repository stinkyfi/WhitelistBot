import asyncio
from django.template.defaultfilters import upper
from pip._vendor import requests
import discord
from discord import Color
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
bot_key = config.discord['bot_key']
# Channels ID (int not strings)
whitelist_channel = config.discord['whitelist_channel']


@client.event
async def on_ready():
    print("gm")
    # channel = client.get_channel(whitelist_channel)
    # await channel.send(":information_source: Bot Update v1.1.0 (Updated admin features) :hammer_pick:")


@client.event
async def on_message(message):
    if message.author.bot:
        print("IT'S THE BOT")
        return
    if '$wl' in message.content:
        await client.process_commands(message)
    if message.channel.id != whitelist_channel:
        print("Wrong Channel")
        return
    print(message.author.id)
    id = str(message.author.id)
    username = f"<@{message.author.id}>"
    addr = message.content
    channel = client.get_channel(whitelist_channel)
    # match the regex statements for the input of the ID and the
    if re.match(r"^(0x)[0-9a-fA-F]{40}$", addr) and re.match(r"^[0-9]{17,18}$", id):
        file = config.discord['file_path']

        # if the file has contents
        if os.path.getsize(file) > 0:
            with open(file, "r+") as f:
                for line in f.read().splitlines():
                    print("Id we looking for:" + line)
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
                embed = discord.Embed(title="Address Accepted", url='', color=Color.blue())                        
                embed.set_thumbnail(url="https://i.ibb.co/tX7TSXk/BUBONIC-BASTARDS.png")                    
                data = "{} address accepted `{}`".format(username, addr[0:5] + "..." + addr[-4:])
                embed.add_field(name="Message: ", value=data, inline=False)   
                await ctx.send(embed=embed)
                await message.delete()
                f.write("\n" + id + ", " + addr)
    else:
        data = '{} address format incorrect, it should be 0x`40 characters ' \
                'as a mix of 0-9 / a-f / A-F`'.format(username)
        await channel.send(data)
        await message.delete()
        return


@client.command()
async def stats(ctx):
    i = 0
    channel = client.get_channel(927299713953325087)
    with open(config.discord['file_path'], "r") as f:
        for line in f.readlines():
            i = i + 1
    f.close()
    await channel.send('There are ' + str(i) + ' entries')


@client.command(pass_context=True)
async def download(ctx):
    channel = client.get_channel(927299713953325087)
    await channel.send('Here is your File:', file=discord.File(config.discord['file_path']))


client.run(bot_key)
