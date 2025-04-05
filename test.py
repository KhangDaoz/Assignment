import cloudscraper as cs
from bs4 import BeautifulSoup as BS

url = 'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats'
scaper = cs.create_scraper()
response = scaper.get(url)
# print(response.status_code)
soup = BS(response.content, 'lxml')

content = soup.find('div', id="content")

all_stats_standard = content.find('div', id = 'all_stats_standard')
table_container = all_stats_standard.table
tbody = table_container.tbody
rows = tbody.find_all('tr')

for row in rows:
    print(row.th.text)
# print(table_container)