import nextcord
from nextcord import SelectMenu, SelectOption, Button, ButtonStyle
from nextcord.ext import commands
from nextcord.ui import  View, Select

import os
import requests
import json
import sys
import settings


tFile = open('TOKEN.txt', 'r')
TOKEN = tFile.read()

client = commands.Bot(command_prefix=".", intents= nextcord.Intents.all())
chList = {}
role = settings.setup['mainRole']
channellist = settings.listen_channels

#Setup, on_ready-----------------------------------------------------------------------------------

@client.event
async def on_ready():
    print('--------------------------------')
    print(f'[+] blueberryManager connected as {client.user} to ')
    print('--------------------------------')

@client.command(pass_context=True)
@commands.has_role(role)
async def botSetup(ctx):
    guild = client.guilds[0]
    for channel in settings.channels:
        probeCategory = nextcord.utils.get(guild.categories, name=settings.channels[channel])
        if probeCategory == None:
            curCategory = await guild.create_category(settings.channels[channel], reason=None)
        else:
            curCategory = guild.get_channel(settings.channels[channel])

        probeChannels = nextcord.utils.get(guild.channels, name=channel)
        if probeChannels == None:
            await guild.create_text_channel(channel, category = curCategory, reason=None)
    ctx.reply('[+] Bot setup succseful')

# Commands, Checks, Events------------------------------------------------------------------------------------

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
            listCategory = nextcord.utils.get(guild.categories, id=listCategory)
            newChannel = await guild.create_voice_channel(f"{channelName[0]}'s Channel ", category = listCategory, reason=None)
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
@commands.has_role(role)
async def exit(ctx):
    await ctx.reply('[+] Shutting Down...')
    sys.exit()


#Buttons--------------------------------------------------------------------------------------------
class mButtons(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @nextcord.ui.button(label='Kanal Edit')
    async def editCallback(self, button : nextcord.ui.Button, interaction):
        author = interaction.user
        for channelAuth in list(chList):
            channelAuthName = int(chList[channelAuth])
            channelAuthName = client.get_channel(channelAuthName)    
            if(str(author), author.voice.channel) == (channelAuth, channelAuthName):
                await author.voice.channel.edit(name= message)
                await ctx.reply('[+] Channel name has been changed to: ' + message, mention_author=False)
        await interaction.response.send_message("Dipshit")



    @nextcord.ui.button(label='Kanal oeffnen')
    async def openCallback(self, button, interaction):
        await interaction.response
    
    @nextcord.ui.button(label='Kanal schliessen')
    async def closeCallback(self, button, interaction):
        button.label = 'cytschka'

    @nextcord.ui.button(label='User kicken')
    async def kickCallback(self, button, interaction):
        select = Select(
        placeholder = "None",
        options=[
            nextcord.SelectOption(
                label = '1',
                description = 'dis description',
                default= True
            ),
            nextcord.SelectOption(
                label = '2',
                description = 'dis description',
                default= True
            ),
            nextcord.SelectOption(
                label = '3',
                description = 'dis description',
                default= True
            )])
        view1 = self
        view1.add_item(select)
        await interaction.response.send_message("select dis", view=view1)

    @nextcord.ui.button(label='User Blocken')
    async def blockCallback(self, button, interaction):
        button.label = 'cytschka'

@client.command()
async def olla(ctx):
    view = mButtons()
    await ctx.send("tylko", view=view)

client.run(TOKEN)