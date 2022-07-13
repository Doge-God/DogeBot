from data import botVoiceClients
from data import ytdl_format_options
from data import ffmpeg_options
from data import songQueues
import youtube_dl
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
    with youtube_dl.YoutubeDL(ytdl_format_options) as youtubeDlObj:
        try:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)['entries'][0]
        except Exception:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)
            return {'source': info['formats'][0]['url'], 'title': info['title']}
    return {'source': info['formats'][0]['url'], 'title': info['title'], 'duration': info['duration']}

def playFromUrl(url, vcClient):
    vcClient.play(discord.FFmpegPCMAudio(url,**ffmpeg_options)
        ,after= lambda err=None: playNext(vcClient))
    print(str(discord.FFmpegPCMAudio(url,**ffmpeg_options)))

def playNext(vcClient):
    if len(songQueues[vcClient.guild.id]) == 1:
        songQueues[vcClient.guild.id].pop(0)
    else:
        songQueues[vcClient.guild.id].pop(0)
        playFromUrl(songQueues[vcClient.guild.id][0]['source'],vcClient)

def tryBeginPlay(vcClient):
    if len(songQueues[vcClient.guild.id]) == 1:
        print("Try begin play:")
        print(songQueues[vcClient.guild.id][0]['source'])
        print(vcClient.session_id)
        playFromUrl(songQueues[vcClient.guild.id][0]['source'],vcClient)
    else:
        print(len(songQueues[vcClient.guild.id]))
        pass

def test():
    with youtube_dl.YoutubeDL(ytdl_format_options) as youtubeDlObj:
        try:
            return youtubeDlObj.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'
            , download=False)['formats'][0]['url']
        except Exception as e:
            print(e)

