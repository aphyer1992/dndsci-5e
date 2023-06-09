import random
import math
import itertools
import json

log_location = 'lds2_output.csv'
chars = [
    {
        'full_name' : 'Daring Duelist',
        'health' : 6,
        'attack' : 5,
        'block' : 0,
        'range' : 1,
    },   
    {
        'full_name' : 'Bludgeon Bandit',
        'health' : 6,
        'attack' : 4,
        'block' : 1,
        'range' : 1,
    },    
    {
        'full_name' : 'Silent Samurai',
        'health' : 6,
        'attack' : 3,
        'block' : 2,
        'range' : 1,
    },     
    {
        'full_name' : 'Lamellar Legionary',
        'health' : 6,
        'attack' : 2,
        'block' : 3,
        'range' : 1,
    },    
    {
        'full_name' : 'Granite Golem',
        'health' : 6,
        'attack' : 1,
        'block' : 4,
        'range' : 1,
    },   
    {
        'full_name' : 'Flamethrower Felon',
        'health' : 6,
        'attack' : 4,
        'block' : 0,
        'range' : 2,
    }, 
    {
        'full_name' : 'Captain Chakram',
        'health' : 6,
        'attack' : 3,
        'block' : 1,
        'range' : 2,
    },    
    {
        'full_name' : 'Jaunty Javelineer',
        'health' : 6,
        'attack' : 2,
        'block' : 2,
        'range' : 2,
    },    
    {
        'full_name' : 'Hammer Hurler',
        'health' : 6,
        'attack' : 1,
        'block' : 3,
        'range' : 2,
    },   
    {
        'full_name' : 'Professor Pyro',
        'health' : 6,
        'attack' : 3,
        'block' : 0,
        'range' : 3,
    }, 
    {
        'full_name' : 'Matchlock Marauder',
        'health' : 6,
        'attack' : 2,
        'block' : 1,
        'range' : 3,
    },   
    {
        'full_name' : 'Rugged Ranger',
        'health' : 6,
        'attack' : 1,
        'block' : 2,
        'range' : 3,
    },   
    {
        'full_name' : 'Thunder Tyrant',
        'health' : 6,
        'attack' : 2,
        'block' : 0,
        'range' : 4,
    }, 
    {
        'full_name' : 'Amazon Archer',
        'health' : 6,
        'attack' : 1,
        'block' : 1,
        'range' : 4,
    },   
    {
        'full_name' : 'Wily Wizard',
        'health' : 6,
        'attack' : 1,
        'block' : 0,
        'range' : 5,
    },
]

used_names = []
for c in chars:
    c['name'] = c['full_name'][0]
    assert( c['name'] not in used_names )
    used_names.append(c['name'])

global_verbose = False

def get_team():
    team = random.sample(chars,3)
    team = [c.copy() for c in team]
    team = sorted(team , key = lambda char: (char['range'] * 10) - char['block'])

    return(team)

def exec_attack(attack_team, defense_team, attacker_name):
    attacker = [c for c in attack_team if c['name'] == attacker_name]
    if(len(attacker) == 0):
        if(global_verbose):
            print(attacker_name + ' has been KOd in previous rounds, skipping\n')
        return()
    assert(len(attacker) == 1)
    attacker = attacker[ 0 ]
    if(attacker['damage_taken'] >= attacker['health']):
        raise('AIIIIE')
        if(global_verbose):
            print(attacker_name + ' has been KOd earlier this round, skipping\n')
        return()
    attacker_pos = attack_team.index(attacker)
    attacker_range = attacker['range']
    remaining_range = attacker_range - attacker_pos
    if(remaining_range < 1 ):
        if(global_verbose):
            print(attacker_name + ' is too far back to attack, skipping\n')
        return()
    if( len(defense_team) == 0 ):
        raise('AIIIEE')
    target_pos = min(remaining_range - 1, len(defense_team) - 1)

    if(target_pos < 0 ):
        raise('AUGH')

    target = defense_team[target_pos]
    if(global_verbose):
        print(attacker_name + ' targets ' + target['name'] + '\n')
    dam = max(1, attacker['attack'] - target['block'])
    target['damage_taken'] = target['damage_taken'] + dam
    if(global_verbose and target['damage_taken'] >= target['health']):
        print(target['name'] + ' KOd\n')
        print('{} takes {} damage, now at {}\n'.format(target['name'], dam, target['damage_taken']))

def play_game(a_team, b_team, shuffle_seed=None):
    round_num = 1
    inits = []
    for char in a_team:
        inits.append(['a', char['name']])
        char['damage_taken'] = 0

    for char in b_team:
        inits.append(['b', char['name']])
        char['damage_taken'] = 0

    if shuffle_seed is None:
        random.shuffle(inits)
    else:
        # seed is an array of 0-5 in some order
        new_inits = []
        for i in range(0,6):
            new_inits.append(inits[shuffle_seed[i]])
        inits = new_inits


    while( True ):
        if(global_verbose):
            print('\n---ROUND {}---\n'.format(round_num))
        round_num = round_num + 1
        for i in inits:
            attack_team = a_team if i[0] == 'a' else b_team
            defense_team = b_team if i[0] == 'a' else a_team
            attacker_name = i[1]
            exec_attack(attack_team, defense_team, attacker_name)

            a_team = [c for c in a_team if c['health'] > c['damage_taken']]
            b_team = [c for c in b_team if c['health'] > c['damage_taken']]

            #check for win
            if(len(a_team) == 0):
                assert(len(b_team) > 0)
                return('B')
            if(len(b_team) == 0):
                assert(len(a_team) > 0)
                return('A')

def list_teams():
    return(list(itertools.combinations(chars, 3)))

def team_from_string(team):
    team_chars = [ team[0], team[1], team[2]]
    team_chars = [ c for c in chars if c['name'] in team_chars ]
    team_chars = [c.copy() for c in team_chars ]
    team_chars = sorted(team_chars, key = lambda char: (char['range'] * 10) - char['block'])
    return(team_chars)

def generate_winrate_cache():
    team_strings = []
    teams = list_teams()
    for t in teams:
        team_strings.append(t[0]['name'] + t[1]['name'] + t[2]['name'])

    shuffle_seeds = list( itertools.permutations([0,1,2,3,4,5]))

    winstruct = {}

    for t in team_strings:
        winstruct[t] = {}

    count = 0
    for i in team_strings:
        i_team = team_from_string(i)
        for j in team_strings:
            if i == j:
                winstruct[i][j] = 0.5
            elif i < j:
                count = count + 1
                if count%100 == 0:
                    print(count)
                j_team = team_from_string(j)
                i_wins = 0
                j_wins = 0
                for seed in shuffle_seeds:
                    res = play_game(i_team, j_team, seed)
                    if res == 'A':
                        i_wins = i_wins + 1
                    else:
                        j_wins = j_wins + 1

                winstruct[i][j] = i_wins / len(shuffle_seeds)
                winstruct[j][i] = j_wins / len(shuffle_seeds)


    my_json = json.dumps(winstruct)
    f = open('winstruct.json', 'w')
    f.write(my_json)
    f.close()

def dataset_random_team():
    while True:
        team = get_team()
        pop = sum([c['popularity'] for c in team]) # char pop is 1-2, team 3-6
        if pop > (6*random.random()):
            return(team)


def write_log_row(log_row, mode='a'):
    log_string = ','.join([str(e) for e in log_row])+"\n"
    f = open(log_location, mode)
    f.write(log_string)
    
def setup_logs():
    log_row = [
        'Green Team Char 1',
        'Green Team Char 2',
        'Green Team Char 3',
        'Blue Team Char 1',
        'Blue Team Char 2',
        'Blue Team Char 3',
        'Winning Team'
    ]
    write_log_row(log_row, mode='w')
    
def gen_dataset():
    setup_logs()
    for c in chars:
        c['popularity'] = 1 + random.random()

    rows_to_make = 131826
    i = 0
    while i < rows_to_make:
        if i%10000 == 0:
            print(i)
        team_a = dataset_random_team()
        team_b = dataset_random_team()
        result = play_game(team_a, team_b)
        row = []
        random.shuffle(team_a)
        random.shuffle(team_b)
        for char in team_a:
            row.append(char['full_name'])
        for char in team_b:
            row.append(char['full_name'])
        if result == 'A':
            row.append('Green')
        else:
            row.append('Blue')
        write_log_row(row)
        i = i + 1

def retrieve_data(apply_filter = lambda x : True):
    f = open('lds2_downloaded_data.csv')
    index_row = f.readline()
    index_row = index_row.replace('\n', '')
    cols = index_row.split(',')
    data = []
    i = 0
    while True:
        if i%1e5 == 0:
            print(i)
        i = i + 1
        row = f.readline()
        row = row.replace('\n', '')
        if row is None:
            break
        row = row.split(',')
        if(len(row) < len(cols)):
            break
        row_data = {}
        col_index = 0
        while col_index < len(cols):
            row_data[cols[col_index]] = row[col_index]
            col_index= col_index + 1
        if apply_filter(row_data) == True:
            data.append(row_data)
    print(len(data))
    return(data)


    
random.seed('LDS2')
#gen_dataset()
data = retrieve_data()
#generate_winrate_cache()
team_strings = []
teams = list_teams()
for t in teams:
    team_strings.append(t[0]['name'] + t[1]['name'] + t[2]['name'])

with open('winstruct.json', 'r') as file:
    winstruct = json.load(file)

char_data = {}
melee_data = [[0,0], [0,0], [0,0], [0,0]]
team_data = {}
for c in chars:
    char_data[c['full_name']] = { 'wins' : 0, 'losses' : 0}

melee_names = [c['full_name'] for c in chars if c['range'] == 1]

for row in data:
    green_chars = [
        row['Green Team Char 1'],
        row['Green Team Char 2'],
        row['Green Team Char 3'],
    ]
    blue_chars = [
        row['Blue Team Char 1'],
        row['Blue Team Char 2'],
        row['Blue Team Char 3'],
    ]
    green_win = 1 if row['Winning Team'] == 'Green' else 0
    winning_chars = green_chars if green_win else blue_chars
    for c in winning_chars:
        char_data[c]['wins'] = char_data[c]['wins'] + 1
    losing_chars = blue_chars if green_win else green_chars
    for c in losing_chars:
        char_data[c]['losses'] = char_data[c]['losses'] + 1

    winning_melee_count = len([w for w in winning_chars if w in melee_names])
    losing_melee_count = len([w for w in losing_chars if w in melee_names])
    melee_data[winning_melee_count][0] = melee_data[winning_melee_count][0] + 1
    melee_data[losing_melee_count][1] = melee_data[losing_melee_count][1] + 1

    winning_team = [c[0] for c in winning_chars]
    winning_team.sort()
    winning_team = ''.join(winning_team)
    
    losing_team = [c[0] for c in losing_chars]
    losing_team.sort()
    losing_team = ''.join(losing_team)

    if winning_team not in team_data.keys():
        team_data[winning_team] = { 'wins' : 0, 'losses' : 0}

    if losing_team not in team_data.keys():
        team_data[losing_team] = { 'wins' : 0, 'losses' : 0}

    team_data[winning_team]['wins'] = team_data[winning_team]['wins'] + 1
    team_data[losing_team]['losses'] = team_data[losing_team]['losses'] + 1

i = 0
while i < 4:
    wins = melee_data[i][0]
    losses = melee_data[i][1]
    winrate = wins / ( wins + losses )
    print('Teams with {} melee win {:.2f}%\n'.format(i, winrate*100))
    i = i + 1
    
char_names = char_data.keys()
for c in char_names:
    wins = char_data[c]['wins']
    losses = char_data[c]['losses']
    winrate = wins / ( wins + losses )
    print('{} wins {:.2f}%\n'.format(c, winrate*100))

teams = team_data.keys()
winstruct_teams = winstruct.keys()
team_winrates = []
for t in teams:
    wins = team_data[t]['wins']
    losses = team_data[t]['losses']
    winrate = wins / ( wins + losses )
    team_winrates.append([t, winrate])
team_winrates.sort(key = lambda x : x[1], reverse=True)

i = 0
while i < 5:
    good_team = team_winrates[i]
    t = good_team[0]
    winrate = good_team[1]
    winstruct_team_name = [ w for w in winstruct_teams if w[0] in t and w[1] in t and w[2] in t ]
    assert(len(winstruct_team_name) == 1 )
    winstruct_team_name = winstruct_team_name[0]
    win_vs_npc = winstruct[winstruct_team_name]['SFR']
    print('Team {} has winrate of {:.2f}% against field and {:.2f}% against NPC'.format(t,winrate * 100, win_vs_npc * 100))
    i = i + 1


details = []
for t in team_strings:
    team_struct = winstruct[ t ]
    winrates = team_struct.values()
    avg_winrate = sum(winrates) / len(winrates)
    distinct = []
    for w in winrates:
        if w not in distinct:
            distinct.append(w)
    loses_to = []
    for o in team_strings:
        if team_struct[o] == 0:
            loses_to.append(o)
    details.append({ 'team' : t, 'avg_winrate' : avg_winrate, 'num_distinct' : len(distinct), 'loses_to' : loses_to})


char_names = [c['name'] for c in chars]
char_details = []
for c in char_names:
    team_matches = [t for t in team_strings if c in t]
    detail_matches = [d for d in details if d['team'] in team_matches]
    winrates = [d['avg_winrate'] for d in detail_matches]
    char_details.append({ 'char' : c, 'avg_winrate' : sum(winrates) / len(winrates)})

char_details = sorted(char_details, key=lambda x: x['avg_winrate'])
for e in char_details:
    print( '{} wins {:.2f}% of the time\n'.format(e['char'], e['avg_winrate'] * 100))


max_winrate = max([ x['avg_winrate'] for x in details])
best_team = [x for x in details if x['avg_winrate'] == max_winrate][0]['team']

melee = [c['name'] for c in chars if c['range'] == 1]

count_win_by_melee = [[0,0], [0,0], [0,0], [0,0]]

for t in team_strings:
    melee_count = 0
    winrate = [d['avg_winrate'] for d in details if d['team'] == t][0]
    for c in t:
        if c in melee:
            melee_count = melee_count + 1
    count_win_by_melee[melee_count][0] = count_win_by_melee[melee_count][0] + 1
    count_win_by_melee[melee_count][1] = count_win_by_melee[melee_count][1] + winrate


num_melee = 0
for e in count_win_by_melee:
    print('With {} melee chars:\n'.format(num_melee))
    print('{} distinct teams, avg winrate {:.2f}%\n'.format(e[0], 100 * e[1] / e[0] ))
    num_melee = num_melee + 1

rangestruct = {}
for c in chars:
    rangestruct[c['name']] = c['range']

npc_team = 'SFR'
good_teams = []
for t in team_strings:
    winrate = winstruct[t][npc_team]
    if winrate > 0.5:
        good_teams.append([t,winrate])

good_teams.sort(key=lambda x: x[1])

for e in good_teams:
    t = e[0]
    w = e[1]
    ranges = [ rangestruct[x] for x in t ]
    rangestring = ''.join([str(x) for x in ranges])
    print('{} ({}) wins {:.1f}% of the time'.format(t, rangestring, w*100))
