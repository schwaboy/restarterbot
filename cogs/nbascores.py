"""A module to pull the NBA scores for a specified date"""
import requests
from datetime import datetime
import pytz
import discord
from discord.ext import commands

tz = pytz.timezone("US/Hawaii")


class nba(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("NBA cog loaded.")

    @discord.app_commands.command(name="scores")
    @discord.app_commands.describe(date="Date in YYYY-MM-DD format")
    async def nbascores(self, interaction: discord.Interaction, date: str = ""):
        """Get the NBA scores for the specified date"""
        headers = {
            "Host": "stats.nba.com",
            "User-Agent": "JerrySloan/0.1.0",
            "Accept": "application,json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "close",
            "Origin": "https://www.nba.com/",
            "Referer": "https://www.nba.com/",
        }
        if not date:
            date = datetime.now(pytz.timezone("US/Hawaii")).strftime("%Y-%m-%d")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message(
                f"{date} is not a valid date. Please use the YYYY-MM-DD format."
            )
        url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date}&LeagueID=00"
        try:
            r = requests.get(url, headers=headers)
            schedule = r.json()
            assert len(schedule["scoreboard"]["games"]) > 0
        except AssertionError:
            await interaction.response.send_message(
                f"Sorry, {interaction.user.mention}. There are no games scheduled on {date}"
            )
        else:
            scores = [f"NBA scores for {date}\n\n"]

        for game in schedule["scoreboard"]["games"]:
            if game["gameStatus"] == 1:
                scores.append(
                    str(
                        (
                            game["homeTeam"]["teamName"]
                            + " vs "
                            + game["awayTeam"]["teamName"]
                            + "  "
                            + game["gameStatusText"]
                        )
                    )
                )
            else:
                scores.append(
                    str(
                        (
                            game["homeTeam"]["teamName"]
                            + " "
                            + str(game["homeTeam"]["score"])
                            + " "
                            + game["awayTeam"]["teamName"]
                            + " "
                            + str(game["awayTeam"]["score"])
                        )
                    )
                    + " "
                )
                if "Qtr" in game["gameStatusText"]:
                    scores[-1] = str(
                        scores[-1]
                        + str(
                            (
                                str(game["gameClock"]).strip()
                                + "  "
                                + str(game["gameStatusText"].strip())
                            )
                        )
                    )
                else:
                    scores[-1] = str(scores[-1] + "  " + str((game["gameStatusText"])))
        await interaction.response.send_message(str("\n".join(scores)))


async def setup(bot):
    await bot.add_cog(nba(bot))


# def getscores(date):
#     """Get the NBA scores for the specified date"""
#     headers = {
#         "Host": "stats.nba.com",
#         "User-Agent": "JerrySloan/0.1.0",
#         "Accept": "application,json, text/plain, */*",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Connection": "close",
#         "Origin": "https://www.nba.com/",
#         "Referer": "https://www.nba.com/",
#     }
#     if not date:
#         date = datetime.now(pytz.timezone("US/Hawaii")).strftime("%Y-%m-%d")
#     try:
#         datetime.strptime(date, "%Y-%m-%d")
#     except ValueError as v:
#         v = [f"{date} is not a valid date. Please use the YYYY-MM-DD format."]
#         return v
#     url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date}&LeagueID=00"
#     try:
#         r = requests.get(url, headers=headers)
#         schedule = r.json()
#         assert len(schedule["scoreboard"]["games"]) > 0
#     except AssertionError as a:
#         a = {f"There are no games scheduled on {date}"}
#         return a
#     else:
#         scores = [f"NBA scores for {date}\n\n"]

#     for game in schedule["scoreboard"]["games"]:
#         if game["gameStatus"] == 1:
#             scores.append(
#                 str(
#                     (
#                         game["homeTeam"]["teamName"]
#                         + " vs "
#                         + game["awayTeam"]["teamName"]
#                         + "  "
#                         + game["gameStatusText"]
#                     )
#                 )
#             )
#         else:
#             scores.append(
#                 str(
#                     (
#                         game["homeTeam"]["teamName"]
#                         + " "
#                         + str(game["homeTeam"]["score"])
#                         + " "
#                         + game["awayTeam"]["teamName"]
#                         + " "
#                         + str(game["awayTeam"]["score"])
#                     )
#                 )
#                 + " "
#             )
#             if "Qtr" in game["gameStatusText"]:
#                 scores[-1] = str(
#                     scores[-1]
#                     + str(
#                         (
#                             str(game["gameClock"]).strip()
#                             + "  "
#                             + str(game["gameStatusText"].strip())
#                         )
#                     )
#                 )
#             else:
#                 scores[-1] = str(scores[-1] + "  " + str((game["gameStatusText"])))
#     return scores


# z = getscores("2022-12-22")
# for q in z:
#     print(q)
