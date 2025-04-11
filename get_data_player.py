import requests
from bs4 import BeautifulSoup
import pandas 
import time

url_dict = {
    'stats' : 'https://fbref.com/en/comps/9/stats/Premier-League-Stats',
    'keepers' : 'https://fbref.com/en/comps/9/keepers/Premier-League-Stats',
    'shooting' : 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats',
    'passing' : 'https://fbref.com/en/comps/9/passing/Premier-League-Stats',
    'gca' : 'https://fbref.com/en/comps/9/gca/Premier-League-Stats',
    'defense' : 'https://fbref.com/en/comps/9/defense/Premier-League-Stats',
    'possession' : 'https://fbref.com/en/comps/9/possession/Premier-League-Stats',
    'misc' : 'https://fbref.com/en/comps/9/misc/Premier-League-Stats',
}

def process_nation(nation):
    nation = str(nation)
    res = ''
    for x in nation:
        if x.isupper():
            res += x
    return res

def get_frame_from_URL(url, prefix):
    #get html from url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #remove comments from html
    html = str(soup.prettify()) 
    html = html.replace('<!--', '').replace('-->', '')

    #use soup to parse html
    soup = BeautifulSoup(html, 'html.parser')
    table_container =  soup.find('table', class_ = "min_width sortable stats_table min_width shade_zero")
    table = table_container.tbody

    #get headers from table
    thead = table_container.thead
    headers_tags = thead.find_all('tr')
    group_names = []
    for th_tag in headers_tags[0].find_all('th'):
        colspan = int(th_tag.get('colspan', 1))
        name = th_tag.text.strip()
        if name == '':
            name = None
        group_names.extend([name] * colspan)

    headers = []
    for group, stat in zip(group_names, headers_tags[1].find_all('th')):
        if stat.text.strip() == '':
            continue
        if stat.text.strip() in ['Player', 'Nation', 'Squad', 'Pos']:
            headers.append(stat.text.strip())
        else:
            if group:
                col_name = f"{prefix}_{group}_{stat.text.strip()}"
            else:
                col_name = f"{prefix}_{stat.text.strip()}"
            headers.append(col_name)
    headers = headers[1:]

    #get rows from table
    rows = table.find_all('tr')
    player_list = []
    for row in rows:
        player = []
        for x in row.find_all('td'):
            player.append(x.text.strip())
        if player == []:
            continue
        player_list.append(player)
    
    return pandas.DataFrame(player_list, columns = headers)

def get_a_fram_with_all_data_from_web():
    # get frame from url
    data_frame = {}
    for name, url, in url_dict.items():
        data_frame[name] = get_frame_from_URL(url, name)
        print('fetched table', name)
        time.sleep(3)

    #merge all dataframes into one
    for name, df in data_frame.items():
        if name == 'stats':
            continue
        data_frame['stats'] = data_frame['stats'].merge(df, how = 'left', on = ['Player', 'Nation', 'Pos', 'Squad'], suffixes = ('', '_x'))

    #remove duplicates
    data_frame['stats'].drop_duplicates(subset = ['Player', 'Nation', 'Pos', 'Squad'], inplace = True)

    #remove player with less than 90 minutes played
    data_frame['stats']['stats_Playing Time_Min'] = data_frame['stats']['stats_Playing Time_Min'].apply(lambda x: int(str(x).replace(',', '')))
    data_frame['stats'] = data_frame['stats'][data_frame['stats']['stats_Playing Time_Min'] > 90]

    #process nation
    data_frame['stats']['Nation'] = data_frame['stats']['Nation'].apply(process_nation)

    #sort by player name
    data_frame['stats'] = data_frame['stats'].sort_values(by = 'Player')

    return data_frame['stats']

column_mapping = {
    'Player': 'Player',
    'Nation': 'Nation',
    'Team': 'Squad',
    'Position': 'Pos',
    'Age': 'stats_Age',
    'Matches Played': 'stats_Playing Time_MP',
    'Starts': 'stats_Playing Time_Starts',
    'Minutes': 'stats_Playing Time_Min',
    'Goals': 'stats_Performance_Gls',
    'Assists': 'stats_Performance_Ast',
    'Yellow Cards': 'stats_Performance_CrdY',
    'Red Cards': 'stats_Performance_CrdR',
    'Expected Goals': 'stats_Expected_xG',
    'Expedted Assist Goals': 'stats_Expected_xAG',
    'PrgC': 'stats_Progression_PrgC',
    'PrgP': 'stats_Progression_PrgP',
    'PrgR': 'stats_Progression_PrgR',
    'Gls': 'stats_Per 90 Minutes_Gls',
    'Ast': 'stats_Per 90 Minutes_Ast',
    'xG': 'stats_Per 90 Minutes_xG',
    'xAG': 'stats_Per 90 Minutes_xAG',
    'GA90': 'keepers_Performance_GA90',
    'Save%': 'keepers_Performance_Save%',
    'CS%': 'keepers_Performance_CS%',
    'Penalty Kicks Save%': 'keepers_Penalty Kicks_Save%',
    'SoT%': 'shooting_Standard_SoT%',
    'SoT/90': 'shooting_Standard_SoT/90',
    'G/sh': 'shooting_Standard_G/Sh',
    'Dist': 'shooting_Standard_Dist',
    'Passes Completed': 'passing_Total_Cmp',
    'Pass Completion': 'passing_Total_Cmp%',
    'TotDist': 'passing_Total_TotDist',
    'Short Pass completion': 'passing_Short_Cmp%',
    'Medium Pass completion': 'passing_Medium_Cmp%',
    'Long Pass completion': 'passing_Long_Cmp%',
    'KP': 'passing_KP',
    'pass into final third 1/3': 'passing_1/3',
    'PPA': 'passing_PPA',
    'CrsPA': 'passing_CrsPA',
    'Expected PrgP': 'passing_PrgP',
    'SCA': 'gca_SCA_SCA',
    'SCA90': 'gca_SCA_SCA90',
    'GCA': 'gca_GCA_GCA',
    'GCA90': 'gca_GCA_GCA90',
    'Tkl': 'defense_Tackles_Tkl',
    'TklW': 'defense_Tackles_TklW',
    'Att': 'defense_Challenges_Att',
    'Lost': 'defense_Challenges_Lost',
    'Blocks': 'defense_Blocks_Blocks',
    'Sh': 'defense_Blocks_Sh',
    'Pass': 'defense_Blocks_Pass',
    'Int': 'defense_Int',
    'Touches': 'possession_Touches_Touches',
    'Def Pen': 'possession_Touches_Def Pen',
    'Def 3rd': 'possession_Touches_Def 3rd',
    'Mid 3rd': 'possession_Touches_Mid 3rd',
    'Att 3rd': 'possession_Touches_Att 3rd',
    'Att Pen': 'possession_Touches_Att Pen',
    'Possession Att': 'possession_Take-Ons_Att',
    'Succ%': 'possession_Take-Ons_Succ%',
    'Tkld%': 'possession_Take-Ons_Tkld%',
    'Carries': 'possession_Carries_Carries',
    'PrgDist': 'possession_Carries_PrgDist',
    'ProgC': 'possession_Carries_PrgC',
    'Carries 1/3': 'possession_Carries_1/3',
    'CPA': 'possession_Carries_CPA',
    'Mis': 'possession_Carries_Mis',
    'Dis': 'possession_Carries_Dis',
    'Rec': 'possession_Receiving_Rec',
    'Possession PrgR': 'possession_Receiving_PrgR',
    'Fls': 'misc_Performance_Fls',
    'Fld': 'misc_Performance_Fld',
    'Off': 'misc_Performance_Off',
    'Crs': 'misc_Performance_Crs',
    'Recov': 'misc_Performance_Recov',
    'Won': 'misc_Aerial Duels_Won',
    'Miscellaneous Stats Lost': 'misc_Aerial Duels_Lost',
    'Won%': 'misc_Aerial Duels_Won%'
}

if __name__ == '__main__':
    #get data from web
    web_data_frame = get_a_fram_with_all_data_from_web()
    #result
    df = pandas.DataFrame()
    for x, y in column_mapping.items():
        df[x] = web_data_frame[y]
    #fill N/a for empty values or unvalid values
    df = df.replace('', 'N/a').fillna('N/a')
    #to csv file
    df.to_csv('result.csv', index = False, encoding = 'utf-8-sig')