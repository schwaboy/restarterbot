#!python3

from nba_api.stats.endpoints import leaguestandingsv3

result = leaguestandingsv3.LeagueStandingsV3()
standings = result.get_dict()
confs = {
    "east": ["Atlantic", "Central", "Southeast"],
    "west": ["Southwest", "Northwest", "Pacific"],
}


def playoffs(conference) -> str:
    teams = []
    count = 1
    for team in standings["resultSets"][0]["rowSet"]:
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


def lottery(conference) -> str:
    teams = []
    count = 1
    for team in standings["resultSets"][0]["rowSet"]:
        if team[10] in confs[conference.lower()]:
            teams.append(team)
    x = []
    for team in teams:
        if count < 9:
            count += 1
            continue
        x.append(
            f"{count} - {team[3]} {team[4]} {team[17]} ("
            + ("%.3f" % team[15]).lstrip("0")
            + ")"
        )
        count += 1
    return x
