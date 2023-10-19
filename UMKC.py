# Project UMKC 1 by Alex Arbuckle #

from asyncio import sleep
from json import load, dump
from datetime import datetime
from discord.ext import commands

token = ''
client = commands.Bot(command_prefix = '')

def setDict(arg):
    '''  '''

    # open file
    with open('UMKC.json', 'w') as f:

        # write dictionary
        dump(arg, f, indent = 4)

def getDict():
    '''  '''

    # if file
    try:

        # open flie
        with open('UMKC.json', 'r') as f:

            # return data
            return {int(i) : j for i, j in load(f).items()}

    # if no file
    except:

        # return new
        return {}

@client.command()
async def setChannel(ctx):
    '''  '''

    # getting current dictionary
    d = getDict()

    # if class does not exist
    if (ctx.channel.id not in d.keys()):

        # declaring class in dictionary
        d[int(ctx.channel.id)] = {}

        # declaring and initializing link
        d[int(ctx.channel.id)]['link'] = 'No Link Available'

        # updating dictionary
        setDict(d)

@client.command()
async def setTitle(ctx, *args):
    '''  '''

    # getting current dictionary
    d = getDict()

    # setting class title
    d[ctx.channel.id]['title'] = ''.join('{} '.format(i) for i in args)

    # updating dictionary
    setDict(d)

@client.command()
async def getTitle(ctx):
    '''  '''

    # getting current dictionary
    d = getDict()

    # if title exists
    try:

        # sending title
        await ctx.channel.send(d[ctx.channel.id]['title'], delete_after = 60.0)

    except:

        pass

@client.command()
async def setTime(ctx, arg, *args):
    '''  '''

    # getting current dictionary
    d = getDict()

    # setting class time
    d[ctx.channel.id]['time'] = arg
    d[ctx.channel.id]['day'] = [i for i in args]

    # updating dictionary
    setDict(d)

@client.command()
async def getTime(ctx):
    '''  '''

    # getting current dictionary
    d = getDict()

    # if time exists
    try:

        # getting time
        time = d[ctx.channel.id]['time']
        day = ''.join(i for i in d[ctx.channel.id]['day'])

        # sending time
        await ctx.channel.send('{} {}'.format(time, day), delete_after = 60.0)

    except:

        pass

@client.command()
async def setLink(ctx, arg):
    '''  '''

    # getting current dictionary
    d = getDict()

    # setting class link
    d[ctx.channel.id]['link'] = arg

    # updating dictionary
    setDict(d)

@client.command()
async def getLink(ctx):
    '''  '''

    # getting current dictionary
    d = getDict()

    # if link exists
    try:

        # sending link
        await ctx.channel.send(d[ctx.channel.id]['link'], delete_after = 60.0)

    except:

        pass

@client.command()
async def init(ctx):
    '''  '''

    # while running
    while (True):

        # if new minute
        if (datetime.now().second % 60 == 0):

            # check for class
            d, day = getDict(), datetime.today().weekday()
            time = '{}{}'.format(datetime.now().hour, datetime.now().minute)
            for i in d.keys():

                # if class
                if ((time == d[i]['time']) and (str(day) in d[i]['day'])):

                    # building notification
                    notification = ':alarm_clock: {}:alarm_clock:'.format(d[i]['title'])
                    notification += '\n\n{}'.format(d[i]['link'])

                    # sending notification
                    await client.get_channel(i).send(notification, delete_after = 600.0)

            # stall
            await sleep(55)

client.run(token)
