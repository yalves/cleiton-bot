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

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

@bot.command(pass_context=True)
async def evento(ctx):
  await event_flow(ctx.author)

async def event_flow(user):
  await user.send("Qual o título do evento?")



bot.run(os.getenv("DISCORD_TOKEN"))