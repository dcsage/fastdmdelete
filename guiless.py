# Importing
import json
import os
import random
import time
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from colorama import Fore, init
token = "YOURTOKEN"
init()

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned, owner_id =108731110833283072 , intents=intents)
client.remove_command('help')

global sent
sent = 0

global deleted
deleted = 0

MAX_CONCURRENT_TASKS = 50
sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

@client.event
async def on_ready():
  print(f"")
  print(f"           {Fore.CYAN}Logged in as {Fore.WHITE}{client.user} ")
  print(f" ")

async def send_message_to_user(user):
    global sent
    global deleted
    if user.bot == True:
        pass
    else:
        try:
            # Acquire the semaphore to limit the number of concurrent tasks
            async with sem:
                chann = await user.create_dm()
                async for message in chann.history(limit=100):
                    if message.author == client.user:
                        await message.delete()
                        deleted = deleted + 1
                        print(f"{Fore.WHITE}[{Fore.CYAN}DELETED{Fore.WHITE}] #{deleted} Deleted a message with {Fore.CYAN}{user} {Fore.WHITE}| {Fore.CYAN}{message.id}")
                        await asyncio.sleep(1)
                sent = sent + 1
                print(f"{Fore.WHITE}[{Fore.GREEN}CLEARED{Fore.WHITE}] #{sent} Cleared DMS with {Fore.WHITE}{user}")
        except:
            # Catch and handle exceptions when sending messages to users
            print(f"{Fore.WHITE}[{Fore.RED}FAIL{Fore.WHITE}] #{sent} Something went wrong with {Fore.WHITE}")

@client.command()
async def deletemessages(ctx):
    dmable_members = set(client.get_all_members())
    tasks = [send_message_to_user(user) for user in dmable_members]
    await asyncio.gather(*tasks)

client.run(token)
