import requests
import pandas as pd
from rapidfuzz import fuzz, process
from unidecode import unidecode

def create_names_key(name):
    name = unidecode(name)
    new_name = ''
    for x in name:
        if x.isalpha() or x == ' ':
            new_name += x
    new_name = new_name.split(' ')
    new_name.sort() 
    return ' '.join(new_name)

def search_exception_players(names):
    # api search special players
    api = 'https://www.footballtransfers.com/us/search/actions/search'

    # headers post request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Referer": "",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # payload post request
    payload = {
        'search_page': 1,
        'search_value': '',
        'players': 1,
        'teams': 1,
    }

    players = []
    for name in names:
        if name == 'Igor': # name from fbref different transfer, this is one special case
            name += ' Júlio'

        # change headers and payload to search players from web transfer
        headers['Referer'] = 'https://www.footballtransfers.com/us/search?search_value=' + name.replace(' ', '%20')
        payload['search_value'] = name.lower()

        # create player 
        player = [name]

        # get data from api
        response = requests.post(api, headers = headers, data = payload)
        data = response.json()
        first_hit = data['hits'][0]

        # append player to list
        team = first_hit['document']['title_sub'].split('-')[1]
        player.append(team)
        player.append(first_hit['document']['transfer_value'])
        players.append(player)
    return players
    
def collect_player_tranfer_values() :
    # get api from web 
    api = 'https://www.footballtransfers.com/us/values/actions/most-valuable-football-players/overview'

    # headers post request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Referer": "https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # payload post request
    payload = {
        "orderBy": "estimated_value",
        "orderByDescending": 1,
        "page": 1,
        "pages": 0,
        "pageItems": 25,
        "positionGroupId": 'all',
        "mainPositionId": 'all',
        "playerRoleId": 'all',
        "age": 'all',
        "countryId": 'all',
        "tournamentId": 31
    }

    # get player transfer 
    df_transfer = pd.DataFrame()

    for page in range(1, 23):
        # change page
        payload['page'] = page

        # requests to api
        response = requests.post(api, headers = headers, data = payload)
        data = response.json()

        # create data_frame for page
        page_df = pd.DataFrame(data['records'])

        # merge cur_page to df_transfer
        df_transfer = pd.concat([df_transfer, page_df], axis = 0, ignore_index = True)

    # read player from file
    data_player_from_fbref = pd.read_csv('SourceCode\\result.csv', encoding = 'utf-8-sig')
    # remove player with less than 900 minutes played
    data_player_from_fbref = data_player_from_fbref[data_player_from_fbref['Minutes'] > 900].reset_index(drop = True)

    # process age
    data_player_from_fbref['Age'] = data_player_from_fbref['Age'].apply(lambda x : int(x.split('-')[0]))
    df_transfer['age'] = df_transfer['age'].apply(lambda x : int(x))


    # choosee columns important
    df_transfer = df_transfer[['player_name', 'age', 'team_short_name', 'estimated_value']]
    data_player_from_fbref = data_player_from_fbref[['Player', 'Team', 'Age']]

    # create name_key
    df_transfer['names_key'] = df_transfer['player_name'].apply(create_names_key)
    data_player_from_fbref['names_key'] = data_player_from_fbref['Player'].apply(create_names_key)

    # match
    matched_names = []
    matched_scores = []

    for name in df_transfer['names_key']:
        best_match = process.extractOne(
            name,
            data_player_from_fbref['names_key'],
            scorer=fuzz.ratio
        )
        matched_names.append(best_match[0])        
        matched_scores.append(best_match[1])      

    # add to dataframe
    df_transfer['matched_names_key'] = matched_names
    df_transfer['match_score'] = matched_scores

    # merge two dataframes
    merged = df_transfer.merge(data_player_from_fbref, left_on=['matched_names_key'], right_on=['names_key'], suffixes=('_trans', '_fbref'))

    # match_score >= 75
    merged = merged[merged['match_score'] >= 75].reset_index(drop=True)

    # remove incorrect players
    uncertain_players = merged[merged['match_score'] != 100]
    merged = pd.concat([merged[merged['match_score'] == 100], uncertain_players[uncertain_players['age'] == uncertain_players['Age']]], axis = 0, ignore_index = True)

    # sort by names
    merged = merged.sort_values(by = 'Player')

    # process exception players
    missing_players = list(set(data_player_from_fbref['Player']) - set(merged['Player']))

    missing_player_details = pd.DataFrame(search_exception_players(missing_players), columns = ['Player', 'Team', 'estimated_value'])
    
    result = merged[['Player', 'Team', 'estimated_value']].reset_index(drop = True)
    result = pd.concat([result, missing_player_details], axis = 0, ignore_index = True)

    result.rename(columns = {'estimated_value' : 'Transfer Value'}, inplace = True)
    result = result.sort_values(by = 'Player')
    result.to_csv('SourceCode\\player_transfer_values.csv', encoding='utf-8-sig', index = False)

if __name__ == '__main__':
    collect_player_tranfer_values()