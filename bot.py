import os
import discord
import database
import uuid
import time
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
        
#     await message.channel.send('Hello!')
#     await bot.process_commands(message)


@bot.command(pass_context=True)
async def evento(ctx):
  await event_flow(ctx)

@bot.command(pass_context=True)
async def eventos(ctx, id):
  await ctx.author.send(database.getEvent(id))

@bot.command(pass_context=True)
async def chamar(ctx, id):
  await ctx.author.send(database.getEvent(id))

async def event_flow(ctx):
  # title = await getTitle(ctx.author)
  # description = await getDescription(ctx.author)
  # dateTime = await getDateTime(ctx.author)
  title = "Eventozada"
  description = "Vai set topper"
  dateTime = datetime.strptime('11/06/2021 15:30', '%d/%m/%Y %H:%M')
  eventId = str(uuid.uuid4()) 
  event = {
    'id': eventId,
    'title': title, 
    'description': description, 
    'datetime': dateTime.strftime('%d/%m/%Y %H:%M'),
    'createdBy': ctx.author.display_name,
    'users': []
    }
  database.addEvent(event)

  await sendEventMessage(ctx, event, eventId)

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

async def sendEventMessage(ctx, event, id):
  embed = discord.Embed(
    title = event['title'],
    description = event['description'],
    colour = discord.Colour.gold(),
  )

  embed.set_footer(text="Evento criado por {}".format(event['createdBy']))
  embed.add_field(name="Data e hora", value=event['datetime'], inline=False)
  message = await ctx.channel.send(embed=embed)
  await message.add_reaction("drake_yes:852995599853944842")
  await message.add_reaction("drake_no:852995631030730752")

  # def check(reaction, user):
  #   check = reaction.emoji == "drake_yes:852995599853944842" 
  #   print(check)
  #   return check

  check = lambda reaction, user: bot.user != user and reaction.emoji == bot.get_emoji(852995599853944842)

  start_time = time.time()
  seconds = 3

  while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    reaction, user = await bot.wait_for('reaction_add', timeout=3, check=check)
    database.addUserToEvent(user, id)

    if elapsed_time > seconds:
      break    

bot.run(os.getenv("DISCORD_TOKEN"))