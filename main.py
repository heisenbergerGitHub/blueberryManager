import discord
from discord import SelectMenu, SelectOption, Button, ButtonStyle
from discord.ext import commands
from discord_ui import View

import os
import requests
import json
import sys
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

#Setup, on_ready-----------------------------------------------------------------------------------

@client.event
async def on_ready():
    print('Ready')



@client.command()  
@commands.has_role(role)
async def botSetup(ctx):
    guild = client.guilds[0]
    for channel in settings.channels:
        probeCategory = discord.utils.get(guild.categories, name=settings.channels[channel])
        if probeCategory == None:
            curCategory = await guild.create_category(settings.channels[channel], overwrites=None, reason=None)
        else:
            curCategory = guild.get_channel(settings.channels[channel])

        probeChannels = discord.utils.get(guild.channels, name=channel)
        if probeChannels == None:
            await guild.create_text_channel(channel, category = curCategory, overwrites=None, reason=None)
    ctx.reply('[+] Bot setup succseful')

# Commands, Checks, Events------------------------------------------------------------------------------------

@client.event
async def on_voice_state_update(member, before, after): 
    #Checking every listed channel in settings.listen_channels
    for listChannel in settings.listen_channels:
        # defining channel
        channel = client.get_channel(listChannel)
        channel = channel.voice_states
        # every key (user) will get a new channel in their ownership and name
        for key in channel:
            #Getting users id and name
            guild = client.guilds[0]
            user = await client.fetch_user(key)
            channelName = str(user).split('#')
               
             # Getting the category of the soon to be created channel  
            listCategory = settings.listen_channels[listChannel]
            listCategory = discord.utils.get(guild.categories, id=listCategory)

            # creating a new channel with users name and moving the user
            newChannel = await guild.create_voice_channel(f"{channelName[0]}'s Channel ", category = listCategory, overwrites=None, reason=None)
            member = await guild.fetch_member(key)
            await member.move_to(newChannel)
            chList[str(user)] = str(newChannel.id)
               # checking if channel is empty
        for channel in list(chList):
            channelIte = chList[channel]
            channelName = client.get_channel(int(channelIte))
            #deleting channel if its empty
            if channelName.voice_states == {}:
                await channelName.delete()
                del chList[channel]



#channel Edit -> soon to be replaced with Buttons
@client.command(pass_context=True)
async def channelName(ctx, message):
    author = ctx.author
    for channelAuth in list(chList):
        channelAuthName = int(chList[channelAuth])
        channelAuthName = client.get_channel(channelAuthName)
    
        if(str(author), author.voice.channel) == (channelAuth, channelAuthName):
            await author.voice.channel.edit(name= message)
            await ctx.reply('[+] Channel name has been changed to: ' + message, mention_author=False)


# Bot Shutdown (Imperator)
@client.command(pass_context=True)
@commands.has_role(role)
async def exit(ctx):
    await ctx.reply('[+] Shutting Down...')
    sys.exit()


#Lock command -> soon to be replaced with buttons
@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    author = ctx.author
    for channelAuth in list(chList):
        channelAuthName = int(chList[channelAuth])
        channelAuthName = client.get_channel(channelAuthName)
    
        if(str(author), author.voice.channel) == (channelAuth, channelAuthName):
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await author.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

#Buttons--------------------------------------------------------------------------------------------
# Buttons, wont work yet
@client.command()
async def buttonSetup(ctx):
    msgButtonsTest = await ctx.send('This is a test text', components=[[
        Button(label='Kanal bearbeiten', custom_id='editChannel'),
        Button(label = 'Kanal schliessen', custom_id='lockChannel'),
        Button(label = 'Kanal oeffnen', custom_id='unlockChannel'),
        Button(label = 'Einladung erstellen', custom_id='createInvite'),
        Button(label = 'User kicken', custom_id='kickUser'),
        Button(label = 'User blocken', custom_id='blockUser'),
        Button(label = 'User entblocken', custom_id='unblockUser')
    #Button(label = 'Channel Besitzer')
    #Callback functions will be here
    ]])
    def check_button(i: discord.Interaction, button):
       return i.author == ctx.author and i.message == msg_with_buttons

    interaction, button = await client.wait_for('button_click', check=check_button)

    embed = discord.Embed(title='You pressed an Button',
    description=f'You pressed a {button.custom_id} button.',
    color=discord.Color.random())
    await interaction.respond(embed=embed)
    
# not working callback



#Useless Shit--------------------------------------------------------------------------------

client.run(TOKEN)
