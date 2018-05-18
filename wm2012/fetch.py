from ftw.testbrowser import browser
from functools import partial
from paths import TEAMS_PATH
import json


def recursive_encode(item):
    if isinstance(item, (int, str)):
        return item

    if isinstance(item, unicode):
        return item.encode('utf-8')

    if isinstance(item, dict):
        return dict(zip(*map(partial(map, recursive_encode), zip(*item.items()))))

    if isinstance(item, list):
        return map(recursive_encode, item)

    raise ValueError('Unexpected type "{0}" ({1})'.format(type(item), repr(item)))


def fetch_teams():
    print '-> Fetch teams into', TEAMS_PATH
    teams = {}

    with browser:
        browser.open('https://wmgame2018.4teamwork.ch/nationen-spieler')
        table = browser.css('#content-core table.listing').first
        for row in table.css('tbody tr'):
            link = row.css('td a').first.attrib.get('href')
            team_id = int(link.split('/')[-1])

            team = row.dict()
            team['Link'] = link
            team['ID'] = team_id
            team['FIFA Rang'] = int(team['FIFA Rang'])
            team['players'] = list(fetch_players(team))
            teams[team_id] = team

    teams = recursive_encode(teams)

    with open(TEAMS_PATH, 'w+') as file_:
        json.dump(teams, file_, sort_keys=True, indent=4,
                  ensure_ascii=False, encoding='utf-8')


def fetch_players(team):
    print '-> Fetch players of', team['Nation']
    browser.open(team['Link'])
    table = browser.css('#content-core table.listing').first
    for row in table.css('tbody tr'):
        link = row.css('td a').first.attrib.get('href')
        player_id = int(link.split('/')[-1])

        player = row.dict()
        player['Marktwert'] = int(player['Marktwert'].replace("'", ""))
        player['ID'] = player_id
        player['Link'] = link
        yield player


def command():
    fetch_teams()
