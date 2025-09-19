import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Charger le token depuis .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user} (slash commands activées)")

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
