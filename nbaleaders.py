"""A module to pull NBA league leaders in a given statistical cateogry"""

import aliases
from nba_api.stats.endpoints import leagueleaders


def leaders(statname) -> str:
    """List the top 10 players in a given statistical category"""
    for k, v in aliases.statnicks.items():
        if statname.lower() in v:
            statname = k
        elif statname.upper() == k:
            statname = k
    result = leagueleaders.LeagueLeaders(
        stat_category_abbreviation=statname, per_mode48="PerGame"
    )
    info = result.get_dict()["resultSet"]
    i = info["headers"].index(statname)
    x = [f"League leaders in {aliases.statnicks[statname][0]}\n"]
    for player in info["rowSet"]:
        if player[1] <= 10:
            x.append(f"{player[1]} - {player[2]} ({player[4]})  {player[i]} {statname}")
    return x
