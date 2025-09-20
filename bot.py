import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Charger le token depuis .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Vérifier que le token est défini
if not TOKEN:
    print("❌ ERREUR : Token Discord non trouvé. Veuillez configurer DISCORD_TOKEN dans les secrets Replit.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"📝 {len(synced)} commandes slash synchronisées avec succès")
    except discord.HTTPException as e:
        if e.code == 50240:
            print("⚠️ Note: Une commande Entry Point existe déjà. Le bot fonctionne normalement.")
        else:
            print(f"⚠️ Erreur HTTP lors de la synchronisation: {e}")
    except Exception as e:
        print(f"⚠️ Erreur lors de la synchronisation des commandes: {e}")
    
    print("🤖 Bot prêt à recevoir les commandes!")

# Slash command /dm avec mentions multiples
@bot.tree.command(name="dm", description="Envoyer un message privé à plusieurs utilisateurs")
@app_commands.describe(
    mentions="Mentionne plusieurs utilisateurs séparés par des espaces",
    message="Le message à envoyer"
)
async def dm(interaction: discord.Interaction, mentions: str, message: str):
    await interaction.response.defer(ephemeral=True)
    success, failed = [], []

    for mention in mentions.split(" "):
        # Vérifier que c'est une mention
        if mention.startswith("<@") and mention.endswith(">"):
            try:
                user_id = int(mention.replace("<@", "").replace(">", "").replace("!", ""))
                user = await bot.fetch_user(user_id)
                await user.send(message)
                success.append(user.name)
            except Exception:
                failed.append(mention)

    response = ""
    if success:
        response += f"📩 Message envoyé à : {', '.join(success)}\n"
    if failed:
        response += f"⚠️ Impossible d’envoyer à : {', '.join(failed)}"

    await interaction.followup.send(response or "❌ Aucun utilisateur trouvé.", ephemeral=True)

bot.run(TOKEN)

