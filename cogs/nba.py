"""A Discord.py 2.0 Cog for NBA statistics"""
import requests
from datetime import datetime
import asyncio
import pytz
import discord
import inflect
from discord.ext import commands
from nba_api.stats.endpoints import (
    commonplayerinfo,
    PlayerDashboardByGameSplits,
    leaguestandingsv3,
    leagueleaders,
)
from nba_api.stats.static import players

tz = pytz.timezone("US/Hawaii")

teamalias = {
    "Bucks": ["mil", "sucks"],
    "Bulls": ["chi"],
    "Cavaliers": ["cle", "cavs"],
    "Celtics": ["bos", "Cs", "C's", "selltix"],
    "Clippers": ["lac", "clips", "clipjoint"],
    "Grizzlies": ["mem", "grizz"],
    "Hawks": ["atl", "hotlanta"],
    "Heat": ["mia"],
    "Hornets": ["cha", "whorenets"],
    "Jazz": ["uta", "jizz", "spazz", "azz"],
    "Kings": ["sac"],
    "Knicks": ["nyk", "nix"],
    "Lakers": ["lal", "fakers", "lakeshow", "showtime"],
    "Magic": ["orl", "tragic"],
    "Mavericks": ["dal", "mavs", "fuck luka"],
    "Nets": ["bkn", "njn"],
    "Nuggets": ["den", "nugs"],
    "Pacers": ["ind"],
    "Pelicans": ["nop", "pels", "nollins"],
    "Pistons": ["det", "pissedons", "pissed ons"],
    "Raptors": ["tor", "craptors"],
    "Rockets": ["hou"],
    "Spurs": ["sas"],
    "Suns": ["phx"],
    "Timberwolves": ["min", "minny", "wolves"],
    "Thunder": ["okc", "blunder"],
    "Trail Blazers": ["por", "pdx", "trailblazers"],
    "Warriors": ["gsw", "dubs"],
    "Wizards": ["was", "wiz"],
}

confs = {
    "east": ["Atlantic", "Central", "Southeast"],
    "west": ["Southwest", "Northwest", "Pacific"],
    "eastern": ["Atlantic", "Central", "Southeast"],
    "western": ["Southwest", "Northwest", "Pacific"],
}

statnicks = {
    "GP": ["games played", "gms", "games", "played"],
    "MIN": ["minutes played", "mins", "minutes", "minplayed", "minsplayed"],
    "FGM": ["field goals", "field goals made"],
    "FGA": ["field goals attempted", "attempts", "shots taken", "shots attempted"],
    "FG_PCT": ["field goal %", "fg%", "shooting%"],
    "FG3M": ["3-pointers made", "3pm", "3s", "3's", "threes"],
    "FG3A": ["3-point attempts", "3pa", "chucks"],
    "FG3_PCT": ["3p%", "three point %", "3pt%"],
    "FTM": ["free throws made", "fts"],
    "FTA": ["free throw attempts"],
    "FT_PCT": ["free throw %", "ft%"],
    "OREB": ["offensive rebounds", "offensive boards"],
    "DREB": ["defensive rebounds", "defensive boards"],
    "REB": ["rebounds", "total rebounds", "boards", "glass"],
    "AST": ["assists", "dimes", "ass"],
    "STL": ["steals"],
    "BLK": ["blocks", "blocked shots", "rejections"],
    "TOV": ["turnovers", "giveaways"],
    "PF": ["fouls", "personal fouls"],
    "PTS": ["points", "ppg", "points per game"],
    "EFF": ["efficiency"],
    "ASS_TOV": ["ass:tov", "assists:turnovers", "atr", "a:t"],
    "STL_TOV": ["stl:tov", "steals:turnovers", "str", "s:t"],
}


class nba(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("NBA cog loaded.")

    @discord.app_commands.command(name="scores", description="NBA scores")
    @discord.app_commands.describe(date="Date in YYYY-MM-DD format")
    async def nbascores(self, interaction: discord.Interaction, date: str = ""):
        """Get the NBA scores for the specified date"""
        await interaction.response.defer()
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
            await interaction.followup.send(
                f"{date} is not a valid date. Please use the YYYY-MM-DD format."
            )
        url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={date}&LeagueID=00"
        try:
            r = requests.get(url, headers=headers)
            schedule = r.json()
            assert len(schedule["scoreboard"]["games"]) > 0
        except AssertionError:
            await interaction.followup.send(
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
        # await interaction.channel.typing()
        await interaction.followup.send(str("\n".join(scores)))

    @discord.app_commands.command(name="seasonstats", description="Player season stats")
    @discord.app_commands.describe(playername="An NBA player's name")
    async def nbaseasonstats(self, interaction: discord.Interaction, playername: str):
        # """List an NBA player's cumulative season stats"""
        await interaction.response.defer()
        try:
            player = players.find_players_by_full_name(playername)
            assert len(player) > 0
            player_id = player[0]["id"]
            player_info = commonplayerinfo.CommonPlayerInfo(
                player_id
            ).common_player_info.get_dict()
        except:
            await interaction.followup.send(f"Player not found, {playername}")
        stats = [
            f"Season Stats for {player[0]['full_name']} ({player_info['data'][0][20]})\n"
        ]
        info = PlayerDashboardByGameSplits(
            last_n_games=0,
            month=0,
            opponent_team_id=0,
            pace_adjust="N",
            per_mode_detailed="PerGame",
            period=0,
            player_id=player_id,
            season="2022-23",
        ).get_dict()["resultSets"][0]["rowSet"][0]
        stats.append(
            f"{info[26]} PTS  {info[18]}/{info[16]} RB  {info[19]} AS  {info[22]} BL  {info[21]} ST"
        )
        stats.append(
            f"{str(info[9]).lstrip('0')} of {(info[8])} FG / {str(info[12]).lstrip('0')} of {info[11]} 3P / {str(info[15]).lstrip('0')} of {info[14]} FT"
        )
        stats.append(
            f"{info[20]} TO  {info[24]} PF  {info[27]} +/-  {info[6]} MN  {info[2]} GP"
        )
        print(str("\n".join(stats)))
        await interaction.followup.send(str("\n".join(stats)))

    @discord.app_commands.command(
        name="leaders", description="The top 10 players in a given statistical category"
    )
    @discord.app_commands.describe(
        statistic="A statistical category such as points or rebounds"
    )
    async def nbaleaders(self, interaction: discord.Interaction, statistic: str):
        """List the top 10 players in a given statistical category"""
        await interaction.response.defer()
        for k, v in statnicks.items():
            if statistic.lower() in v:
                statname = k
            elif statistic.upper() == k:
                statname = k
        result = leagueleaders.LeagueLeaders(
            stat_category_abbreviation=statname, per_mode48="PerGame"
        )
        print(result)
        info = result.get_dict()["resultSet"]
        i = info["headers"].index(statname)
        x = [f"League leaders in {statnicks[statname][0]}\n"]
        for player in info["rowSet"]:
            if player[1] <= 10:
                x.append(
                    f"{player[1]} - {player[2]} ({player[4]})  {player[i]} {statname}"
                )
        await interaction.followup.send(str("\n".join(x)))

    @discord.app_commands.command(
        name="record", description="Current W/L record of an NBA team"
    )
    @discord.app_commands.describe(teamname="The name of an NBA team")
    async def nbarecord(self, interaction: discord.Interaction, teamname: str):
        await interaction.response.defer()
        """Pull the current W/L record of the specified team"""
        result = leaguestandingsv3.LeagueStandingsV3()
        standings = result.get_dict()["resultSets"][0]["rowSet"]
        p = inflect.engine()
        for k, v in teamalias.items():
            if teamname.lower() in v:
                teamname = k
        for team in standings:
            if teamname.capitalize() in team:
                x = f"{team[3]} {team[4]}\nRecord: {team[13]}-{team[14]} ({('%.3f' %team[15]).lstrip('0')})\n{p.ordinal(team[12])} in the {team[10]} Division.\n{p.ordinal(team[8])} in the {team[6]}ern Conference.\n{team[7].strip()} vs. the {team[6]}ern Conference.\n{team[11].strip()} vs. the {team[10]} Division."
                [team[13], team[14], team[15], team[10], team[12], team[13]]
        await interaction.followup.send(x)


async def setup(bot):
    await bot.add_cog(nba(bot))
