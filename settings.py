from keras.utils import to_categorical
from geopy.geocoders import  Yandex
import pickle
import numpy as np

CEL =['ИЖС', 'СНТ, ДНП']

REGIONS =['Московская область', 'Москва']

GOR_OKRUGS = ['Раменский', 'Дмитровский', 'Домодедово', 'Истра', 'Чехов',
       'Ленинский', 'Троицкий административный округ', 'Одинцовский',
       'Богородский', 'Данные отсутствуют', 'Красногорск',
       'Солнечногорск', 'Новомосковский административный округ',
       'Щёлково', 'Сергиево-Посадский', 'Подольск', 'Можайский',
       'Павловский Посад', 'Пушкинский', 'Люберцы', 'Клин',
       'Волоколамский', 'Мытищи', 'Балашиха', 'Воскресенск',
       'Наро-Фоминский', 'Лосино-Петровский', 'Ступино', 'Черноголовка',
       'Луховицы', 'Орехово-Зуевский', 'Электросталь', 'Талдомский',
       'Серпухов', 'Кашира', 'Шаховская', 'Зарайск', 'Коломенский',
       'Лотошино', 'Рузский', 'Егорьевск', 'Шатура', 'Краснознаменск',
       'Озёры', 'Серебряные Пруды']

MAIN_SHOSSES = ['Новорязанское шоссе', 'Рогачёвское шоссе', 'Новокаширское шоссе',
       'Волоколамское шоссе', 'Дмитровское шоссе', 'Егорьевское шоссе',
       'Симферопольское шоссе', 'Киевское шоссе', 'Можайское шоссе',
       'Носовихинское шоссе', 'Пятницкое шоссе', 'Каширское шоссе',
       'Ленинградское шоссе', 'Варшавское шоссе', 'Щёлковское шоссе',
       'Ярославское шоссе', 'Рязанское шоссе', 'Минское шоссе',
       'Быковское шоссе', 'Калужское шоссе', 'Горьковское шоссе',
       'Новорижское шоссе', 'Успенское шоссе', 'Осташковское шоссе',
       'Алтуфьевское шоссе', 'Новосходненское шоссе', 'Ильинское шоссе',
       'Боровское шоссе', 'Фряновское шоссе', 'Куркинское шоссе']

loc_mkad = {'Дмитровское шоссе':[55.907885, 37.544415],'Новорязанское шоссе':[55.686721, 37.831275],
            'Рогачёвское шоссе':[55.908118, 37.543538],'Новокаширское шоссе':[55.575721, 37.688375],
            'Волоколамское шоссе':[55.831974, 37.395436], 'Егорьевское шоссе':[55.708083, 37.834006],
            'Симферопольское шоссе':[55.575988, 37.596946], 'Киевское шоссе':[55.638882, 37.459486],
            'Можайское шоссе':[55.713532, 37.386122], 'Носовихинское шоссе':[55.744193, 37.841924],
            'Пятницкое шоссе':[55.832574, 37.393725], 'Каширское шоссе':[55.591747, 37.729931],
            'Ленинградское шоссе':[55.883944, 37.441925], 'Варшавское шоссе':[55.571605, 37.597860],
            'Щёлковское шоссе':[55.813980, 37.838782], 'Ярославское шоссе':[55.882639, 37.725777],
            'Рязанское шоссе':[55.707734, 37.836560], 'Минское шоссе':[55.712719, 37.380796],
            'Быковское шоссе':[55.707678, 37.835177], 'Калужское шоссе':[55.610016, 37.490083],
            'Горьковское шоссе':[55.778060, 37.846869], 'Новорижское шоссе':[55.789824, 37.371454],
            'Успенское шоссе':[55.765812, 37.373779], 'Осташковское шоссе':[55.894963, 37.672753],
            'Алтуфьевское шоссе':[55.909921, 37.588725], 'Новосходненское шоссе':[55.881482, 37.444302],
            'Ильинское шоссе':[55.789880, 37.372298], 'Фряновское шоссе':[55.813703, 37.838854],
            'Боровское шоссе':[55.662376, 37.432093], 'Куркинское шоссе':[55.870744, 37.411918]
            }

with open('place_all.bin', "rb") as file:
    PLACE_ALL = pickle.load(file)

def code_categorical(x, list_name):
       dict_data = {}
       for num, value in enumerate(list_name):
              dict_data[value] = num

       code_region = to_categorical(dict_data[x], len(dict_data)).astype('int')
       return code_region


def get_loc_yandex(place_row):
       try:
              oblast = place_row[0]
              gorodskoi_okrug = f'Городской округ {place_row[1]}'
              if gorodskoi_okrug.find('Данные отсутствуют') > -1:
                     gorodskoi_okrug = ""
              elif gorodskoi_okrug.find('административный округ') > -1:
                     gorodskoi_okrug = place_row[1]

              selo = place_row[2]
              full_name = f'{oblast} {gorodskoi_okrug} {selo}'

              geolocator = Yandex(api_key='77b9b6b9-a198-4054-910e-b008211e74fd',
                                  user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
              location = geolocator.geocode(full_name, timeout=5)

              return location.latitude, location.longitude

       except IndexError as ex:
              print(ex)
              print("Не удалось получить локацию .")
              return 0, 0

def distance_categorical(arg):
  if arg < 51:
      arg_group = arg // 5
  elif arg > 50:
      arg_group = 10
  ohe_arg = to_categorical(arg_group, 11)
  return  ohe_arg

path_Sc_square = 'yScaler_square.bin'
with open(path_Sc_square, "rb") as file:
  yScaler_square = pickle.load(file)

def square_scaled(num):
  global yScaler_square
  num = np.array(num)
  square_norm = yScaler_square.transform(num.reshape(-1, 1)).flatten()

  return float(square_norm)

path_Sc_latitude = 'yScaler_latitude.bin'
with open(path_Sc_latitude, "rb") as file:
  yScaler_latitude = pickle.load(file)

def latitude_scaled(num):
  global yScaler_latitude
  num = np.array(num)
  latitude_norm = yScaler_latitude.transform(num.reshape(-1, 1)).flatten()

  return float(latitude_norm)

path_Sc_longitude = 'yScaler_longitude.bin'
with open(path_Sc_longitude, "rb") as file:
  yScaler_longitude = pickle.load(file)

def longitude_scaled(num):
  global yScaler_longitude
  num = np.array(num)
  longitude_norm = yScaler_longitude.transform(num.reshape(-1, 1)).flatten()

  return float(longitude_norm)

with open('price_categor.bin', "rb") as file:
    PRICE_CATEGOR = pickle.load(file)

def fact_price(arg):
    global PRICE_CATEGOR
    for key, value in PRICE_CATEGOR.items():
        if value == arg:
            return key

