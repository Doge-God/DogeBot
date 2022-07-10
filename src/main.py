import discord
from discord.ext import commands
from functions import *
from data import botVoiceClients

#client = discord.Client()
client = commands.Bot(command_prefix='!')

with open("key.txt",'r') as keyFile:
    TOKEN = keyFile.readline()
keyFile.close()

@client.event 
async def on_ready():
    print('DogeBot logged in.')
    #await getSusBotChannel(client).send("DogeBot Online.")

@client.event
async def on_message(msg_read):
    if msg_read.author == client.user:
        return
    if msg_read.content.startswith('hello'):
        await msg_read.channel.send('Greetings.')
        return
    await client.process_commands(msg_read)
 
@client.command()
async def e(ctx):
    await ctx.send('***E***')

@client.command()
async def off(ctx):
    if ctx.author.name == "Doge_god" and ctx.author.discriminator == "2925":
        await ctx.send('DogeBot Offline.')
        #disconnect all voice clients from all servers
        for vc in client.voice_clients:
            await vc.disconnect()
        #log client out
        await client.logout()
        quit()

@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        newVcClient = await channel.connect()
        botVoiceClients[channel.id] = newVcClient
    else:
        await ctx.send("Join voice channel for voice channel commands.")

@client.command()
async def dc(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        if botVoiceClients[channel.id]:
            await botVoiceClients[channel.id].disconnect()
        else:
            ctx.send("DogeBot not in this voice channel.")
    else:
        await ctx.send("Join voice channel for voice channel commands.")


client.run(TOKEN)

