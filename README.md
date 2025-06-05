# 🪐 Planet Crafter Save Backup Bot

This Discord bot automatically monitors your **Planet Crafter** save folder.
When a new or updated save is detected, it compresses the files into a `.rar` archive and uploads it directly to a Discord channel.

---

## ✅ Features

* 📁 Monitors the Planet Crafter save file `Standard-1.json`
* 🗜️ Compresses all save data into a `.rar` file using WinRAR
* 🤖 Sends the backup to a specific Discord channel automatically
* 🔐 Uses a `.env` file to keep all private information secure

---

## 🧠 Requirements

* Python 3.8 or higher
* [WinRAR](https://www.win-rar.com/start.html?&L=0) (must be installed and `rar.exe` path set correctly)
* A Discord bot with the following permissions:

  * `Send Messages`
  * `Attach Files`
* Python packages:

  * `discord.py`
  * `python-dotenv`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Setup

### 1. Clone or download the repository

```bash
git clone https://github.com/your-username/planet-crafter-backup-bot.git
cd planet-crafter-backup-bot
```

### 2. Create the `.env` file

Create a file called `.env` in the root of the project with the following content:

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_discord_channel_id
RAR_EXE_PATH=C:\Program Files\WinRAR\rar.exe
SAVE_FOLDER=C:\Users\YourName\AppData\LocalLow\MijuGames\Planet Crafter
DEST_FOLDER=C:\Users\YourName\Desktop\SalvataggiPlanetCrafter
```

> ⚠️ Replace all values with your own:
>
> * `DISCORD_TOKEN`: The token of your Discord bot
> * `DISCORD_CHANNEL_ID`: The ID of the channel where the backups will be sent
> * `RAR_EXE_PATH`: Full path to `rar.exe` from WinRAR
> * `SAVE_FOLDER`: Path to your Planet Crafter save files
> * `DEST_FOLDER`: Path where the bot will save the compressed `.rar` files before uploading

---

### 3. Run the bot

```bash
python main.py
```

The bot will log in, start monitoring the save folder, and upload compressed saves to Discord whenever a change is detected.

---

## 🔄 How it works (code overview)

* **main.py**

  * Loads your settings from `.env`
  * Starts a loop that checks every 10 seconds for changes to the `Standard-1.json` save file
  * If the save is modified, it:

    * Compresses the entire save folder into a `.rar` file
    * Sends the file to your specified Discord channel

* **.env**

  * Used to keep all your sensitive info out of the code
  * You must not upload this file to GitHub (it's already ignored in `.gitignore`)

---

## 🛠️ What to Modify

If you want to customize the project:

| You want to...                                    | Change in...       | Notes                                                                                          |
| ------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| Change the backup interval                        | `main.py`          | Modify the `await asyncio.sleep(10)` line                                                      |
| Change file to monitor (default: Standard-1.json) | `main.py`          | Change the value of `save_file`                                                                |
| Use `.zip` instead of `.rar`                      | `main.py`          | Replace the WinRAR command with `zipfile` or `shutil.make_archive()` (Python standard library) |
| Use a Linux system                                | `.env` + `main.py` | Set `RAR_EXE_PATH` to `rar` if in your `PATH`                                                  |

---

## 🧼 Safety Tips

* Make sure your `.env` is added to `.gitignore`
* Never share your Discord bot token publicly
* Always use a test server when deploying changes

---

## 🧹 Example Output

When the bot detects a change, it will send a message like:

> "Ecco il salvataggio di Planet Crafter:"
> *(attached file: PlanetCrafter\_Saves\_20250527\_173212.rar)*

---

## 🛆 To-Do / Future Ideas

* Add support for `.zip` format for cross-platform use
* Implement backup retention (e.g., keep only last 5 files)
* Add Discord command to trigger backup manually (e.g. `!backup`)
* Add logs to a file

---

## 📜 License

This project is open source and available under the MIT License.
## 🚫 License and Commercial Use

This project is licensed under the **Creative Commons BY-NC 4.0** license.

You are free to share, modify, and use this project **for non-commercial purposes only**, provided you give proper credit.

**Commercial use, redistribution, or selling is not allowed without my explicit permission.**  
If you're interested in using this software commercially or including it in a paid product, please contact me to discuss terms or revenue sharing:

📩 [https://github.com/AndreiBri](https://github.com/AndreiBri)
# Auto-Save-Discord
