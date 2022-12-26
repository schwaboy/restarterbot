#! python3
"""A Discord bot that restarts a container via Portainer."""

import os
import logging
from dotenv import load_dotenv
import requests
import discord
from discord.ext import commands
import nbascores
import nbastandings
import aliases
from datetime import datetime
import pytz

tz = pytz.timezone("US/Hawaii")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# client = discord.Client()
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
logging.basicConfig(filename="thebot.log", filemode="a", level=logging.DEBUG)


def restart_container():
    """Restart a Docker container using the Portainer API."""
    portainer_pass = os.getenv("PORTAINER_PASS")
    portainer_user = os.getenv("PORTAINER_USER")
    portainer_url = os.getenv("PORTAINER_URL")
    portainer_login = {"password": portainer_pass, "username": portainer_user}

    auth_response = requests.post(f"{portainer_url}/auth", json=(portainer_login))
    d = auth_response.json()
    portainer_token = d["jwt"]
    headers = {"Authorization": "Bearer " + portainer_token}

    restart_response = requests.post(
        f"{portainer_url}/endpoints/1/docker/containers/{os.getenv('CONTAINER_ID')}/restart",
        headers=headers,
    )
    return restart_response.status_code


@client.event
async def on_ready():
    """Display login confirmation message."""
    print("We have logged in as {0.user}".format(client))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@client.tree.command(name="scores", description="NBA scores")
@discord.app_commands.describe(date="Date in YYYY-MM-DD format")
async def scores(
    interaction: discord.Interaction, date: str = datetime.now(tz).strftime("%Y-%m-%d")
):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await interaction.response.send_message(
            f"Sorry {interaction.user.mention}, {date} is not a valid date. Please use the YYYY-MM-DD format."
        )
        return
    try:
        r = nbascores.getscores(date)
        assert r
    except AssertionError:
        await interaction.response.send_message(
            f"There are no games scheduled on {date}, {interaction.user.mention}"
        )
    else:
        await interaction.response.send_message(str("\n".join(r)))


@client.tree.command(name="standings", description="NBA standings by conference")
async def standings(interaction: discord.Interaction, conference: str):
    await interaction.response.send_message(
        str("\n".join(nbastandings.playoffs(conference)))
    )


@client.tree.command(name="stfu", description="Shut the fuck up")
@discord.app_commands.describe(user="The user you want to shut the fuck up")
async def stfu(interaction: discord.Interaction, user: str):
    await interaction.response.send_message(f"Shut the fuck up, {user}")


@client.tree.command(name="lottery", description="Lottery teams")
async def standings(interaction: discord.Interaction, conference: str):
    await interaction.response.send_message(
        str("\n".join(nbastandings.lottery(conference)))
    )


@client.tree.command(name="streak", description="W/L streak of an NBA team")
async def standings(interaction: discord.Interaction, teamname: str):
    await interaction.response.send_message(nbastandings.streak(teamname))


@client.tree.command(name="record", description="Current W/L record of an NBA team")
async def standings(interaction: discord.Interaction, teamname: str):
    await interaction.response.send_message(nbastandings.record(teamname))


@client.event
async def on_message(message):
    """Display login confirmation message."""
    if message.author == client.user:
        return
    elif message.content.lower().startswith("greetings"):
        channel = message.channel
        await channel.send("Hello {.author.display_name}!".format(message))
    elif message.content.endswith(os.getenv("DISCORD_TEST_TRIGGER")):
        channel = message.channel
        await channel.send(os.getenv("DISCORD_TEST_RESPONSE"))
    elif message.content == os.getenv("RESTART_TRIGGER"):
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


client.run(TOKEN)
