from operator import itemgetter
from wm2012 import data


def humanize(num):
    for x in ['','K','M','G']:
        if num < 1000.0 and num > -1000.0:
            return "%3.1f%s" % (num, x)
        num /= 1000.0
    return "%3.1f%s" % (num, 'T')


def player_score_sum(first_team, second_team):
    first_scores = sum(map(itemgetter('score'), first_team)) * 2
    second_scores = sum(map(itemgetter('score'), second_team))
    total = sum((first_scores, second_scores))
    return '{} ({})'.format(total, humanize(total))


def player_market_values(first_team, second_team):
    first = sum(map(itemgetter('Marktwert'), first_team)) * 2
    second = sum(map(itemgetter('Marktwert'), second_team))
    total = sum((first, second))
    return '{} ({})'.format(total, humanize(total))



def match_score(first_team, second_team):
    total = 0

    for player in first_team:
        team = data.TEAMS[player['team_id']]
        total += team['stats']['wins'] * 4
        total -= team['stats']['wins'] * 2

    for player in second_team:
        team = data.TEAMS[player['team_id']]
        total += team['stats']['losses'] * 2
        total -= team['stats']['losses'] * 1

    return total
