import nextcord
from nextcord import SelectMenu, SelectOption, Button, ButtonStyle
from nextcord.ext import commands, Form
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




class userDropdown(nextcord.ui.Select):
    def __init__(self):
        options=[
                    
            nextcord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            nextcord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            nextcord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(userDropdown())




class mButtons(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @nextcord.ui.button(label='Kanal Edit')
    async def editCallback(self, button : nextcord.ui.Button, interaction):
         
        view = DropdownView()
        await interaction.response.send_message("select dis", view=view)




    @nextcord.ui.button(label='User kicken')
    async def kickCallback(self, button, interaction):
        view = DropdownView()
        await interaction.response.send_message("User asuwaehlen:", view=view)


@client.command()
async def olla(ctx):
    view = mButtons()
    await ctx.send("", view=mButtons())







client.run(TOKEN)