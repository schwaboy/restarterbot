"""A module to pull an NBA player's cumulative season statistics"""
import aliases
from nba_api.stats.endpoints import commonplayerinfo, PlayerDashboardByGameSplits
from nba_api.stats.static import players


def seasonstats(playername) -> str:
    """List an NBA player's cumulative season stats"""
    try:
        player = players.find_players_by_full_name(playername)
        assert len(player) > 0
        player_id = player[0]["id"]
        player_info = commonplayerinfo.CommonPlayerInfo(
            player_id
        ).common_player_info.get_dict()
    except:
        errormessage = [f"Player not found, {playername}"]
        return errormessage
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
    return stats
