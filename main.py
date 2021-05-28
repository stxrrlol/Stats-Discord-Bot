import os
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')

@bot.command()
async def stats(ctx, *, arg):
    headers = {"TRN-Api-Key": "be1a9da5-fcea-4b47-9323-cb02a5b39a87"}
    regions = ['NAE', 'EU', 'NAW', 'OCE', 'BR', 'ME', 'ASIA']
    platforms = ['CONSOLE', 'MOBILE', 'PC', 'GLOBAL']
    rc = bool([ele for ele in regions if(ele in arg.upper())])
    plc = bool([ele for ele in platforms if(ele in arg.upper())])
    if (rc == False) & (plc == True):
        await ctx.send('Your region is not a valid region')
    if (rc == True) & (plc == False):
        await ctx.send('Your platform is not a valid platform')
    if (rc == True) & (plc == True):
        a = 0
        while a <= 6:
            test = arg.upper().find(regions[a])
            if test != -1:
                region = regions[a]
            a = a + 1
        a = 0
        while a <= 3:
            test = arg.upper().find(platforms[a])
            if test != -1:
                platform = platforms[a]
            a = a + 1
        arg = arg.lower()
        region = region.lower()
        platform = platform.lower()
        arg = arg.split(' ')
        a = arg.index(platform)
        del arg[a]
        a = arg.index(region)
        del arg[a]
        epic = ' '.join(arg)
        epic = epic.replace(' ', '%20')
        url = 'https://fortnitetracker.com/api/v0/profiles/find?platformUserHandle=' + epic
        r = requests.get(url, headers=headers)
        if r.text == '':
            await ctx.send('The epic name you entered does not exist')
        if r.text != '':
            url = 'https://api.fortnitetracker.com/v1/powerrankings/' + platform + '/' + region + '/' + epic
            r = requests.get(url, headers=headers)
            y = r.json()
            if y == {'status': 'Try again in a few minutes. PR is updating'}:
                await ctx.send('No stats have been found for this player on this platform in this region')
            if y != {'status': 'Try again in a few minutes. PR is updating'}:
                pr = '{:,}'.format(y['points'])
                earnings = '$' + '{:,}'.format(y['cashPrize'])
                events = '{:,}'.format(y['events'])
                rank = '{:,}'.format(y['rank'])
                epic = y['name']
                await ctx.send(epic + '\n--------------------\n<:powerrank:847508034620096532> ' + pr + '\n:moneybag: ' + earnings + '\nRank: ' + rank + '\nEvents: ' + events)

bot.run(TOKEN)
