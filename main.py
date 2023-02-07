# -*- coding: utf-8 -*- 

# Import discord.py. Allows access to Discord's API.
import discord

import os

from dotenv import load_dotenv

from discord.ext import commands

import openai

import re


# Loads the .env file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Creates a new Bot object with a specified prefix. It can be whatever you want it to be.
# all() 表示所有權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# on_message() event listener. Notice it is using @bot.event as opposed to @bot.command().
@bot.event
async def on_message(message):

	#match = re.search('(?<=!小孤獨\s).+', message.content) #prompt=match.group(0),
	prefix = message.content[0:5]

	if prefix == '!小孤獨 ':
		print(message.content)
		print(message.content[5:])

		response = openai.Completion.create(
			model="text-davinci-003",
			prompt=message.content[5:],
			temperature=0, # 隨機文字組合，範圍 0～1，預設 0.5，0 表示不隨機，1 表示完全隨機。
			max_tokens=3900, # 希望 AI 回傳的最大字數
		)

		# Sends a message to the channel.
		await message.channel.send(response.choices[0].text)

	# Includes the commands for the bot. Without this line, you cannot trigger your commands.
	#await bot.process_commands(message)


# Command $ping. Invokes only when the message "$ping" is send in the Discord server.
# Alternatively @bot.command(name="ping") can be used if another function name is desired.
@bot.command()
async def testPing(ctx):
	# Sends a message to the channel using the Context object.
	await ctx.channel.send("pong")


@bot.command(
	# Adds this value to the $help ping message.
	help="輸入 !pin 和 dc 訊息 ID 來釘選",
	# Adds this value to the $help message.
	brief="輸入 !pin 和 dc 訊息 ID 來釘選"
)
async def pin(ctx, message_id: int):
    message = await ctx.fetch_message(message_id)
    await message.pin()


@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == "📌":
        await bot.pin_message(reaction.message)



# Command $print. This takes an in a list of arguments from the user and simply prints the values back to the channel.
# @bot.command(
# 	# Adds this value to the $help print message.
# 	help="Looks like you need some help.",
# 	# Adds this value to the $help message.
# 	brief="Prints the list of values back to the channel."
# )
# async def print(ctx, *args):
	# response = ""

	# # Loops through the list of arguments that the user inputs.
	# for arg in args:
	# 	response = response + " " + arg

	# # Sends a message to the channel using the Context object.
	# await ctx.channel.send(response)


# Executes the bot with the specified token. Token has been removed and used just as an example.
bot.run(DISCORD_TOKEN)
