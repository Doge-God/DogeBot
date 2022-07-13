from turtle import color
from helpers import *
from discord.ext import commands
from data import botVoiceClients
from data import songQueues
import random
import datetime
from google_images_search import GoogleImagesSearch

#client = discord.Client()
client = commands.Bot(command_prefix='!')

with open("key.txt") as keyFile:
    fileContents = open("key.txt").readlines()
    TOKEN = fileContents[0]
    GOOGLEAPIKEY = fileContents[1]
    GOOGLEENGINEID = fileContents[2]
keyFile.close()

searchPara = {
    'num': 10,
    'fileType': 'jpg|gif|png',
    'imgType': 'photo'
}

@client.event 
async def on_ready():
    print('DogeBot logged in.')
    botVoiceClients.clear()
    songQueues.clear()
    embedObj=discord.Embed(
        title="DogeBot Online.",
        color=discord.Color.green())
    await getSusBotChannel(client).send(embed = embedObj)

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
 
@client.event
async def on_command_error(ctx,error):
    if not isinstance(error, discord.ext.commands.CommandNotFound):
        return
    searchTerm = searchPara
    searchTerm['q'] = ctx.invoked_with
    gis = GoogleImagesSearch(GOOGLEAPIKEY, GOOGLEENGINEID)
    gis.search(search_params=searchPara)
    imgUrl = gis.results()[random.randint(0,9)].url
    embedMsg = discord.Embed(title="Here is {}".format(ctx.invoked_with), color=discord.Color.blurple())
    embedMsg.set_image(url=imgUrl)
    await ctx.send(embed=embedMsg)

@client.command()
async def e(ctx):
    embedObj=discord.Embed(
        title="E",
        color=discord.Color.blue())
    await ctx.send(embed = embedObj)

@client.command()
async def off(ctx):
    if ctx.author.name == "Doge_god" and ctx.author.discriminator == "2925":
        botVoiceClients.clear()
        embedObj=discord.Embed(
            title="DogeBot Offline.",
            color=discord.Color.red())
        await ctx.send(embed = embedObj)
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
            songQueues[ctx.guild.id] = []
            print("Joined, session ID: ")
            print(newVcClient.session_id)
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
            await getVcClient(ctx).disconnect()
            del botVoiceClients[ctx.guild.id]
            del songQueues[ctx.guild.id]

@client.command()
async def play(ctx,*phrases):
    match checkVcCommand(ctx):
        case "userNotInVc":
            await ctx.send("Join voice channel for voice channel commands.")
            return
        case "botNotInServer":
            await join(ctx)
        case "botNotInChannel":
            await join(ctx)
        case "sameServerAndChannel":
            pass
    searchTerm = ' '.join(phrases)
    searchResult = searchYoutube(searchTerm)
    embedObj=discord.Embed(title="__{}__".format(searchResult['title']),color=discord.Color.teal())
    embedObj.set_author(name="Added to queue: ")
    embedObj.add_field(name="Position",value="#{}".format(len(songQueues[ctx.guild.id])),inline=True)
    embedObj.add_field(name="Duration",value=str(datetime.timedelta(seconds=int(searchResult['duration']))),inline=True)
    embedObj.add_field(name="ETA"
        ,value=str(datetime.timedelta(seconds=getEta(len(songQueues[ctx.guild.id]),ctx.guild.id))),inline=True)
    await ctx.send(embed=embedObj)
    songQueues[ctx.guild.id].append(searchResult)
    tryBeginPlay(getVcClient(ctx))

@client.command(aliases=['q'])
async def queue(ctx):
    match checkVcCommand(ctx):
        case "userNotInVc":
            await ctx.send("Join voice channel for voice channel commands.")
            return
        case "botNotInServer":
            await ctx.send("DogeBot not in vc in this server.")
            return
        case "botNotInChannel":
            await ctx.send("DogeBot not in this channel.")
            return
        case "sameServerAndChannel":
            pass
    #if queue is empty simply print queue empty msg
    if len(songQueues[ctx.guild.id]) == 0:
        await ctx.send(embed=discord.Embed(title="Queue empty.",color=discord.Color.teal()))
        return

    embedObj=discord.Embed(title="Queue",color=discord.Color.teal())
    cnt = 0
    for song in songQueues[ctx.guild.id]:
        embedObj.add_field(name= ("Currently playing:" if cnt == 0 else "#{}".format(cnt)) 
            + "   ({})".format(str(datetime.timedelta(seconds=int(song['duration']))))
            ,value=song['title'],inline=False)
        cnt += 1
    await ctx.send(embed=embedObj)

@client.command()
async def skip(ctx,tgtTrack=None):
    match checkVcCommand(ctx):
            case "userNotInVc":
                await ctx.send("Join voice channel for voice channel commands.")
                return
            case "botNotInServer":
                await ctx.send("DogeBot not in vc in this server.")
                return
            case "botNotInChannel":
                await ctx.send("DogeBot not in this channel.")
                return
            case "sameServerAndChannel":
                pass
    if tgtTrack == None:
        if len(songQueues[ctx.guild.id]) < 1:
            await ctx.send(embed=discord.Embed(title="Queue empty.",color=discord.Color.teal()))
            return
        getVcClient(ctx).stop()
        await ctx.send(embed=discord.Embed(title="Skipped.",color=discord.Color.teal()))
        return
    trackNum = int(tgtTrack)

    #trying to skip last added song AND theres more than 1 song in the queue
    if trackNum == -1 and len(songQueues[ctx.guild.id]) > 1:
        embedObj=discord.Embed(title="Removed last song added:",color=discord.Color.teal())
        embedObj.add_field(name="#{}".format(len(songQueues[ctx.guild.id])-1)
            +"   ({})".format(str(datetime.timedelta(seconds=int(songQueues[ctx.guild.id][-1]['duration']))))
            ,value=songQueues[ctx.guild.id][-1]['title'],inline=False)
        await ctx.send(embed=embedObj)
        songQueues[ctx.guild.id].pop(-1)
    
    elif trackNum in range(1, len(songQueues[ctx.guild.id])):
        embedObj=discord.Embed(title="Removed:",color=discord.Color.teal())
        embedObj.add_field(name="#{}".format(trackNum)
            +"   ({})".format(str(datetime.timedelta(seconds=int(songQueues[ctx.guild.id][trackNum]['duration']))))
            ,value=songQueues[ctx.guild.id][trackNum]['title'],inline=False)
        await ctx.send(embed=embedObj)
        songQueues[ctx.guild.id].pop(trackNum)
    else:
        await ctx.send(embed=discord.Embed(title="Invalid skip location.",color=discord.Color.red()))

client.run(TOKEN)

