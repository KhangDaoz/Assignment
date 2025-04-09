import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

def get_player(url):
    # get html from url
    response = requests.get(url)
    print(response.status_code)

    # use soup to parse html
    soup = BS(response.content, 'lxml')
    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    # table_container = soup.find('table', id = 'stats_standard')
    
    # rows = table_container.tbody.find_all('tr')
    # content = soup.find('div', id="content")
    # all_stats_standard = content.find('div', id = "all_stats_standard", class_ = 'table_wrapper')
    # # print(all_stats_standard)
    # table_container = all_stats_standard.find('div', class_ = "table_container is_setup", id="div_stats_standard")
    # # print(table_container)
    # tbody = table_container.tbody
    # rows = tbody.find_all('tr')

    player_lists = []
    # for row in rows:
    #     #find classes in the table
    #     center_class = row.find_all('td', class_ = 'center')
    #     right_class = row.find_all('td', class_ = 'right')
    #     left_class = row.find_all('td', class_ = 'left')

    #     #find information of players
    #     name = left_class[0].text.strip()
    #     nation = left_class[1].text.strip()[3:] 
    #     pos = center_class[0].text.strip()
    #     age = center_class[1].text.strip()   

    #     playing_time = []
    #     playing_time.append(right_class[0].text.strip())
    #     playing_time.append(right_class[1].text.strip())
    #     playing_time.append(right_class[2].text.strip())

    #     if playing_time[0] == '0':
    #         continue
    #     if playing_time[2] != '' and ',' not in playing_time[2] and int(playing_time[2]) < 90:
    #         continue 

    #     performance = []
    #     performance.append(right_class[4].text.strip())
    #     performance.append(right_class[5].text.strip())
    #     performance.append(right_class[10].text.strip())
    #     performance.append(right_class[11].text.strip())
    #     # print(performance)

    #     expected = []
    #     expected.append(right_class[12].text.strip())
    #     expected.append(right_class[14].text.strip())
    #     # print(expected)

    #     progession = []
    #     progession.append(right_class[16].text.strip())
    #     progession.append(right_class[17].text.strip())  
    #     progession.append(right_class[18].text.strip())
    #     # print(progession)

    #     per90Minutes = []
    #     per90Minutes.append(right_class[19].text.strip())
    #     per90Minutes.append(right_class[20].text.strip())    
    #     per90Minutes.append(right_class[24].text.strip())
    #     per90Minutes.append(right_class[25].text.strip())
    #     # print(per90Minutes)

    #     player = [name, nation, team, pos, age]
    #     player.extend(playing_time)
    #     player.extend(performance)  
    #     player.extend(expected)
    #     player.extend(progession)
    #     player.extend(per90Minutes)
    #     # print(player)
    #     player_lists.append(player)
    return player_lists

if __name__ == "__main__":
    url = 'https://fbref.com/en/comps/9/stats/Premier-League-Stats' 

    player_lists = get_player(url)
    
    dataFrame = pd.DataFrame(player_lists, columns = ['Name', 'Nation', 'Team', 'Position', 'Age', 'Matches Played', 'Starts', 'Minutes', 'Goals', 'Assists', 'Yellow Cars', 'Red Cards', 'Expected Goals', 'Expected Assists', 'PrgC', 'PrgP', 'PrgR', 'Gls', 'Ast', 'xG', 'xGA'])
    dataFrame.to_csv('result.csv', encoding = 'utf-8-sig', index = False)