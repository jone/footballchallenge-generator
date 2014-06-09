from operator import itemgetter


def adding_player_to_first_team_allowed(player, first_team, second_team):
    first_team = first_team[:]
    second_team = second_team[:]
    first_team.append(player)
    return validate(first_team, second_team)


def adding_player_to_second_team_allowed(player, first_team, second_team):
    first_team = first_team[:]
    second_team = second_team[:]
    second_team.append(player)
    return validate(first_team, second_team)


def validate(first_team, second_team):
    if not validate_first_team_has_enough_nations(first_team):
        return False
    if not validate_all_teams_have_enough_nations(first_team, second_team):
        return False
    return True


def validate_first_team_has_enough_nations(first_team):
    nations = set(map(itemgetter('team_id'), first_team))

    amount_of_nations = len(nations)
    amount_of_players = len(first_team)
    amount_of_possible_future_nations = 11 - amount_of_players

    return amount_of_nations + amount_of_possible_future_nations

def validate_all_teams_have_enough_nations(first_team, second_team):
    nations = set(map(itemgetter('team_id'), first_team + second_team))

    amount_of_nations = len(nations)
    amount_of_players = len(first_team)
    amount_of_possible_future_nations = 22 - amount_of_players

    return amount_of_nations + amount_of_possible_future_nations
