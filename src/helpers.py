from data import botVoiceClients
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
def getVcCommandVcClient(ctx):
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

#========================================================================================
ytdl_format_options = {
    'format': 'bestaudio/best',
    #'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
}
#====================================================================================

def searchYoutube(searchPhrase):
    with youtube_dl.YoutubeDL(ytdl_format_options) as youtubeDlObj:
        try:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)['entries'][0]
        except Exception:
            info = youtubeDlObj.extract_info(str(searchPhrase), download=False)
            return {'source': info['formats'][0]['url'], 'title': info['title']}
    return {'source': info['formats'][0]['url'], 'title': info['title']}

async def playFromUrl(url, vcClient):
    vcClient.play(discord.FFmpegPCMAudio(url,**ffmpeg_options), 
    after=lambda e: print('complete'))
    print(str(discord.FFmpegPCMAudio(url,**ffmpeg_options)))

def test():
    with youtube_dl.YoutubeDL(ytdl_format_options) as youtubeDlObj:
        try:
            return youtubeDlObj.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley'
            , download=False)['formats'][0]['url']
        except Exception as e:
            print(e)

