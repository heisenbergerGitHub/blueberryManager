import discord
from discord.ext import commands
import os
import requests
import json
import sys
import configparser
import settings



intents = discord.Intents.default()
intents.typing = False
intents.presences = False

tFile = open('TOKEN.txt', 'r')
TOKEN = tFile.read()
client = commands.Bot(command_prefix='.')
chList = {}
role = settings.setup['mainRole']
channellist = settings.listen_channels


@client.event
async def on_ready():
    print('Ready')



@client.event
async def on_voice_state_update(member, before, after): 
    for listChannel in settings.listen_channels:
        channel = client.get_channel(listChannel)
        channel = channel.voice_states

        for key in channel:
            guild = client.guilds[0]
            user = await client.fetch_user(key)
            channelName = str(user).split('#')

            listCategory = settings.listen_channels[listChannel]
            print(listCategory)
            print(type(listCategory))
            listCategory = discord.utils.get(guild.categories, id=listCategory)

            newChannel = await guild.create_voice_channel(f"{channelName[0]}'s Channel ", category = listCategory, overwrites=None, reason=None)
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
            await ctx.reply('[+] Channel name has been changed to: ' + message, mention_author=False)



@client.command()  
@commands.has_role(role)
async def botSetup(ctx):
    guild = client.guilds[0]
    for channel in settings.channels:
        probeCategory = discord.utils.get(guild.categories, name=settings.channels[channel])
        if probeCategory == None:
            curCategory = await guild.create_category(settings.channels[channel], overwrites=None, reason=None)
        
        probeChannels = discord.utils.get(guild.channels, name=channel)
        if probeChannels == None:
            await guild.create_text_channel(channel, category = curCategory, overwrites=None, reason=None)
            print(curCategory)
            print(type(curCategory))



@client.command(pass_context=True)
@commands.has_role(role)
async def exit(ctx):
    await ctx.reply('[+] Shutting Down...')
    sys.exit()



client.run(TOKEN)