from wm2012 import data
from wm2012 import ranking
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
    # for player in players:
    #     print ' - '.join((str(player['score']).ljust(10),
    #                     player['Name'],
    #                     player['Position'],
    #                     data.TEAMS[player['team_id']]['Nation']))

    positions = ranking.group_players_by_position(players)
    first_team, second_team = assign_players(positions)
    print 'DONE'
    print ''

    print 'First Team:'
    print_team(first_team)

    print 'Second Team:'
    print_team(second_team)



def assign_players(positions):
    print 'Assigning players'
    first_team = []
    second_team = []

    print '... first team'
    for position, amount in POSITIONS:
        for _ in range(amount):
            print '1.', position
            for player in positions[position]:
                if player in first_team or player in second_team:
                    continue

                if validators.adding_player_to_first_team_allowed(player,
                                                                      first_team,
                                                                      second_team):
                    first_team.append(player)
                    break

    print '... second team'
    for position, amount in POSITIONS:
        for _ in range(amount):
            print '2.', position
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
