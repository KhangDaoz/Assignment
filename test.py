from bs4 import BeautifulSoup as BS
import pandas as pd
import time
import requests

def get_player(url, team):
    # url = 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats#all_stats_standard'
    # team = 'Arsenal'
    response = requests.get(url)
    print(response.status_code)
    soup = BS(response.content, 'lxml')

    content = soup.find('div', id="content")

    all_stats_standard = content.find('div', id = 'all_stats_standard')
    table_container = all_stats_standard.table
    # print(table_container)
    tbody = table_container.tbody
    rows = tbody.find_all('tr')
    player_lists = []
    for row in rows:
    #find all classes in the table
        center_class = row.find_all('td', class_ = 'center')
        right_class = row.find_all('td', class_ = 'right')
        # right_group_start_class = row.find_all('td', class_ = 'right group_start')
        # right_iz_group_start_class = row.find_all('td', class_ = 'right iz group_start')
        # right_iz_class = row.find_all('td', class_ = 'right iz')

        name = row.th.text.strip()
        if row.find('td', class_ = "left poptip") is not None:
            nation = row.find('td', class_ = "left poptip").text.strip()[3:] 
        pos = center_class[0].text.strip()
        age = center_class[1].text.strip()   

        playing_time = []
        playing_time.append(right_class[0].text.strip())
        playing_time.append(right_class[1].text.strip())
        playing_time.append(right_class[2].text.strip())
        # print(right_class)
        # print(playing_time)
        if playing_time[0] == '0':
            continue
        if playing_time[2] != '' and ',' not in playing_time[2] and int(playing_time[2]) < 90:
            continue 

        performance = []
        performance.append(right_class[4].text.strip())
        performance.append(right_class[5].text.strip())
        performance.append(right_class[10].text.strip())
        performance.append(right_class[11].text.strip())
        # print(performance)

        expected = []
        expected.append(right_class[12].text.strip())
        expected.append(right_class[14].text.strip())
        # print(expected)

        progession = []
        progession.append(right_class[16].text.strip())
        progession.append(right_class[17].text.strip())  
        progession.append(right_class[18].text.strip())
        # print(progession)

        per90Minutes = []
        per90Minutes.append(right_class[19].text.strip())
        per90Minutes.append(right_class[20].text.strip())    
        per90Minutes.append(right_class[24].text.strip())
        per90Minutes.append(right_class[25].text.strip())
        # print(per90Minutes)

        player = [name, nation, team, pos, age]
        player.extend(playing_time)
        player.extend(performance)  
        player.extend(expected)
        player.extend(progession)
        player.extend(per90Minutes)
        # print(player)
        player_lists.append(player)
    return player_lists

if __name__ == "__main__":
    club = {'Arsenal': 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats',
            # 'Aston Villa': 'https://fbref.com/en/squads/8602292d/Aston-Villa-Stats',
            # 'Bournemouth': 'https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats',
            # 'Brentford': 'https://fbref.com/en/squads/cd051869/Brentford-Stats',
            # 'Brighton & Hove Albion': 'https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats',
            # 'Chelsea': 'https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats',
            # 'Crystal Palace': 'https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats',
            # 'Everton': 'https://fbref.com/en/squads/d3fd31cc/Everton-Stats',
            # 'Fulham': 'https://fbref.com/en/squads/fd962109/Fulham-Stats',
            # 'Ipswich Town' : 'https://fbref.com/en/squads/b74092de/Ipswich-Town-Stats',
            # 'Leicester City': 'https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats',
            # 'Liverpool': 'https://fbref.com/en/squads/822bd0ba/Liverpool-Stats',
            # 'Manchester City': 'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats',
            # 'Manchester United': 'https://fbref.com/en/squads/19538871/Manchester-United-Stats',
            # 'Newcastle United': 'https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats',
            # 'Nottingham Forest': 'https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats',
            # 'Southampton' : 'https://fbref.com/en/squads/33c895d4/Southampton-Stats',
            # 'Tottenham Hotspur': 'https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats',
            # 'West Ham United': 'https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats',
            # 'Wolverhampton Wanderers': 'https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats'
            }
    player_lists = []
    for team, url in club.items():
        print(f'Đang lấy dữ liệu đội: {team}')
        player_lists.extend(get_player(url, team))
        time.sleep(10)  # Chờ 10 giây giữa mỗi lần gọi

    dataFrame = pd.DataFrame(player_lists, columns = ['Name', 'Nation', 'Team', 'Position', 'Age', 'Matches Played', 'Starts', 'Minutes', 'Goals', 'Assists', 'Yellow Cars', 'Red Cards', 'Expected Goals', 'Expected Assists', 'PrgC', 'PrgP', 'PrgR', 'Gls', 'Ast', 'xG', 'xGA'])
    # print(dataFrame)
    dataFrame.to_csv('result.csv', encoding = 'utf-8-sig', index = False)