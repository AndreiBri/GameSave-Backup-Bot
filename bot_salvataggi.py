import os
import subprocess
import datetime
import time
import discord
from discord.ext import tasks, commands
import asyncio

# Percorso del programma WinRAR (modifica il percorso in base alla tua installazione)
RAR_EXE_PATH = r'C:\Program Files\WinRAR\rar.exe'

# Cartella di salvataggio di Planet Crafter
SAVE_FOLDER = r'C:\Users\User\AppData\LocalLow\MijuGames\Planet Crafter'

# Cartella di destinazione per l'archivio
DEST_FOLDER = r'C:\Users\User\Desktop\SalvataggiPlanetCrafter'

# Token del bot Discord (sostituisci con il tuo token)
DISCORD_TOKEN = 'MTI4Mzk1MTM2ODI2ODE1NzAwMQ.GAgFkP.Lqy_KZDD6AYk2bEgkfVI1qTu6nxlMpn5_wHW_E'
# ID del canale Discord (sostituisci con l'ID del canale dove inviare i file)
DISCORD_CHANNEL_ID = 1311648131183804506

# Inizializza il bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Variabile per tenere traccia dell'ultimo salvataggio inviato
last_sent_timestamp = None

# Funzione per verificare se un file è in uso
def is_file_in_use(filepath):
    """Verifica se il file è in uso da un altro processo."""
    if not os.path.exists(filepath):
        return False
    try:
        with open(filepath, 'a'):
            return False  # Se il file può essere aperto in modalità append, non è in uso
    except IOError:
        return True  # Se il file non può essere aperto, è in uso

# Funzione per comprimere i salvataggi in un archivio
def compress_saves():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(DEST_FOLDER, f"PlanetCrafter_Saves_{timestamp}.rar")
    print(f"Sto per creare l'archivio in: {archive_path}")
    
    if not os.path.exists(RAR_EXE_PATH):
        print(f"ERRORE: Il percorso di RAR.EXE non è valido: {RAR_EXE_PATH}")
        return None

    # Evitare citazioni extra nei percorsi
    save_folder_quoted = SAVE_FOLDER
    archive_path_quoted = archive_path

    # Aggiungi una lista per i file da escludere
    exclude_files = []

    # Scorri i file nella cartella di salvataggio e aggiungi quelli in uso alla lista di esclusione
    for root, dirs, files in os.walk(SAVE_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            if is_file_in_use(file_path):
                print(f"Il file {file_path} è in uso, lo escluderò dall'archivio.")
                exclude_files.append(file_path)

    # Costruisci il comando RAR con l'opzione -x per escludere i file
    exclude_params = [f'-x"{file}"' for file in exclude_files]

    # Correzione del comando RAR
    command = [RAR_EXE_PATH, "a", "-r", archive_path_quoted, save_folder_quoted] + exclude_params

    # Esegui il comando
    try:
        print("Esecuzione del comando RAR...")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Comando RAR eseguito con successo!")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione del comando: {e}")
        print(f"Stderr: {e.stderr.decode()}")
    except Exception as e:
        print(f"Errore sconosciuto: {e}")
    
    return archive_path

# Funzione per inviare il file su Discord
async def send_to_discord(archive_path):
    """Invia il file compresso su Discord."""
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print("Canale Discord non trovato!")
        return

    try:
        await channel.send("Ecco il salvataggio di Planet Crafter:", file=discord.File(archive_path))
        print(f"File {archive_path} inviato a Discord!")
    except Exception as e:
        print(f"Errore durante l'invio a Discord: {e}")

# Funzione per monitorare i salvataggi
async def monitor_saves():
    global last_sent_timestamp
    # Usa un ciclo per monitorare costantemente la cartella
    print("Monitoraggio dei salvataggi di Planet Crafter...")
    while True:
        # Controlla se ci sono modifiche ai file di salvataggio
        save_file = os.path.join(SAVE_FOLDER, "Standard-1.json")
        
        if os.path.exists(save_file):
            file_mod_time = os.path.getmtime(save_file)
            # Se l'ultimo salvataggio è stato modificato e non è stato inviato
            if last_sent_timestamp is None or file_mod_time > last_sent_timestamp:
                print(f"Modifica rilevata: {save_file}")
                archive_path = compress_saves()
                if archive_path:
                    # Aggiorna il timestamp dell'ultimo salvataggio inviato
                    last_sent_timestamp = file_mod_time
                    # Invio del file su Discord
                    await send_to_discord(archive_path)
        
        await asyncio.sleep(10)  # Attendi 10 secondi prima di controllare di nuovo

@bot.event
async def on_ready():
    """Quando il bot è pronto, inizia il monitoraggio."""
    print(f"{bot.user} è connesso a Discord!")
    # Avvia il monitoraggio come task asincrono
    bot.loop.create_task(monitor_saves())

if __name__ == "__main__":
    # Avvia il bot Discord
    bot.run(DISCORD_TOKEN)
