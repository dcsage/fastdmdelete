# enjoy
import threading
import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from colorama import Fore, init
import customtkinter

global sent
sent = 0

global deleted
deleted = 0

MAX_CONCURRENT_TASKS = 50
sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

intents = discord.Intents.default()
intents.members = True

# intents.presences = True | CHANGE THIS IF YOU HAVE PRESENCE INTENTS FOR SPEEDY LOGIN

client = commands.AutoShardedBot(command_prefix=commands.when_mentioned, owner_id =108731110833283072 , intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    text_box.configure(state="normal")
    # log output to text box with red color
    text_box.insert("end", " \n")
    text_box.insert("end", f"Bot logged in as {client.user} \n")
    text_box.insert("end", " \n")
    text_box.configure(state="disabled")
    # scroll text box to the bottom
    text_box.see("end")
    dmable_members = set(client.get_all_members())
    tasks = [send_message_to_user(user) for user in dmable_members]
    await asyncio.gather(*tasks)

# themes

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("700x550")
root.title("$age's Mass Deleter")

async def send_message_to_user(user):
    global sent
    global deleted
    if user.bot == True:
        pass
    else:
        # Acquire the semaphore to limit the number of concurrent tasks
        async with sem:
            chann = await user.create_dm()
            async for message in chann.history(limit=100):
                if message.author == client.user:
                    await message.delete()
                    deleted = deleted + 1
                    await asyncio.sleep(1)
            sent = sent + 1
            text_box.configure(state="normal")
            text_box.insert("end",f"\n[CLEARED] #{sent} | {user} | {deleted} MD")
            text_box.configure(state="disabled")
            text_box.see("end")


def loginconf(token):
    try:

        token = token 
        client.run(token)
    except:
        text_box.configure(state="normal")
        text_box.insert("end",f"\nInvalid token entered, please restart the app.")
        text_box.configure(state="disabled")
        text_box.see("end")

def login():
    button.configure(state="disabled")
    entry1.configure(state="disabled")
    text_box.configure(state="normal")
    # log output to text box with red color
    text_box.configure(state="disabled")
    # scroll text box to the bottom
    text_box.see("end")
    token = entry1.get()
    threading.Thread(target=loginconf, args=(token,)).start()


frame = customtkinter.CTkFrame(master = root)
frame.pack(pady=40, padx=120, fill="both", expand = True)

label = customtkinter.CTkLabel(master=frame, text="$age's Deleter Menu | V1.3 | New Features")
label.pack(side="top",pady=20, padx = 10)


entry1 = customtkinter.CTkEntry(master=frame, placeholder_text = "Bot Token",show = "*")
entry1.pack(pady=12,padx=10)
entry1.configure(height=30, width=300)


button = customtkinter.CTkButton(master=frame, text="Delete DMS",command=login)
button.pack(pady=12, padx=10)

# create text box to log output
text_box = customtkinter.CTkTextbox(master=frame)
text_box.pack(side="bottom", pady=12, padx=10)
text_box.configure(height=300, width=500)
text_box.configure(state="disabled")

root.mainloop()
init()
