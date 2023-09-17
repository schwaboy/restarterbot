import os
import discord
import requests
from omdb import OMDBClient
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
apikey = os.getenv("IMDB_API_KEY")
dictkey = os.getenv("DICTIONARY_API_KEY")
theskey = os.getenv("THESAURUS_API_KEY")
client=OMDBClient(apikey=apikey)


class imdb(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("imdb cog loaded.")

    @discord.app_commands.command(name="imdb", description="Get info about a movie or TV show")
    @discord.app_commands.describe(title="A movie or TV show")
    async def imdb(self, interaction: discord.Interaction, title: str = ""):
        if title == "":
            await interaction.response.send_message("Please provide a title", ephemeral=True)
            return
        try:
            result = client.search(title)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
            return
        if result is None:
            await interaction.response.send_message("No results found", ephemeral=True)
            return
        imdbid = result[0]['imdb_id']
        movie = client.imdbid(imdbid)
        embed = discord.Embed(title=movie["title"], description=movie["plot"], color=0x00ff00)
        embed.set_thumbnail(url=movie["poster"])
        embed.add_field(name="Year", value=movie["year"], inline=True)
        embed.add_field(name="Rated", value=movie["rated"], inline=True)
        embed.add_field(name="Runtime", value=movie["runtime"], inline=True)
        embed.add_field(name="Genre", value=movie["genre"], inline=True)
        embed.add_field(name="Director", value=movie["director"], inline=True)
        embed.add_field(name="Writer", value=movie["writer"], inline=True)
        embed.add_field(name="Actors", value=movie["actors"], inline=True)
        embed.add_field(name="Awards", value=movie["awards"], inline=True)
        embed.add_field(name="IMDb Rating", value=movie["imdb_rating"], inline=True)
        embed.add_field(name="IMDb Votes", value=movie["imdb_votes"], inline=True)
        embed.add_field(name="Metascore", value=movie["metascore"], inline=True)
        embed.add_field(name="Type", value=movie["type"], inline=True)
        embed.add_field(name="Box Office", value=movie["box_office"], inline=True)
        embed.add_field(name="Production", value=movie["production"], inline=True)
        embed.add_field(name="Website", value=movie["website"], inline=True)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="dict", description="Get the dictionary definition of a word")
    @discord.app_commands.describe(word="Word")
    async def dictionary(self, interaction: discord.Interaction, word: str = ""):
        """Return the dictionary definition of a word"""
        await interaction.response.defer()
        url = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={dictkey}'
        response = requests.get(url)
        definition = response.json()
        if definition:
            await interaction.followup.send(f"{word} ({definition[0]['fl']}) - {definition[0]['hwi']['prs'][0]['mw']}\n{definition[0]['shortdef'][0]}")
        else:
            await interaction.followup.send(f"{word} is not a word.")

    @discord.app_commands.command(name="thes", description="Get similar words")
    @discord.app_commands.describe(word="Word")
    async def thes(self, interaction: discord.Interaction, word: str = ""):
        """Return similar words"""
        await interaction.response.defer()
        url = f'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={theskey}'
        response = requests.get(url)
        definition = response.json()
        try:
            await interaction.followup.send(f"{word} ({definition[0]['fl']})\n{', '.join(definition[0]['meta']['syns'][0][:])}")
        except TypeError:
            await interaction.followup.send(f"No synonyms found for \"{word}\".")

async def setup(bot):
    await bot.add_cog(imdb(bot))
