import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

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
  await event_flow(ctx.author)

async def event_flow(user):
  title = await getTitle(user)
  description = await getDescription(user)
  dateTime = await getDateTime(user)

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
  return msg

bot.run(os.getenv("DISCORD_TOKEN"))