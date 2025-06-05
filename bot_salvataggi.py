import os
import subprocess
import datetime
import time
import discord
from discord.ext import tasks, commands
import asyncio
from dotenv import load_dotenv

# Carica variabili da .env
load_dotenv()

# Percorso del programma WinRAR (modifica se diverso)
RAR_EXE_PATH = os.getenv("RAR_EXE_PATH")

# Cartelle di salvataggio e destinazione
SAVE_FOLDER = os.getenv("SAVE_FOLDER")
DEST_FOLDER = os.getenv("DEST_FOLDER")

# Token e ID canale Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Inizializza il bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

last_sent_timestamp = None  # Traccia l'ultimo salvataggio inviato

def is_file_in_use(filepath):
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, 'a'):
            return False
    except IOError:
        return True

def compress_saves():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(DEST_FOLDER, f"PlanetCrafter_Saves_{timestamp}.rar")
    
    if not os.path.exists(RAR_EXE_PATH):
        print(f"ERRORE: Il percorso RAR.EXE non è valido: {RAR_EXE_PATH}")
        return None

    exclude_files = []
    for root, dirs, files in os.walk(SAVE_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            if is_file_in_use(file_path):
                print(f"Il file {file_path} è in uso, lo escludo.")
                exclude_files.append(file_path)

    exclude_params = [f'-x"{file}"' for file in exclude_files]
    command = [RAR_EXE_PATH, "a", "-r", archive_path, SAVE_FOLDER] + exclude_params

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return archive_path
    except subprocess.CalledProcessError as e:
        print(f"Errore: {e.stderr.decode()}")
    except Exception as e:
        print(f"Errore sconosciuto: {e}")
    return None

async def send_to_discord(archive_path):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print("Canale Discord non trovato.")
        return
    try:
        await channel.send("Ecco il salvataggio di Planet Crafter:", file=discord.File(archive_path))
        print(f"Inviato: {archive_path}")
    except Exception as e:
        print(f"Errore Discord: {e}")

async def monitor_saves():
    global last_sent_timestamp
    print("Monitoraggio attivo...")
    while True:
        save_file = os.path.join(SAVE_FOLDER, "Standard-1.json")
        if os.path.exists(save_file):
            file_mod_time = os.path.getmtime(save_file)
            if last_sent_timestamp is None or file_mod_time > last_sent_timestamp:
                print("Modifica rilevata, creo archivio...")
                archive_path = compress_saves()
                if archive_path:
                    last_sent_timestamp = file_mod_time
                    await send_to_discord(archive_path)
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(f"{bot.user} connesso.")
    bot.loop.create_task(monitor_saves())

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
