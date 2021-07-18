from bs4 import BeautifulSoup
from requests import get
from datetime import datetime


def translate_release_date(date):

    if "Hoy" in date:
        return "Today"
    
    elif "Ayer" in date:
        return "Yesterday"

    else:

        date_formatted = "{year}-{day}".format(day='-'.join(date.split("/")[::-1]), year=datetime.now().year)
        return date_formatted

def translate_state(state):
    if state == "En emision":
        return "Airing"
    else:
        return "Finished"

def translate_next_episode(date):
    split_date=date.split(' ')

    if len(split_date) <= 3:
        return '-'
    else:
        translated_date = ''

        if split_date[4] == 'Enero':
            translated_date = '01'
        elif split_date[4] == 'Febrero':
            translated_date = '02'
        elif split_date[4] == 'Marzo':
            translated_date = '03'
        elif split_date[4] == 'Abril':
            translated_date = '04'
        elif split_date[4] == 'Mayo':
            translated_date = '05'
        elif split_date[4] == 'Junio':
            translated_date = '06'
        elif split_date[4] == 'Julio':
            translated_date = '07'
        elif split_date[4] == 'Agosto':
            translated_date = '08'
        elif split_date[4] == 'Septiembre':
            translated_date = '09'
        elif split_date[4] == 'Octubre':
            translated_date = '10'
        elif split_date[4] == 'Noviembre':
            translated_date = '11'
        elif split_date[4] == 'Diciembre':
            translated_date = '12'
        
        translated_date = translated_date + f"-{split_date[3]}"

        return translated_date

def retrieve_animes():
    anime_list = []
    url = "https://jkanime.net/"
    html = get(url).text
    soup = BeautifulSoup(html, "lxml")
    anime_html_list = soup.select('.maximoaltura a')

    for e in anime_html_list:

        name = e.h5.text
        episode = e.h6.text.split()[1]

        spaced_date = e.find("div", class_="anime__sidebar__comment__item__text").span.text
        unspaced_date = ("".join(spaced_date.split()))
        date = translate_release_date(unspaced_date)

        anime_url = "/".join(e['href'].split('/')[0:-2])
        anime_html = get(anime_url).text
        anime_soup = BeautifulSoup(anime_html, 'lxml')

        state_untranslated = anime_soup.find('span', class_='enemision').text

        state = translate_state(state_untranslated)

        next_episode_untranslated:str

        if state == "Airing":
            next_episode_untranslated = anime_soup.find_all('div', id='proxep')[1].p.text
        else:
            next_episode_untranslated = "-"

        next_episode = translate_next_episode(next_episode_untranslated)

        anime = {
            "name": name,
            "episode": episode,
            "released": date,
            "state": state,
            "next_episode": next_episode
        }

        anime_list.append(anime)

    return tuple(anime_list)

