from operator import itemgetter
from wm2012.fetch import recursive_encode
from wm2012.paths import GROUPS_PATH
from wm2012.paths import TEAMS_PATH
import json


def load(path):
    with open(path) as file_:
        return recursive_encode(json.load(file_))

def teams():
    teams = load(TEAMS_PATH)
    for team_id, team in teams.items():
        for player in team['players']:
            player['team_id'] = team_id
    return teams

TEAMS = teams()
TEAMS_BY_NATION = dict(map(lambda team: (team['Nation'], team), TEAMS.values()))


def groups():
    groups = {}
    for group_name, teams in load(GROUPS_PATH).items():
        groups[group_name] = sorted(map(TEAMS_BY_NATION.__getitem__, teams),
                                    key=itemgetter('FIFA Rang'))

    return groups


GROUPS = groups()
