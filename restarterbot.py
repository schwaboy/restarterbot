#! python3
"""A Discord bot that restarts a container via Portainer."""

import os
import logging
import asyncio
from dotenv import load_dotenv
import requests
import discord
from discord.ext import commands
import cogs.nba as nba


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
logging.basicConfig(filename="thebot.log", filemode="a", level=logging.DEBUG)


async def load():
    """Load all cogs"""
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    """Display login confirmation message."""
    print("We have logged in as {0.user}".format(bot))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


def restart_container():
    """Restart a Docker container using the Portainer API."""
    portainer_pass = os.getenv("PORTAINER_PASS")
    portainer_user = os.getenv("PORTAINER_USER")
    portainer_url = os.getenv("PORTAINER_URL")
    portainer_login = {"password": portainer_pass, "username": portainer_user}

    auth_response = requests.post(f"{portainer_url}/api/auth", json=(portainer_login))
    d = auth_response.json()
    portainer_token = d["jwt"]
    headers = {"Authorization": "Bearer " + portainer_token}

    restart_response = requests.post(
        f"{portainer_url}/api/endpoints/1/docker/containers/{os.getenv('CONTAINER_ID')}/restart",
        headers=headers,
    )
    return restart_response.status_code


@bot.tree.command(name="stfu", description="Shut the fuck up")
@discord.app_commands.describe(user="The user you want to shut the fuck up")
async def stfu(interaction: discord.Interaction, user: str):
    await interaction.response.send_message(f"Shut the fuck up, {user}")


@bot.event
async def on_message(message):
    """Display login confirmation message."""
    if message.author == bot.user:
        return
    elif message.content.lower().startswith("greetings"):
        channel = message.channel
        await channel.send("Hello {.author.display_name}!".format(message))
    elif message.content.endswith(os.getenv("DISCORD_TEST_TRIGGER")):
        channel = message.channel
        await channel.send(os.getenv("DISCORD_TEST_RESPONSE"))
    elif message.content.lower() == os.getenv("RESTART_TRIGGER"):
        channel = message.channel
        status = restart_container()
        if status == 204:
            await channel.send(
                "Restarting the bot at the request of {.author.display_name}.".format(
                    message
                )
            )
        else:
            await channel.send("Failed to restart the bot. Error code: " + status)


async def main():
    await load()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
