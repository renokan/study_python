"""Library for OVDP.py / Библиотека для программы OVDP.

В def load_db() импортируем модуль requests, должен быть установлен отдельно.
Если же работать с локальными данными (*.json) - requests не требуется.
Для обновления данных нужно удалить файлы *.json и запустить программу.
"""

import os
import json

load_data = {'stocks': {'name_db': 'db_stocks.json',
                        'load': 'https://bank.gov.ua/depo_securities?json',
                        'date': ''
                        },
             'auctions': {'name_db': 'db_auctions.json',
                          'load': 'https://bank.gov.ua/NBUStatService/v1/statdirectory/ovdp?json',
                          'date': ''
                          }
             }
# Ищем путь, где установлена программа, для записи данных (*.json)
path_to_db = os.path.dirname(os.path.realpath(__file__)) + os.sep
# Конвертируемые данные храним в словарях
info_stocks = {}
info_auctions = {}


def convert_stocks():
    """Конвертируем данные из строки (в файле) в словарь."""
    try:
        data = json.load(open(path_to_db + load_data['stocks']['name_db'], encoding='utf-8'))
    except Exception as error_c:
        return error_c
    else:
        for i in data:
            if i.get('cpcode'):
                info_stocks[i['cpcode']] = i
                # 'UA4000063010': {'cpcode': 'UA4000063010',
                #                  'emit_name': 'МІН ФІН',
                #                  'pay_period': 182, 'pgs_date': '11.03.2020',
                #                  'payments': [{'pay_val': 21.92, 'pay_type': '1',
                #                                'pay_date': '24.03.2010', 'array': 'true'},
            else:
                return "Error converting from local file. No key='cpcode'."


def convert_auctions():
    """Конвертируем данные из строки (в файле) в словарь."""
    try:
        data = json.load(open(path_to_db + load_data['auctions']['name_db'], encoding='utf-8'))
    except Exception as error_c:
        return error_c
    else:
        if data[0].get('auctiondate'):
            for i in range(len(data)):
                auct_year = int(data[i]['auctiondate'].split(".")[2])
                auct_num = data[i]['auctionnum']
                info_auctions[(auct_year, auct_num)] = data[i]
        else:
            return "Error converting from local file. No key='auctiondate'."


def load_db():
    """Загружаем данные."""
    # Импортируем requests когда он нужен, так работаем с локальной базой
    import requests
    try:
        stocks_temp = requests.get(load_data['stocks']['load'])
        # >>> stocks_temp.headers
        # 'content-type': 'application/json; encoding=utf-8',
        # 'content-language': 'uk-UA',
        # 'date': 'Thu, 11 Jul 2019 13:41:03 GMT',
        # 'statusrequest': 'OK+%C2%E8%EA%EE%ED%E0%ED%EE'
        #
        # >>> stocks_temp.headers.get('date')
        # 'Thu, 11 Jul 2019 13:41:03 GMT'
    except requests.exceptions.RequestException as error_re:
        # requests.exceptions.HTTPError
        # requests.exceptions.ConnectionError
        # requests.exceptions.ConnectTimeout
        # requests.exceptions.ReadTimeout
        return error_re
    else:
        stocks_data = stocks_temp.text
        # stocks_temp.json()
        # stocks_temp.content
        stocks_file = path_to_db + load_data['stocks']['name_db']

    try:
        auctions_temp = requests.get(load_data['auctions']['load'])
    except requests.exceptions.RequestException as error_re:
        return error_re
    else:
        auctions_data = auctions_temp.text
        auctions_file = path_to_db + load_data['auctions']['name_db']

    try:
        pass
        with open(stocks_file, 'w') as db_s, open(auctions_file, 'w') as db_a:
            db_s.write(stocks_data)
            db_a.write(auctions_data)
    except Exception:
        return "Error saving to local file."
    else:
        load_data['stocks']['date'] = stocks_temp.headers.get('date')
        load_data['auctions']['date'] = auctions_temp.headers.get('date')

    # Дампим текущее стостояние баз
    db_status = path_to_db + 'db_status.json'
    json.dump(load_data, open(db_status, 'w'), indent=4)


def check_data():
    """Проверяем наличие данных, если их нет - пробуем загрузить."""
    check_stocks = convert_stocks()
    check_auction = convert_auctions()
    if check_stocks or check_auction:
        check_load = load_db()
        if check_load:
            return "No data. Error loading from external source."
        else:
            check_stocks = convert_stocks()
            check_auction = convert_auctions()
            if check_stocks or check_auction:
                return "No data. Error converting from local file."
