import os
import discord
import logging
import pandas as pd
from discord.ext import commands
import re

logging.basicConfig(level=logging.INFO)

#client = discord.Client()
bot = commands.Bot(command_prefix='_')
guild = discord.Guild

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game('_scan help'))

def is_command (msg):
    if len(msg.content) == 0:
        return False
    elif msg.content.split()[0] == '_scan':
        return True
    else:
        return False

@bot.command()
async def get_long_msg(ctx, *, person=""):
    dataList = []#pd.DataFrame(columns=['content', 'time', 'author'])
    message = ctx.message
    # Acquiring the channel via the bot command
    channel = message.channel
    print(person)    
    
    answer = discord.Embed(title="Creating your Dataframe of links",
                           description="Data is on the way...",
                           colour=0x1a7794) 
    
    await message.channel.send(embed=answer)
    
    async for msg in channel.history(limit=1000):       # The added 1000 is so in case it skips messages for being
        if (msg.author != bot.user) and (msg.author.name == person if len(person)>0 else True): 
            if not is_command(msg):                             # the total amount originally specified by the user.
                msgText = msg.content if not msg.attachments else 'Image'
                #data = []
                if len(msgText) > 2:
                        dataList.append({'content': msgText,
                                    'time': msg.created_at,
                                    'author': msg.author.name,
                                    'reference': (await channel.fetch_message(msg.reference.message_id)).content if msg.reference else ""})
    
    # Turning the pandas dataframe into a .csv file and sending it to the user
    data = pd.DataFrame.from_records(dataList)
    file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determining file name and location
    data.to_csv(file_location) # Saving the file as a .csv via pandas
    
    answer = discord.Embed(title="Here is your .CSV File",
                           description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : 1000""",
                           colour=0x1a7794) 
    
    #await message.author.send(embed=answer)
    data_dump_channel = bot.get_channel(ADD DESTINATION CHANNEL ID HERE)
    #await message.channel.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
    await data_dump_channel.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
    os.remove(file_location) # Deleting the file



@bot.command()
async def get_links(ctx, *, msglen=1000):
    dataList = []#pd.DataFrame(columns=['content', 'time', 'author'])
    message = ctx.message
    # Acquiring the channel via the bot command
    if len(message.channel_mentions) > 0:
        channel = message.channel_mentions[0]
    else:
        channel = message.channel

    if(channel != "Design related websites"):
        await message.channel.send(embed=discord.Embed(title="Wrong channel.", description="Please try in the design related webites channel"))
        return
    
    answer = discord.Embed(title="Creating your Dataframe of links",
                           description="Data is on the way...",
                           colour=0x1a7794) 
    
    await message.channel.send(embed=answer)
    
    async for msg in channel.history(limit=int(msglen)):       # The added 1000 is so in case it skips messages for being
        if msg.author != bot.user:                           # a command or a message it sent, it will still read the
            if not is_command(msg):                             # the total amount originally specified by the user.
                msgText = msg.content if not msg.attachments else 'Image'
                urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', msgText)
                #data = []
                if len(urls) > 0:
                        dataList.append({'content': urls,
                                    'time': msg.created_at,
                                    'author': msg.author.name})
    
    # Turning the pandas dataframe into a .csv file and sending it to the user
    data = pd.DataFrame.from_records(dataList)
    file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determining file name and location
    data.to_csv(file_location) # Saving the file as a .csv via pandas
    
    answer = discord.Embed(title="Here is your .CSV File",
                           description=f"""It might have taken a while, but here is what you asked for.\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : 1000""",
                           colour=0x1a7794) 
    
    #await message.author.send(embed=answer)
    data_dump_channel = bot.get_channel(ADD DESTINATION CHANNEL ID HERE)
    #await message.channel.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
    await data_dump_channel.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
    os.remove(file_location) # Deleting the file





bot.run(ADD BOT KEY HERE)

