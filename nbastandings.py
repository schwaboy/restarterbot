#!python3

from nba_api.stats.endpoints import leaguestandingsv3
import inflect
import aliases

result = leaguestandingsv3.LeagueStandingsV3()
standings = result.get_dict()["resultSets"][0]["rowSet"]
confs = {
    "east": ["Atlantic", "Central", "Southeast"],
    "west": ["Southwest", "Northwest", "Pacific"],
    "eastern": ["Atlantic", "Central", "Southeast"],
    "western": ["Southwest", "Northwest", "Pacific"],
}


def playoffs(conference) -> str:
    teams = []
    count = 1
    for team in standings:
        if team[10] in confs[conference.lower()]:
            teams.append(team)
    x = []
    for team in teams:
        x.append(
            f"{count} - {team[3]} {team[4]} {team[17]} ("
            + ("%.3f" % team[15]).lstrip("0")
            + ")"
        )
        count += 1
        if count >= 9:
            break
    return x


def lottery():
    standings.sort(reverse=True, key=lambda x: x[15])
    x = []
    count = 15
    for team in standings:
        if team[8] > 8:
            count -= 1
            x.insert(
                0,
                f"{count} - {team[3]} {team[4]}  {team[17]}  ("
                + ("%.3f" % team[15]).lstrip("0")
                + ")",
            )
    return x


# def lottery(conference) -> str:
#     teams = []
#     count = 1
#     for k, v in aliases.teamalias.items():
#         if teamname in v:
#             teamname = k
#     for team in standings["resultSets"][0]["rowSet"]:
#         if team[10] in confs[conference.lower()]:
#             teams.append(team)
#     x = []
#     for team in teams:
#         if count < 9:
#             count += 1
#             continue
#         x.append(
#             f"{count} - {team[3]} {team[4]} {team[17]} ("
#             + ("%.3f" % team[15]).lstrip("0")
#             + ")"
#         )
#         count += 1
#     return x


def streak(teamname) -> str:
    for k, v in aliases.teamalias.items():
        if teamname.lower() in v:
            teamname = k
    for team in standings:
        if teamname.capitalize() in team:
            x = f"{team[3]} {team[4]}\nCurrent streak: {team[37]}\nLast 10 games: {team[20]}"
    return x


def record(teamname) -> str:
    p = inflect.engine()
    for k, v in aliases.teamalias.items():
        if teamname.lower() in v:
            teamname = k
    for team in standings:
        if teamname.capitalize() in team:
            x = f"{team[3]} {team[4]}\nRecord: {team[13]}-{team[14]} ({('%.3f' %team[15]).lstrip('0')})\n{p.ordinal(team[12])} in the {team[10]} Division.\n{p.ordinal(team[8])} in the {team[6]}ern Conference.\n{team[7].strip()} vs. the {team[6]}ern Conference.\n{team[11].strip()} vs. the {team[10]} Division."
            [team[13], team[14], team[15], team[10], team[12], team[13]]
    return x
