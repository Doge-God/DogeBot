from logging import raiseExceptions
from data import *

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
