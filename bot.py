import os
import discord
import mongo as database
import uuid
import time
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks
from datetime import datetime
from pytz import timezone

load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_reaction_add(reaction, user):
  if user == bot.user or reaction.message.author != bot.user:
    return

  drakeYes = bot.get_emoji(852995599853944842)
  drakeNo = bot.get_emoji(852995631030730752)

  if reaction.emoji == drakeYes:
    await reaction.message.remove_reaction(drakeNo, user)
    database.addUserToEvent(user, reaction.message.id)

  if reaction.emoji == drakeNo:
    await reaction.message.remove_reaction(drakeYes, user)
    database.removeUserFromEvent(user, reaction.message.id)
  

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
        
#     await message.channel.send('Hello!')
#     await bot.process_commands(message)


@bot.command(pass_context=True)
async def evento(ctx):
  await event_flow(ctx)

@tasks.loop(seconds = 60)
async def remindEvents():
  now = datetime.now().astimezone(timezone('America/Sao_Paulo'))
  date = now.strftime('%d/%m/%Y %H:%M')
  events = database.getEventsByDateTime(date)
  for event in events:
    await sendReminderMessage(event)
    database.removeEvent(event)
    
@remindEvents.before_loop
async def before():
    await bot.wait_until_ready()

async def sendReminderMessage(event):
  userMentions = [ bot.get_user(x).mention for x in event['users'] ]
  embed = discord.Embed(
    title = F"[COMEÇANDO] {event['title']}",
    description = " ".join(userMentions),
    colour = discord.Colour.teal(),
  )

  embed.set_footer(text="Evento criado por {}".format(event['createdBy']))
  await bot.get_channel(event['channel']).send(embed=embed) 

  #also send a dm to users in userMentions
  for user in event['users']:
    await bot.get_user(user).send(embed=embed)

async def event_flow(ctx):
  title = await getTitle(ctx.author)
  description = await getDescription(ctx.author)
  dateTime = await getDateTime(ctx.author)
  channelId = ctx.channel.id
  event = {
    'title': title, 
    'description': description, 
    'datetime': dateTime.strftime('%d/%m/%Y %H:%M'),
    'createdBy': ctx.author.display_name,
    'users': [],
    'channel': channelId
    }  

  eventMessageLink = await sendEventMessage(ctx, event)
  await sendMessageLink(ctx.author, eventMessageLink)

async def getTitle(user):
  embed = discord.Embed(
    title = 'Qual o título do evento?',
    description = 'Até 200 caracters',
    colour = discord.Colour.blue(),
  )
  await user.send(embed=embed)

  def check(m):
      return m.author == user

  msg = await bot.wait_for('message', check=check)
  return msg.content

async def getDescription(user):
  embed = discord.Embed(
    title = 'Qual a descrição do evento?',
    description = 'Até 200 caracters',
    colour = discord.Colour.blue(),
  )
  await user.send(embed=embed)

  def check(m):
      return m.author == user

  msg = await bot.wait_for('message', check=check)
  return msg.content

async def getDateTime(user):
  embed = discord.Embed(
    title = 'Qual a data/hora do evento?',
    description = 'Favor usar o formato dd/mm/yyyy hh:mm',
    colour = discord.Colour.blue(),
  )
  await user.send(embed=embed)

  def check(m):
      return m.author == user

  msg = await bot.wait_for('message', check=check)
  return datetime.strptime(msg.content, '%d/%m/%Y %H:%M')

async def sendEventMessage(ctx, event):
  embed = discord.Embed(
    title = event['title'],
    description = event['description'],
    colour = discord.Colour.gold(),
  )

  embed.set_footer(text="Evento criado por {}".format(event['createdBy']))
  embed.add_field(name="Data e hora", value=event['datetime'], inline=False)
  message = await ctx.channel.send(embed=embed)
  event['id'] = message.id
  database.addEvent(event)
  await message.add_reaction("drake_yes:852995599853944842")
  await message.add_reaction("drake_no:852995631030730752")
  return message.jump_url

async def sendMessageLink(user, eventMessageLink):
  embed = discord.Embed(
    title = "O evento foi criado",
    description = f"[Clique aqui para visualizar]({eventMessageLink})",
    colour = discord.Colour.green(),
  )
  await user.send(embed=embed)

remindEvents.start()

bot.run(os.getenv("DISCORD_TOKEN"))