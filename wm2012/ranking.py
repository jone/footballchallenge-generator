from collections import defaultdict
from operator import itemgetter
from pprint import pprint
from wm2012.stats import humanize
import itertools


SCORE_MULTIPLIER = {
    'group_loosers': 0.1,
    'eight_loosers': 0.1,
    'quarter_loosers': 0.1,
    'semi_loosers': 0.1,
    'final_looser': 0.1,
    'winner': 0.1}

# SCORE_MULTIPLIER = {
#     'group_loosers': 1.0,
#     'eight_loosers': 1.2,
#     'quarter_loosers': 1.4,
#     'semi_loosers': 1.7,
#     'final_looser': 2.1,
#     'winner': 2.5}


# SCORE_MULTIPLIER = {
#     'group_loosers': 1.0,
#     'eight_loosers': 1.1,
#     'quarter_loosers': 1.4,
#     'semi_loosers': 1.8,
#     'final_looser': 2.0,
#     'winner': 3.0}


# SCORE_MULTIPLIER = {
#     'group_loosers': 1.0,
#     'eight_loosers': 1.5,
#     'quarter_loosers': 2.0,
#     'semi_loosers': 3.0,
#     'final_looser': 4.0,
#     'winner': 5.0}


REVERSE_SCORE_MULTIPLIER = dict(zip(*reversed(zip(*SCORE_MULTIPLIER.items()))))


def calculate_score_multiplier(groups):
    print 'Ranking: calculating score multiplier'
    group_results = _calculate_group_results(groups)
    eight_final_results = _calculate_eight_final_results(group_results)
    quarter_final_results = _calculate_quarter_final_results(eight_final_results)
    semi_final_results = _calculate_semi_final_results(quarter_final_results)
    winner = _calculate_final_results(semi_final_results)
    print 'WINNER', winner['Nation']
    print ''


def apply_score_multiplier(teams):
    print 'Ranking: Applying score multiplier to players.'

    for pos, team in enumerate(sorted(teams,
                                      key=itemgetter('score_multiplier'),
                                      reverse=True)):
        team_market_value = sum(map(itemgetter('Marktwert'), team['players']))
        print '#{}'.format(pos+1).rjust(3), \
            team['Nation'].decode('utf-8').rjust(20, '.'), \
            '#{}'.format(str(team['FIFA Rang'])).ljust(3), \
            '..', \
            '{}$ ({}$)'.format(team_market_value,
                               humanize(team_market_value)).rjust(20, '.'), \
            ' -> ', \
            team['score_multiplier'], \
            REVERSE_SCORE_MULTIPLIER[team['score_multiplier']]

        for player in team['players']:
            _calculate_player_score(player, team)


def players_by_score(teams):
    print 'Ranking: sort players by score'
    players = reduce(list.__add__, map(itemgetter('players'), teams))
    return sorted(players, key=itemgetter('score'), reverse=True)


def group_players_by_position(players):
    print 'Ranking: gorup players by position'
    positions = defaultdict(list)
    for player in players:
        positions[player['Position']].append(player)
    return dict(positions)


def _calculate_group_results(groups):
    print '.. calculating group results'
    results = {}

    for group_name, teams in groups.items():
        assert len(teams) == 4
        # print 'Group', group_name
        group_results = dict(zip(map(itemgetter('ID'), teams), [0] * len(teams)))

        for team_a, team_b in itertools.combinations(teams, 2):
            winner = _winner_of(team_a, team_b, SCORE_MULTIPLIER['group_loosers'])
            group_results[winner['ID']] += 1

        results[group_name] = sorted(teams,
                                     key=lambda team: group_results[team['ID']],
                                     reverse=True)

    return results


def _calculate_eight_final_results(group_results):
    print '.. calculating eight final results'

    def play(team1, team2):
        return _winner_of(
            team1, team2,
            looser_score_multiplier=SCORE_MULTIPLIER['eight_loosers'])

    A = group_results['A']
    B = group_results['B']
    C = group_results['C']
    D = group_results['D']
    E = group_results['E']
    F = group_results['F']

    thirds = [group[2] for group in group_results.values()]
    best_thirds = sorted(thirds, cmp=_compare_winner_teams)[:4]

    for one, two, three, four in itertools.combinations(best_thirds, 4):
        if (one in B or
            two in D or
            three in A or
            four in C):
            continue

        return {'e1': play(A[1], C[2]),
                'e2': play(B[0], one),
                'e3': play(D[0], two),
                'e4': play(A[0], three),
                'e5': play(C[0], four),
                'e6': play(F[0], E[1]),
                'e7': play(E[0], D[1]),
                'e8': play(B[1], F[1])}


def _calculate_quarter_final_results(eight_final_results):
    print '.. calculating quarter final results'

    games = (('e1', 'e2'),
             ('e3', 'e4'),
             ('e5', 'e6'),
             ('e7', 'e8'))

    results = []

    for team_a_name, team_b_name in games:
        team_a = eight_final_results[team_a_name]
        team_b = eight_final_results[team_b_name]
        winner = _winner_of(
            team_a, team_b,
            looser_score_multiplier=SCORE_MULTIPLIER['quarter_loosers'])
        results.append(winner)

    return results


def _calculate_semi_final_results(quarter_final_results):
    print '.. calculating semi final results'
    games = (quarter_final_results[0:2],
             quarter_final_results[2:4])
    results = []

    for team_a, team_b in games:
        winner = _winner_of(
            team_a, team_b,
            looser_score_multiplier=SCORE_MULTIPLIER['semi_loosers'])
        results.append(winner)

    return results


def _calculate_final_results(semi_final_results):
    print '.. calculating final results'
    team_a, team_b = semi_final_results
    winner = _winner_of(
        team_a, team_b,
        looser_score_multiplier=SCORE_MULTIPLIER['final_looser'])
    winner['score_multiplier'] = SCORE_MULTIPLIER['winner']
    return winner



def _match(team_a, team_b, looser_score_multiplier):
    winner, looser = sorted((team_a, team_b), _compare_winner_teams)
    winner['stats']['wins'] += 1
    looser['stats']['losses'] += 1
    looser['score_multiplier'] = looser_score_multiplier
    return winner, looser


def _compare_winner_teams(*teams):
    for team in teams:
        if 'stats' not in team:
            team['stats'] = {'wins': 0,
                             'losses': 0}

    # Marktwert
    # return cmp(*tuple(sum(map(itemgetter('Marktwert'), team['players']))
    #                   for team in reversed(teams)))

    # FIFA Rang
    return cmp(*map(itemgetter('FIFA Rang'), teams))


def _winner_of(team_a, team_b, looser_score_multiplier):
    return _match(team_a, team_b, looser_score_multiplier)[0]


def _calculate_player_score(player, team):
    player['score'] = player['Marktwert'] * team['score_multiplier']
