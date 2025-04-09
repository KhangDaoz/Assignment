import requests
from bs4 import BeautifulSoup
import pandas 

response = requests.get('https://fbref.com/en/comps/9/stats/Premier-League-Stats')
soup = BeautifulSoup(response.content, 'html.parser')

# with open('data1.html', 'w', encoding='utf-8') as file:
#     file.write(str(soup.prettify()))
# with open('data1.html', 'r', encoding='utf-8') as file:
#     content = file.read()
content = str(soup.prettify())
content = content.replace('<!--', '').replace('-->', '')

soup = BeautifulSoup(content, 'html.parser')
table = soup.find('table', id = 'stats_standard').tbody
rows = table.find_all('tr')
list_player = []
cnt = 0
for row in rows:
    player = []
    for x in row.find_all('td'):
        player.append(x.text.strip())
    if player == []:
        continue
    list_player.append(player)

data_frame = pandas.DataFrame(list_player, columns = ['Player', 'Nation', 'Pos',  'Squad', 'Age', 'Born',	'MP', 'Starts',	'Min', '90s', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'xG', 'npxG',	'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls', 'Ast', 'G+A',	'G-PK', 'G+A-PK', 'xG',	'xAG', 'xG+xAG', 'npxG', 'npxG+xAG','Matches'])
data_frame.to_csv('result.csv', index = False, encoding = 'utf-8-sig')