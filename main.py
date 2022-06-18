import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import requests
import json

TOKEN = ''
client = commands.Bot(command_prefix='.')

@client.command(pass_context=True)
@client.event
async def on_ready():
    print("Bot Online")
    channel = client.get_channel(987799715523485740)
    channel = channel.voice_states

    for key in channel:
        guild = client.guilds[0]
        member = await client.fetch_user(key)
        channelName = str(member).split('#')
        channelName = channelName[0] + "'s Channel" 
        newChannel = await guild.create_voice_channel(channelName)


client.run(TOKEN)



