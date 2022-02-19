from riotwatcher import LolWatcher, ApiError
import pandas as pd

def items (items, row, slot):
    if (items == 0):
        row[slot] = ""
    else:
        row[slot] = item_dict[str(row[slot])]
    return row[slot]

# golbal variables
api_key = 'RGAPI-7867657e-5e92-4ea6-ae7b-9325e12fd9fa'
watcher = LolWatcher(api_key)
my_region = 'euw1'

me = watcher.summoner.by_name(my_region, 'Rodri05')
#print(me)

# Return the rank status
my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
#print(my_ranked_stats)

my_matches = watcher.match.matchlist_by_puuid('EUROPE', me['puuid'])

# fetch last match detail
last_match = my_matches[0]
match_detail = watcher.match.by_id('EUROPE', last_match)

participants = []
for row in match_detail['info']['participants']:
    participants_row = {}
    participants_row['champion'] = row['championId']
    participants_row['sumSpell1'] = row['summoner1Id']
    participants_row['sumSpell2'] = row['summoner2Id']
    participants_row['win'] = row['win']
    participants_row['kills'] = row['kills']
    participants_row['deaths'] = row['deaths']
    participants_row['assists'] = row['assists']
    participants_row['totalDamageDealt'] = row['totalDamageDealt']
    participants_row['goldEarned'] = row['goldEarned']
    participants_row['champLevel'] = row['champLevel']
    participants_row['totalMinionsKilled'] = row['totalMinionsKilled']
    participants_row['item0'] = row['item0']
    participants_row['item1'] = row['item1']
    participants_row['item2'] = row['item2']
    participants_row['item3'] = row['item3']
    participants_row['item4'] = row['item4']
    participants_row['item5'] = row['item5']
    participants_row['item6'] = row['item6']
    participants.append(participants_row)
df = pd.DataFrame(participants)
df

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

# Lets get some static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
static_item_list = watcher.data_dragon.items(latest, 'en_US')
static_spell_list = watcher.data_dragon.summoner_spells(latest, 'en_US')

#  static list data to dict for looking up
champ_dict = {}
item_dict = {}
spell_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

for key in static_item_list['data']:
    row = static_item_list['data'][key]
    item_dict[key] = row['name']

for key in static_spell_list['data']:
    row = static_spell_list['data'][key]
    spell_dict[row['key']] = row['name']

for row in participants:
    row['champion'] = champ_dict[str(row['champion'])]
    row['sumSpell1'] = spell_dict[str(row['sumSpell1'])]
    row['sumSpell2'] = spell_dict[str(row['sumSpell2'])]
    row['item0'] = items(row['item0'], row, 'item0')
    row['item1'] = items(row['item1'], row, 'item1')
    row['item2'] = items(row['item2'], row, 'item2')
    row['item3'] = items(row['item3'], row, 'item3')
    row['item4'] = items(row['item4'], row, 'item4')
    row['item5'] = items(row['item5'], row, 'item5')
    row['item6'] = items(row['item6'], row, 'item6')

# print dataframe
df = pd.DataFrame(participants)
df

print(df)