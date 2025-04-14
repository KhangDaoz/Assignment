import requests
import pandas as pd

url = 'https://www.footballtransfers.com/en/transfers/actions/confirmed/overview'

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Referer": "https://www.footballtransfers.com/en/transfers/confirmed/2024-2025/uk-premier-league",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

payload = {
    "orderBy": "date_transfer",
    "orderByDescending": 1,
    "page": 1,
    "pages": 0,
    "pageItems": 25,
    "countryId": all,
    "season": 5845,
    "tournamentId": 31,
    "clubFromId": all,
    "clubToId": all,
}

df = pd.DataFrame()

for page in range(1, 15):
    payload['page'] = page
    response = requests.post(url, headers = headers, data = payload)
    data = response.json()
    cur_df = pd.DataFrame(data['records'])
    df = pd.concat([df, cur_df], axis = 0, ignore_index = True)

df_transfer = df[['player_name', 'country_name', 'age', 'club_from_name', 'club_to_name', 'amount', 'date_transfer']]
df_transfer = df_transfer.rename(columns = {'player_name' : 'Player'})

df = pd.read_csv('result.csv', encoding = 'utf-8-sig')
df_transfer = df_transfer.merge(df[['Player', 'Minutes']], how = 'left', on = 'Player')
df_transfer = df_transfer[df_transfer['Minutes'] > 900].reset_index(drop = True)
print(df_transfer)
# df_transfer.to_csv('test.csv', encoding = 'utf-8-sig')