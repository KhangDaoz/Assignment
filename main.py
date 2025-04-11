import requests
from bs4 import BeautifulSoup
import pandas 
import time

def get_frame_from_URL(url, prefix):
    #get html from url
    response = requests.get(url)
    # print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    #remove comments from html
    html = str(soup.prettify()) 
    html = html.replace('<!--', '').replace('-->', '')
    #use soup to parse html
    soup = BeautifulSoup(html, 'html.parser')
    table_container =  soup.find('table', class_ = "min_width sortable stats_table min_width shade_zero")
    # with open('data.html', 'w', encoding = 'utf-8') as f:
    #     f.write(str(table_container.prettify))
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
    # print(group_names)
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
    # print(len(headers), headers)
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
    
    data_frame = pandas.DataFrame(player_list, columns = headers)
    # data_frame.to_csv('result.csv', index = False, encoding = 'utf-8-sig')
    return data_frame
    
def process_nation(nation):
    nation = str(nation)
    res = ''
    for x in nation:
        if x.isupper():
            res += x
    return res

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
    data_frame = {}
    for name, url, in url_dict.items():
        # data_frame[name] = get_frame_from_URL(url, name)
        # data_frame[name].to_csv(name + '.csv', index = False, encoding = 'utf-8-sig')
        data_frame[name] = pandas.read_csv(name + '.csv')
        print('fetched table', name)
        time.sleep(3)
    for name, df in data_frame.items():
        if name == 'stats':
            continue
        data_frame['stats'] = data_frame['stats'].merge(df, how = 'left', on = ['Player', 'Nation', 'Pos', 'Squad'], suffixes = ('', '_x'))
    
    data_frame['stats']['stats_Playing Time_Min'] = data_frame['stats']['stats_Playing Time_Min'].apply(lambda x: int(str(x).replace(',', '')))
    data_frame['stats'] = data_frame['stats'][data_frame['stats']['stats_Playing Time_Min'] > 90]
    # data_frame['Standard Stats'] = data_frame['Standard Stats'].drop(['90s', 'G+A', 'G-PK', 'PK'], axis = 1)
    # for name in url_dict.keys():
    #     if name != 'Standard Stats':
    #         data_frame['Standard Stats'] = data_frame['Standard Stats'].merge(data_frame[name], how = 'left', on = 'Player', suffixes = ('', '_x'))
    data_frame['stats'].drop_duplicates(subset = ['Player', 'Nation', 'Pos', 'Squad'], inplace = True)
    data_frame['stats']['Nation'] = data_frame['stats']['Nation'].apply(process_nation)
    data_frame['stats'] = data_frame['stats'].sort_values(by = 'Player')

    df = pandas.DataFrame()
    for x, y in column_mapping.items():
        df[x] = data_frame['stats'][y]
    # df['Player'] = data_frame['stats']['Player']
    # df['Nation'] = data_frame['stats']['Nation']
    # df['Team'] = data_frame['stats']['Squad']
    # df['Position'] = data_frame['stats']['Pos']
    # df['Age'] = data_frame['stats']['stats_Age']
    # df['Matches Played'] = data_frame['stats']['stats_Playing Time_MP']
    # df['Starts'] = data_frame['stats']['stats_Playing Time_Starts']
    # df['Minutes'] = data_frame['stats']['stats_Playing Time_Min']
    # df['Goals'] = data_frame['stats']['stats_Performance_Gls']
    # df['Assists'] = data_frame['stats']['stats_Performance_Ast']
    # df['Yellow Cards'] = data_frame['stats']['stats_Performance_CrdY']
    # df['Red Cards'] = data_frame['stats']['stats_Performance_CrdR']
    # df['Expected Goals'] = data_frame['stats']['stats_Expected_xG']
    # df['Expedted Assist Goals'] = data_frame['stats']['stats_Expected_xAG']
    # df['PrgC'] = data_frame['stats']['stats_Progression_PrgC']
    # df['PrgP'] = data_frame['stats']['stats_Progression_PrgP']
    # df['PrgR'] = data_frame['stats']['stats_Progression_PrgR']
    # df['Gls'] = data_frame['stats']['stats_Per 90 Minutes_Gls']
    # df['Ast'] = data_frame['stats']['stats_Per 90 Minutes_Ast']
    # df['xG'] = data_frame['stats']['stats_Per 90 Minutes_xG']
    # df['xAG'] = data_frame['stats']['stats_Per 90 Minutes_xAG']
    # df['GA90'] = data_frame['stats']['keepers_Performance_GA90']
    # df['Save%'] = data_frame['stats']['keepers_Performance_Save%']
    # df['CS%'] = data_frame['stats']['keepers_Performance_CS%']
    # df['Penalty Kicks Save%'] = data_frame['stats']['keepers_Penalty Kicks_Save%']
    # df['SoT%'] = data_frame['stats']['shooting_Standard_SoT%']
    # df['SoT/90'] = data_frame['stats']['shooting_Standard_SoT/90']
    # df['G/sh'] = data_frame['stats']['shooting_Standard_G/Sh'] 
    # df['Dist'] = data_frame['stats']['shooting_Standard_Dist']
    # df['Passes Completed'] = data_frame['stats']['passing_Total_Cmp']
    # df['Pass Completion'] = data_frame['stats']['passing_Total_Cmp%']
    # df['TotDist'] = data_frame['stats']['passing_Total_TotDist']
    # df['Short Pass completion'] = data_frame['stats']['passing_Short_Cmp%']
    # df['Medium Pass completion'] = data_frame['stats']['passing_Medium_Cmp%']
    # df['Long Pass completion'] = data_frame['stats']['passing_Long_Cmp%']
    # df['KP'] = data_frame['stats']['passing_KP']
    # df['pass into final third 1/3'] = data_frame['stats']['passing_1/3']
    # df['PPA'] = data_frame['stats']['passing_PPA']
    # df['CrsPA'] = data_frame['stats']['passing_CrsPA']
    # df['Expected PrgP'] = data_frame['stats']['passing_PrgP']
    # df['SCA'] = data_frame['stats']['gca_SCA_SCA']
    # df['SCA90'] = data_frame['stats']['gca_SCA_SCA90']
    # df['GCA'] = data_frame['stats']['gca_GCA_GCA']
    # df['GCA90'] = data_frame['stats']['gca_GCA_GCA90']
    # df['Tkl'] = data_frame['stats']['defense_Tackles_Tkl']
    # df['TklW'] = data_frame['stats']['defense_Tackles_TklW']
    # df['Att'] = data_frame['stats']['defense_Challenges_Att']
    # df['Lost'] = data_frame['stats']['defense_Challenges_Lost']
    # df['Blocks'] = data_frame['stats']['defense_Blocks_Blocks']
    # df['Sh'] = data_frame['stats']['defense_Blocks_Sh']
    # df['Pass'] = data_frame['stats']['defense_Blocks_Pass']
    # df['Int'] = data_frame['stats']['defense_Int']
    # df['Touches'] = data_frame['stats']['possession_Touches_Touches']
    # df['Def Pen'] = data_frame['stats']['possession_Touches_Def Pen']
    # df['Def 3rd'] = data_frame['stats']['possession_Touches_Def 3rd']
    # df['Mid 3rd'] = data_frame['stats']['possession_Touches_Mid 3rd']
    # df['Att 3rd'] = data_frame['stats']['possession_Touches_Att 3rd']
    # df['Att Pen'] = data_frame['stats']['possession_Touches_Att Pen']
    # df['Possession Att'] = data_frame['stats']['possession_Take-Ons_Att']
    # df['Succ%'] = data_frame['stats']['possession_Take-Ons_Succ%']
    # df['Tkld%'] = data_frame['stats']['possession_Take-Ons_Tkld%']
    # df['Carries'] = data_frame['stats']['possession_Carries_Carries']
    # df['PrgDist'] = data_frame['stats']['possession_Carries_PrgDist']
    # df['ProgC'] = data_frame['stats']['possession_Carries_PrgC']
    # df['Carries 1/3'] = data_frame['stats']['possession_Carries_1/3']
    # df['CPA'] = data_frame['stats']['possession_Carries_CPA']
    # df['Mis'] = data_frame['stats']['possession_Carries_Mis']
    # df['Dis'] = data_frame['stats']['possession_Carries_Dis']
    # df['Rec'] = data_frame['stats']['possession_Receiving_Rec']
    # df['Possession PrgR'] = data_frame['stats']['possession_Receiving_PrgR']
    # df['Fls'] = data_frame['stats']['misc_Performance_Fls']
    # df['Fld'] = data_frame['stats']['misc_Performance_Fld']
    # df['Off'] = data_frame['stats']['misc_Performance_Off']
    # df['Crs'] = data_frame['stats']['misc_Performance_Crs']
    # df['Recov'] = data_frame['stats']['misc_Performance_Recov']
    # df['Won'] = data_frame['stats']['misc_Aerial Duels_Won']
    # df['Miscellaneous Stats Lost'] = data_frame['stats']['misc_Aerial Duels_Lost']
    # df['Won%'] = data_frame['stats']['misc_Aerial Duels_Won%']

    df = df.replace('', 'N/a').fillna('N/a')
    df.to_csv('tmp.csv', index = False, encoding = 'utf-8-sig')
    # data_frame['stats'].to_csv('result.csv', index = False, encoding = 'utf-8-sig')
    # get_frame_from_URL(url_dict['Goalkeeping'])