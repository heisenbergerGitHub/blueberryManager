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

intents = nextcord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=".", intents=intents)

chList = {}
role = settings.setup['mainRole']
channellist = settings.listen_channels

#Setup, on_ready-----------------------------------------------------------------------------------

@client.event
async def on_ready():
    print('--------------------------------')
    print(f'[+] blueberryManager connected as {client.user} to ')
    print('--------------------------------')

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





#Editing Channel---------------------------------------------------------------------------------------


class channelEdit(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Kanaleinstellungen",
            timeout=60,
        )

        self.name = nextcord.ui.TextInput(
            label='Neuer Kanalname',
        )
        self.add_item(self.name)

        self.size = nextcord.ui.TextInput(
            label='Neue Kanalgroesse',
        )
        self.add_item(self.size)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        author = interaction.user
        for channelAuth in list(chList):
            channelAuthName = int(chList[channelAuth])
            channelAuthName = client.get_channel(channelAuthName)    
            if(str(author), author.voice.channel) == (channelAuth, channelAuthName):
                await author.voice.channel.edit(name= self.name.value, user_limit= self.size.value)
                await interaction.response.send_message(f'[+] Kanalname wurde zu {self.name.value} geaendert\n[+] Kanalgroesse wurde auf {self.size.value} User limitiert')
            else:
                await interaction.response.send_message('[+] Du musst besitzer dieses Kanals sein um diesen editieren zu koennen')


#Kick the user-----------------------------------------------------------------------------------------
class userKickDropdown(nextcord.ui.Select):
    def __init__(self, interaction : nextcord.Interaction):
        channel = interaction.voice.channel
        userDropdownList = []
        for user in channel.voice_states:
            listMember= client.get_user(user)
            userDropdownList.append(nextcord.SelectOption(label= str(listMember),emoji="👾"))
        super().__init__(placeholder="Userliste",max_values=1,min_values=1,options=userDropdownList)
        
    async def callback(self, interaction: nextcord.Interaction):
        guild = client.guilds[0]  
        await interaction.response.send_message(f'[+] User {self.values[0]} wurde erfolgreich gekickt')
        memberToKick = str(self.values[0])
        memberToKick =  guild.get_member_named(str(memberToKick))
        await memberToKick.move_to(None)

class kickDropdownView(nextcord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.add_item(userKickDropdown(user))



#Buttonsstuf------------------------------------------------------------------------------------------
class mButtons(nextcord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @nextcord.ui.button(label='Kanal Edit', emoji = '⚙️')
    async def editCallback(self, button : nextcord.ui.Button, interaction):
        modal = channelEdit()
        await interaction.response.send_modal(modal)
    
    @nextcord.ui.button(label='Kanal oeffnen')
    async def openCallback(self, button : nextcord.ui.Button, interaction):
        pass

    @nextcord.ui.button(label='Kanal schliessen')
    async def closeCallback(self, button : nextcord.ui.Button, interaction):
        pass    

    @nextcord.ui.button(label='User kicken')
    async def kickCallback(self, button, interaction):
        view = kickDropdownView(interaction.user)
        await interaction.response.send_message("User asuwaehlen:", view=view)

@client.command()
async def c(ctx):
    view = mButtons()
    await ctx.send("", view=mButtons())







client.run(TOKEN)