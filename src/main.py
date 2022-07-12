from helpers import *
from discord.ext import commands
from data import botVoiceClients

#client = discord.Client()
client = commands.Bot(command_prefix='!')

with open("key.txt",'r') as keyFile:
    TOKEN = keyFile.readline()
keyFile.close()



@client.event 
async def on_ready():
    print('DogeBot logged in.')
    botVoiceClients.clear()
    await getSusBotChannel(client).send("DogeBot Online.")

@client.event
async def on_message(msg_read):
    if msg_read.author == client.user:
        return
    if msg_read.content.startswith('hello'):
        await msg_read.channel.send('Greetings.')
        return
    if ":BatChest:" in msg_read.content:
        await msg_read.channel.send(':BatChest:')
        return
    await client.process_commands(msg_read)
 
@client.command()
async def e(ctx):
    embedObj=discord.Embed(
        title="E",
        description="e",
        color=discord.Color.blue())
    await ctx.send(embed = embedObj)

@client.command()
async def off(ctx):
    if ctx.author.name == "Doge_god" and ctx.author.discriminator == "2925":
        await ctx.send('DogeBot Offline.')
        #disconnect all voice clients from all servers
        for vc in client.voice_clients:
            await vc.disconnect()
        #log client out
        await client.close()
        quit()

@client.command()
async def join(ctx):
    match checkVcCommand(ctx):
        case "userNotInVc":
            await ctx.send("Join voice channel for voice channel commands.")
        case "botNotInServer":
            newVcClient = await ctx.message.author.voice.channel.connect()
            botVoiceClients[ctx.guild.id] = newVcClient
        case "botNotInChannel":
            await botVoiceClients[ctx.guild.id].move_to(ctx.author.voice.channel)

@client.command()
async def dc(ctx):
    match checkVcCommand(ctx):
        case "userNotInVc":
            await ctx.send("Join voice channel for voice channel commands.")
        case "botNotInServer":
            await ctx.send("DogeBot not in vc in this server.")
        case "botNotInChannel":
            await ctx.send("DogeBot not in this channel.")
        case "sameServerAndChannel":
            await getVcCommandVcClient(ctx).disconnect()
            del botVoiceClients[ctx.guild.id]

@client.command()
async def play(ctx,phrase):
    await playFromUrl(searchYoutube(phrase)['source'], getVcCommandVcClient(ctx))


client.run(TOKEN)

