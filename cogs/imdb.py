import os
import discord
from omdb import OMDBClient
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
apikey = os.getenv("IMDB_API_KEY")

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

async def setup(bot):
    await bot.add_cog(imdb(bot))
