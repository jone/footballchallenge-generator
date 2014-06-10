from operator import itemgetter
from wm2012 import data
from wm2012 import ranking
from wm2012 import stats
from wm2012 import validators


POSITIONS = (
    ('Sturm', 2),
    ('Torh\xc3\xbcter', 1),
    ('Mittelfeld', 5),
    ('Verteidigung', 3))


def command():
    ranking.calculate_score_multiplier(data.GROUPS)
    ranking.apply_score_multiplier(data.TEAMS.values())
    players = ranking.players_by_score(data.TEAMS.values())
    positions = ranking.group_players_by_position(players)
    first_team, second_team = assign_players(positions)
    print 'DONE'
    print ''

    print 'First Team:'
    print_team(first_team)

    print 'Second Team:'
    print_team(second_team)

    print 'Total Nations:', len(set(map(itemgetter('team_id'),
                                      first_team + second_team)))
    print_nations(first_team, second_team)
    print 'Player score sum:', stats.player_score_sum(first_team, second_team)
    print 'Player market value:', stats.player_market_values(first_team, second_team)
    print 'Total match score:', stats.match_score(first_team, second_team)



def assign_players(positions):
    print 'Assigning players'
    first_team = []
    second_team = []

    for position, amount in POSITIONS:
        for _ in range(amount):
            for player in positions[position]:
                if player in first_team or player in second_team:
                    continue

                if validators.adding_player_to_first_team_allowed(player,
                                                                  first_team,
                                                                  second_team):
                    first_team.append(player)
                    break

    for position, amount in POSITIONS:
        for _ in range(amount):
            for player in positions[position]:
                if player in first_team or player in second_team:
                    continue

                if validators.adding_player_to_second_team_allowed(player,
                                                                   first_team,
                                                                   second_team):
                    second_team.append(player)
                    break

    return first_team, second_team


def print_team(players):
    for player in players:
        team = data.TEAMS[player['team_id']]
        print player['Position'].rjust(20), ':', player['Name'], '({} -> {})'.format(
            team['Nation'],
            ranking.REVERSE_SCORE_MULTIPLIER[team['score_multiplier']])
    print 'Players:', len(players)
    print 'Teams:', len(set(map(itemgetter('team_id'), players)))
    print ''


def print_nations(first_players, second_players):
    first_nations = map(itemgetter('Nation'),
                        map(data.TEAMS.get,
                            map(itemgetter('team_id'), first_players)))
    second_nations = map(itemgetter('Nation'),
                        map(data.TEAMS.get,
                            map(itemgetter('team_id'), second_players)))

    all_nations = first_nations + second_nations
    all_nations = dict(map(
            lambda nation: (
                nation, len(filter(lambda x: x==nation, all_nations))),
            all_nations))

    print 'Nations:'
    for nation, amount in sorted(all_nations.items(), key=lambda x: x[1],
                                 reverse=True):
        print ' - {}: {} ({} / {})'.format(
            nation,
            amount,
            len(filter(lambda x: x==nation, first_nations)),
            len(filter(lambda x: x==nation, second_nations)))
