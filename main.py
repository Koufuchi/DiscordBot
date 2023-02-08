# -*- coding: utf-8 -*- 

import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai
import os
import re


# Loads the .env file that resides on the same level as the script.
load_dotenv()

# 讀取 env
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# all() 表示所有權限
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 紀錄問過的東西
sendMsg = []

# on_message() 監聽器
@bot.event
async def on_message(message):

    prefix = message.content[0:5]

    if prefix == '!小孤獨5':
        print(message.content)

        sendMsg.append(message.content[5:])

        prompt = ''

        for i in sendMsg:
            prompt = prompt + '\n' + i

        response = openai.Completion.create(
        	model="text-davinci-003",
        	prompt=message.content[5:],
        	temperature=0, # 隨機文字組合，範圍 0～1，預設 0.5，0 表示不隨機，1 表示完全隨機。
        	max_tokens=3900, # 希望 AI 回傳的最大字數
        )

        # 傳訊息到聊天室
        await message.channel.send(response.choices[0].text)

    # Includes the commands for the bot. Without this line, you cannot trigger your commands.
    await bot.process_commands(message)

# 清空發問歷史
@bot.command()
async def reset(ctx):
    sendMsg = []

    await ctx.channel.send('已清空發問歷史')

# 查詢發問歷史
@bot.command()
async def send(ctx):
    his = ''
    for i in sendMsg:
        his = his + '\n' + i

    await ctx.channel.send(his)


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


# 啟動機器人
bot.run(DISCORD_TOKEN)
