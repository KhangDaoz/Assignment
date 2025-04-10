import requests
from bs4 import BeautifulSoup
import pandas 
import time

def get_frame_from_URL(url):
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
    table = table_container.tbody
    #get headers from table
    thead = table_container.thead
    headers = []
    #get name table
    name = url.split('/')[-2]
    for x in thead.find_all('tr')[1].find_all('th'):
        if x.text.strip() == '':
            continue
        headers.append(x.text.strip() + '_' + name)
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

def check_playing_time(x):
    x = str(x)
    if ',' in x:
        return False
    return int(x) > 90

if __name__ == '__main__':
    url_dict = {
        'Standard Stats' : 'https://fbref.com/en/comps/9/stats/Premier-League-Stats',
        # 'Goalkeeping' : 'https://fbref.com/en/comps/9/keepers/Premier-League-Stats',
        # 'Shooting' : 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats',
        # 'Passing' : 'https://fbref.com/en/comps/9/passing/Premier-League-Stats',
        # 'Goal and Shot Creation' : 'https://fbref.com/en/comps/9/gca/Premier-League-Stats',
        # 'Defensive Actions' : 'https://fbref.com/en/comps/9/defense/Premier-League-Stats',
        # 'Possession' : 'https://fbref.com/en/comps/9/possession/Premier-League-Stats',
        # 'Miscellaneous Stats' : 'https://fbref.com/en/comps/9/misc/Premier-League-Stats',
    }
    data_frame = {}
    for name, url, in url_dict.items():
        data_frame[name] = get_frame_from_URL(url)
        # data_frame[name] = pandas.read_csv(name + '.csv')
        time.sleep(3)
    data_frame['Standard Stats']['Nation_stats'] = data_frame['Standard Stats']['Nation_stats'].apply(process_nation)
    data_frame['Standard Stats']['Min_stats'] = data_frame['Standard Stats']['Min_stats'].apply(lambda x: int(str(x).replace(',', '')))
    data_frame['Standard Stats'] = data_frame['Standard Stats'][data_frame['Standard Stats']['Min_stats'] > 90]
    # data_frame['Standard Stats'] = data_frame['Standard Stats'].drop(['90s', 'G+A', 'G-PK', 'PK'], axis = 1)
    # for name in url_dict.keys():
    #     if name != 'Standard Stats':
    #         data_frame['Standard Stats'] = data_frame['Standard Stats'].merge(data_frame[name], how = 'left', on = 'Player', suffixes = ('', '_x'))
    data_frame['Standard Stats'].to_csv('result.csv', index = False, encoding = 'utf-8-sig')
    # get_frame_from_URL(url_dict['Goalkeeping'])