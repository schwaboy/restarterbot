import requests
from datetime import datetime
import pytz


def getscores():
    headers = {
        "Host": "stats.nba.com",
        "User-Agent": "JerrySloan/0.1.0",
        "Accept": "application,json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Origin": "https://www.nba.com/",
        "Referer": "https://www.nba.com/",
    }

    tz = pytz.timezone("US/Hawaii")
    url = f"https://stats.nba.com/stats/scoreboardv3?GameDate={datetime.now(tz).strftime('%Y-%m-%d')}&LeagueID=00"
    r = requests.get(url, headers=headers)
    schedule = r.json()

    scores = []
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
            # print(game)
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
    return scores


print(getscores())
