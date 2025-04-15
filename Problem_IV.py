import requests
import pandas as pd

def collect_player_tranfer_values() :
    # get api from web to url
    url = 'https://www.footballtransfers.com/us/values/actions/most-valuable-football-players/overview'

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
        "positionGroupId": all,
        "mainPositionId": all,
        "playerRoleId": all,
        "age": all,
        "countryId": all,
        "tournamentId": 31
    }

    # get player transfer 
    df_transfer = pd.DataFrame()

    for page in range(1, 23):
        # change page
        payload['page'] = page

        # requests to api
        response = requests.post(url, headers = headers, data = payload)
        data = response.json()

        # create data_frame for page
        cur_df = pd.DataFrame(data['records'])

        # merge cur_page to df_transfer
        df_transfer = pd.concat([df_transfer, cur_df], axis = 0, ignore_index = True)

    # process dataframe
    df_result = df_transfer[['player_name', 'country_name', 'age', 'estimated_value']]
    df_result = df_result.rename(columns = {'player_name' : 'Player', 'country_name' : 'Country', 'age' : 'Age', 'estimated_value' : 'Price'})

    data_player_from_fbref = pd.read_csv('result.csv', encoding = 'utf-8-sig')

    # add column Minutes
    df_result = df_result.merge(data_player_from_fbref[['Player', 'Minutes']], how = 'left', on = 'Player')

    # remove player with less than 900 minutes played
    df_result = df_result[df_result['Minutes'] > 900].reset_index(drop = True)

    # result
    return df_result

if __name__ == '__main__':
    df = collect_player_tranfer_values()
    print(df)
