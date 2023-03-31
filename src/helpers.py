from data import botVoiceClients
from data import ytdl_format_options
from data import ffmpeg_options
from data import songQueues
import youtube_dl
import yt_dlp
import asyncio
import discord
from youtube_dl import YoutubeDL

#get all channels from Sus Amongus
def getSusChannels (client):
    susChannels = []
    for guild in client.guilds:
        for channel in guild.channels:
            if guild.id == 845236320489832479:
                susChannels.append(channel)
    if len(susChannels) == 0:
        raise RuntimeError("No channels from Sus Amongus found")
    else:
        return susChannels

#return bot channel from Sus Amongus
def getSusBotChannel(client):
    for channel in getSusChannels(client):
        if channel.name == "bot":
            return channel
    raise RuntimeError("No channel from Sus Amongus called bot")

#return voice client from the vc command
def getVcClient(ctx):
    return botVoiceClients[ctx.guild.id]

#return string: userNotInVc, botNotInServer, botNotInChannel, sameServerAndChannel
def checkVcCommand(ctx):
    #check if user is in vc
    if not ctx.author.voice:
        return "userNotInVc"
    #check if bot is in vc in current server
    try:
         botVoiceClients[ctx.guild.id]
    #bot is not in vc of this server
    except KeyError:
        return "botNotInServer"
    #bot is not in the same channel of the user
    if ctx.author.voice.channel.id != botVoiceClients[ctx.guild.id].channel.id:
        return "botNotInChannel"
    return "sameServerAndChannel"

def searchYoutube(searchPhrase):

    with yt_dlp.YoutubeDL(ytdl_format_options) as youtubeDlObj:

        
        try:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)['entries'][0]
        except Exception:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)
            print(info)
            return {'source': info['formats'][7]['url'], 'title': info['title'], 'duration': info['duration']}
    print(info)
    return {'source': info['formats'][7]['url'], 'title': info['title'], 'duration': info['duration']}
 
def playFromUrl(url, vcClient, seekSec = 0):
    ffmpeg_options['options'] = f'-vn -ss {seekSec}'
    vcClient.play(discord.FFmpegPCMAudio(url,**ffmpeg_options)
        ,after= lambda err: print('Player error: %s' % err) if err else playNext(vcClient))
    print(str(discord.FFmpegPCMAudio(url,**ffmpeg_options)))

def playNext(vcClient):
    songQueues[vcClient.guild.id].pop(0)
    if len(songQueues[vcClient.guild.id]) == 0:
        print("Queue empty")
        return
    else:
        playFromUrl(songQueues[vcClient.guild.id][0]['source'],vcClient)

def tryBeginPlay(vcClient):
    if len(songQueues[vcClient.guild.id]) == 1 :
        playFromUrl(songQueues[vcClient.guild.id][0]['source'],vcClient)

def getEta(quePos,serverId):
    tot = 0
    for x in range(0, quePos):
        tot += int(songQueues[serverId][x]['duration'])
    return tot


