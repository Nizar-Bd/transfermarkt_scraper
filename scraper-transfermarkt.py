import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
import os

HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
           'cache-control': 'max-age=0',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116',
           }

leagues = ['ligue-1','serie-a','premier-league','laliga','bundesligua','liga-nos','superlig','eredivisie']
codes = ['fr1','it1','GB1','ES1','L1','PO1','TR1','NL1']

leagues_urls = []

for league, code in zip(leagues, codes):
    leagues_urls.append(f'https://www.transfermarkt.com/{league}/startseite/wettbewerb/{code}')


def new_session():
    global HEADERS
    session = requests.session()
    session.headers.update(HEADERS)
    return session


def get_data(session, urls):
    for url in urls:
        res = session.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find('table', class_='items')

        league_name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald').text.lower().strip().replace(' ','-')
        print(f'LEAGUE : getting data for {league_name} ⌛')
        #create dir for league
        league_path = os.path.join('data', league_name)
        if not os.path.exists(league_path):
            os.makedirs(league_path)

        # get club urls
        club_urls = ['https://www.transfermarkt.com' + x.find('a')['href'] for x in table.find_all('td', class_='hauptlink no-border-links')]
        club_urls = [x[:-4] for x in club_urls]
        for club_url in club_urls:
            res = session.get(club_url+'2023')
            soup = BeautifulSoup(res.content, 'html.parser')
            club_name = soup.find('h1', class_='data-header__headline-wrapper data-header__headline-wrapper--oswald').text.lower().strip().replace(' ','-')
            print(f'CLUB : getting data for {club_name} ⌛')
            #make dir for the club
            club_path = os.path.join(league_path, club_name)
            if not os.path.exists(club_path):
                os.makedirs(club_path)

            players_list = []
            for year in range(1979,2024):
                url_year = club_url + f'{year}'
                res = session.get(url_year)
                soup = BeautifulSoup(res.content, 'html.parser')

                players = soup.find('div', id='yw1').find_all('tr', class_='odd') + soup.find('div', id='yw1').find_all('tr', class_='even')

                for player in players :
                    try :
                        name = player.find('td', class_='hauptlink').find('a').text.lower().strip()
                    except :
                        name = np.nan

                    try :
                        birth_date = player.find_all('td', class_='zentriert')[1].text[:-5].replace(',','').lower()
                    except :
                        birth_date = np.nan

                    try :
                        nation = player.find_all('td', class_='zentriert')[2].find()['title'].lower() or np.nan
                    except :
                        nation = np.nan

                    try :
                        face_url = player.find('td', rowspan='2').find()['data-src'] or np.nan
                    except :
                        face_url = np.nan

                    players_list.append({'name':name,
                                         'birth_date':birth_date,
                                         'nation':nation,
                                         'face_url':face_url})

            club_df = pd.DataFrame(players_list).drop_duplicates()
            csv_path = os.path.join(club_path, f'{club_name}.csv')
            club_df.to_csv(csv_path)
            print(f'CLUB : data colected and saved for {club_name} ✅ \n total players in this club : {len(club_df)}')

        print(f'LEAGUE : data colected and saved for {league_name} ✅')

if __name__ == '__main__' :
    session = new_session()
    get_data(session, leagues_urls)
