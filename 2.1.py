import csv
import requests

print('Чтобы подобрать подходящее аниме, пройдите опрос. На закрытые вопросы отвечайте "Da" или "Net"')
print()
f = open('anime.csv', encoding='utf-8', newline='')
animes = csv.DictReader(f)


def format_pokaza(param, key, anime_list_param):
    if param != '':
        for anime in anime_list_param[:]:
            if not (anime[key] == param):
                anime_list_param.remove(anime)


def genre_and_studio(mult_params, key, anime_list_param):
    if mult_params != ['']:
        rmv = True
        for anime in anime_list_param[:]:
            for param in mult_params:
                anime_params = anime[key].replace(' ', '').split(',')
                if param in anime_params:
                    rmv = False
                    break
            if rmv:
                anime_list_param.remove(anime)
            rmv = True


def Da_Net(param, key, check_param, anime_list_param):
    if param != '':
        if param == 'Da':
            for anime in anime_list_param[:]:
                if anime[key] == check_param:
                    anime_list_param.remove(anime)
        if param == 'Net':
            for anime in anime_list_param[:]:
                if anime[key] != check_param:
                    anime_list_param.remove(anime)


def ckey(anime):
    try:
        result = float(anime['Rating Score'])
        return result
    except ValueError:
        return 0


anime_list = list()
anime_list_temp = list()
anime_list = [anime for anime in animes]
anime_list.sort(reverse=True, key=ckey)

print('Какой жанр?')
genre = input().replace(' ', '').split(',')
print('Какой формат показа?')
anime_type = input()
print('Многесерийное аниме?')
serial = input()
print('Закончилось ли аниме?')
finished = input()
print('Какая студия?')
studios = input().replace(' ', '').split(',')

genre_and_studio(genre, 'Tags', anime_list)
genre_and_studio(studios, 'Studios', anime_list)
format_pokaza(anime_type, 'Type', anime_list)
Da_Net(serial, 'Episodes', '1', anime_list)
Da_Net(finished, 'Finished', 'False', anime_list)
f.close()

k = 1
for anime in anime_list:
    url = 'https://www.anime-planet.com/images/anime/covers/thumbs/' + str(anime['Anime-PlanetID']) + '.jpg'
    img_data = requests.get(url).content
    handler = open(str(k) + '.jpg', 'wb')
    handler.write(img_data)
    handler.close()
    k += 1
    if k > 5:
        break

f = open('animes.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(animes.fieldnames)
for anime in anime_list:
    wr.writerow(anime.values())
f.close()

print()
print('Подобранные аниме хранятся в файле animes.csv')
