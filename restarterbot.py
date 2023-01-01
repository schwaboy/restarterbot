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
import nbastandings
import nbaleaders
import nbaseasonstats
import aliases
from datetime import datetime
import pytz


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
# bot = discord.bot()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
logging.basicConfig(filename="thebot.log", filemode="a", level=logging.DEBUG)


async def load():
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


# @bot.tree.command(name="scores", description="NBA scores")
# @discord.app_commands.describe(date="Date in YYYY-MM-DD format")
# async def scores(interaction: discord.Interaction, date: str = ""):
#     await interaction.response.send_message(str("\n".join(nbascores.getscores(date))))
# try:
#     datetime.strptime(date, "%Y-%m-%d")
# except ValueError:
#     await interaction.response.send_message(
#         f"Sorry {interaction.user.mention}, {date} is not a valid date. Please use the YYYY-MM-DD format."
#     )
#     return
# try:
#     r = nbascores.getscores(date)
#     assert r
# except AssertionError:
#     await interaction.response.send_message(
#         f"There are no games scheduled on {date}, {interaction.user.mention}"
#     )
# else:
#     await interaction.response.send_message(
#         f"NBA scores for {date}\n\n" + str("\n".join(r))
#     )


@bot.tree.command(name="standings", description="NBA standings by conference")
async def standings(interaction: discord.Interaction, conference: str):
    await interaction.response.send_message(
        str("\n".join(nbastandings.playoffs(conference)))
    )


@bot.tree.command(name="stfu", description="Shut the fuck up")
@discord.app_commands.describe(user="The user you want to shut the fuck up")
async def stfu(interaction: discord.Interaction, user: str):
    await interaction.response.send_message(f"Shut the fuck up, {user}")


@bot.tree.command(name="lottery", description="Lottery teams")
async def standings(interaction: discord.Interaction):
    await interaction.response.send_message(str("\n".join(nbastandings.lottery())))


@bot.tree.command(name="streak", description="W/L streak of an NBA team")
async def standings(interaction: discord.Interaction, teamname: str):
    await interaction.response.send_message(nbastandings.streak(teamname))


# @bot.tree.command(name="record", description="Current W/L record of an NBA team")
# async def standings(interaction: discord.Interaction, teamname: str):
#     await interaction.response.send_message(nbastandings.record(teamname))


# @bot.tree.command(
#     name="leaders", description="The top 10 players in a given statistical category"
# )
# @discord.app_commands.describe(
#     statistic="A statistical category such as points or rebounds"
# )
# async def standings(interaction: discord.Interaction, statistic: str):
#     await interaction.response.send_message(
#         str("\n".join(nbaleaders.leaders(statistic)))
#     )


# @bot.tree.command(name="seasonstats", description="Player season stats")
# @discord.app_commands.describe(playername="An NBA player's name")
# async def seasonstats(interaction: discord.Interaction, playername: str):
#     await interaction.channel.typing()
#     await interaction.response.send_message(
#         str("\n".join(nbaseasonstats.seasonstats(playername)))
#     )


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
