import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import requests
import json
import sys

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

tFile = open('TOKEN.txt', 'r')
TOKEN = tFile.read()
client = commands.Bot(command_prefix='.')
chList = {}



@client.event
async def on_ready():
    print('Ready')



@client.command(pass_context=True)
@commands.has_role('IMPERATOR')
async def exit(ctx):
    await ctx.reply('Shutting Down...')
    sys.exit()


@client.event
async def on_voice_state_update(member, before, after): 
  
    channel = client.get_channel(988055091640684639)    #988055091640684639
    channel = channel.voice_states

    for key in channel:
        guild = client.guilds[0]
        user = await client.fetch_user(key)
        channelName = str(user).split('#') 
        newChannel = await guild.create_voice_channel(f"{channelName[0]}'s Channel ")
        member = await guild.fetch_member(key)
        await member.move_to(newChannel)
        chList[str(user)] = str(newChannel.id)

    for channel in list(chList):
        channelIte = chList[channel]
        channelName = client.get_channel(int(channelIte))

        if channelName.voice_states == {}:
            await channelName.delete()
            del chList[channel]
            



@client.command(pass_context=True)
async def changeName(ctx, message):
    author = ctx.author
    
    
    for channelAuth in list(chList):
        channelAuthName = int(chList[channelAuth])
        channelAuthName = client.get_channel(channelAuthName)
       

        if(str(author), author.voice.channel) == (channelAuth, channelAuthName):
            await author.voice.channel.edit(name= message)
            await ctx.reply('Channel name has been changed to: ' + message, mention_author=False)


client.run(TOKEN)


