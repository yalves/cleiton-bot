import os
import discord
import database
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

async def event_flow(ctx):
  title = await getTitle(ctx.author)
  description = await getDescription(ctx.author)
  dateTime = await getDateTime(ctx.author)
  event = {'title': title, 'description': description, 'datetime': dateTime.strftime('%d/%m/%Y %H:%M')}
  id = database.addEvent(event)

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

bot.run(os.getenv("DISCORD_TOKEN"))