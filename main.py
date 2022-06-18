import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import requests
import json

TOKEN = 'OTg3Nzk4NzUyNTYxNTk0Mzc4.GCT1zv.-UntIIlRFqtaL9xi8NdYZqCSHCTYBdoz9cLtb4'
client = commands.Bot(command_prefix='.')

@client.command(pass_context=True)
@client.event
async def on_ready():
    print("Bot Online")
    channel = client.get_channel(987799715523485740)
    channel = channel.voice_states

    for key in channel:
        guild = client.guilds[0]
        user = await client.fetch_user(key)
        channelName = str(user).split('#')
        channelName = channelName[0] + "'s Channel" 
        newChannel = await guild.create_voice_channel(channelName)

        Member = Member(user)
        await discord.Member.move_to(,channel=newChannel)

client.run(TOKEN)



