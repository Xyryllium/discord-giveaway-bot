import random
import asyncio
import datetime
import time
import nextcord
from nextcord.ext import commands
from dateutil import tz
from nextcord.ext.commands import MemberConverter

client = commands.Bot(command_prefix=">")



@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

@client.command()
@commands.has_role("Giveaway")
async def gstart(ctx, time: str, numberOfWinners: int, prize:str, message:str):
    embed = nextcord.Embed(title = f"{prize}")

    convertedTime = convert(time)

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    
    unit = time[-1]

    print(convertedTime)

    if unit == 's':
        utc = datetime.datetime.utcnow() + datetime.timedelta(seconds = convertedTime)
    elif unit == 'm':
        utc = datetime.datetime.utcnow() + datetime.timedelta(minutes = convertedTime/60)
    elif unit == 'h':
        utc = datetime.datetime.utcnow() + datetime.timedelta(hours = convertedTime/3600)
    else:
       utc = datetime.datetime.utcnow() + datetime.timedelta(days = convertedTime)

    
    utc = utc.replace(tzinfo=from_zone)
    
    local_time = utc.astimezone(to_zone)

    format_time = local_time.strftime('%Y-%m-%d %H:%M:%S')

    embed.add_field(name = "Ends At:", value =f"{format_time}\n")
    
    embed.add_field(name = "Winners:", value =f"{numberOfWinners}")
    
    embed.set_footer(text = f"Ends {time} from now!")

    my_msg = await ctx.send(embed = embed)

    await my_msg.add_reaction("🎉")


    await asyncio.sleep(convertedTime)

    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    users_mention = []

    n = 0
    for _ in range(numberOfWinners):
        winner = random.choice(users)
        users.pop(users.index(winner))
        message = f"{message}";
        embed = nextcord.Embed(title=message)
        await winner.send(embed=embed)
        n = n + 1
        users_mention.append(winner.mention)
    await ctx.send(f"Congratulations {users_mention} you won the giveaway !")
    

client.run("OTQ4ODkyMjI2MTY2MDYzMTA0.YiCawA.pGdZ1raAL32iypvozWcp1PNA0I4")