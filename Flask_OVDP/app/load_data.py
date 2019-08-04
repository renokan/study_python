#!/home/renokan/flask-ovdp/venv/bin/python3
"""Load data for flask_ovdp."""

import os
import json
import requests
from datetime import datetime
import pygal
from pygal.style import Style
custom_style = Style(colors=('#0d00d6', '#ff0000'),
                     background='#ffffff'
                     )

path_to_app = os.path.dirname(os.path.realpath(__file__)) + os.sep
path_to_log = path_to_app + 'update_data.log'
path_to_json = path_to_app + 'db_auctions.json'
path_to_report = path_to_app + 'static' + os.sep + 'reports' + os.sep

info_auctions = {}


def save_log(logging=None):
    """Saving log."""
    if logging:
        with open(path_to_log, 'a', encoding='utf-8') as data_log:
            dtime = datetime.today().strftime('%d-%m-%Y %H:%M')
            data_log.write('\n' + dtime + '\t' + logging)


def load_data():
    """Loading data."""
    try:
        request_get = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/ovdp?json')
    except requests.exceptions.RequestException:
        return "load_data(): Error loading data from bank.gov.ua source."
    else:
        try:
            with open(path_to_json, 'w', encoding='utf-8') as local_json:
                local_json.write(request_get.text)
        except Exception:
            return "load_data(): Error opening or writing to db_auctions.json file."
        else:
            return "load_data(): Download to db_auctions.json completed."


def convert_data():
    """Converting data."""
    try:
        data = json.load(open(path_to_json, encoding='utf-8'))
    except Exception:
        return "convert_data(): Error load db_auctions.json file."
    else:
        if data[0].get('auctiondate'):
            for i in range(len(data)):
                auct_year = int(data[i]['auctiondate'].split(".")[2])
                auct_num = data[i]['auctionnum']
                info_auctions[(auct_year, auct_num)] = data[i]
            return "convert_data(): Converting data from the db_auctions.json file is complete."
        else:
            return "convert_data(): Error converting from local file. No key='auctiondate'."


def auctions_stat():
    """General auction statistics."""
    uah_in = {}
    uah_out = {}
    usd_in = {}
    usd_out = {}
    eur_in = {}
    eur_out = {}
    for value in info_auctions.values():
        year_auct = int(value['auctiondate'].split(".")[2])
        year_repay = int(value['repaydate'].split(".")[2])
        money = value['attraction']
        if money > 0:
            if value['valcode'] == 'UAH':
                if uah_in.get(year_auct) is None:
                    uah_in[year_auct] = []
                if uah_out.get(year_repay) is None:
                    uah_out[year_repay] = []
                uah_in[year_auct].append(money)
                uah_out[year_repay].append(money)
            elif value['valcode'] == 'USD':
                if usd_in.get(year_auct) is None:
                    usd_in[year_auct] = []
                if usd_out.get(year_repay) is None:
                    usd_out[year_repay] = []
                usd_in[year_auct].append(money)
                usd_out[year_repay].append(money)
            elif value['valcode'] == 'EUR':
                if eur_in.get(year_auct) is None:
                    eur_in[year_auct] = []
                if eur_out.get(year_repay) is None:
                    eur_out[year_repay] = []
                eur_in[year_auct].append(money)
                eur_out[year_repay].append(money)

    if uah_in or uah_out or usd_in or usd_out or eur_in or eur_out:
        if uah_in or uah_out:
            uah_chart = pygal.Bar(style=custom_style, x_label_rotation=50)
            uah_chart.title = 'Currency UAH, billion'
            years = list(set(uah_in.keys()).union(set(uah_out.keys())))
            years = [x for x in years if x > 2011]
            years.sort()
            data_in = []
            data_out = []
            for x in years:
                if uah_in.get(x):
                    data_in.append(round(sum(uah_in.get(x)) / 1000000000))
                else:
                    data_in.append(0)
                if uah_out.get(x):
                    data_out.append(round(sum(uah_out.get(x)) / 1000000000))
                else:
                    data_out.append(0)
            uah_chart.x_labels = map(str, years)
            uah_chart.add('In', data_in)
            uah_chart.add('Out', data_out)
            uah_chart.render_to_file(path_to_report + 'report_stat_uah.svg')
        if usd_in or usd_out:
            usd_chart = pygal.Bar(style=custom_style)
            usd_chart.title = 'Currency USD, million'
            years = list(set(usd_in.keys()).union(set(usd_out.keys())))
            years.sort()
            data_in = []
            data_out = []
            for x in years:
                if usd_in.get(x):
                    data_in.append(round(sum(usd_in.get(x)) / 1000000))
                else:
                    data_in.append(0)
                if usd_out.get(x):
                    data_out.append(round(sum(usd_out.get(x)) / 1000000))
                else:
                    data_out.append(0)
            usd_chart.x_labels = map(str, years)
            usd_chart.add('In', data_in)
            usd_chart.add('Out', data_out)
            usd_chart.render_to_file(path_to_report + 'report_stat_usd.svg')
        if eur_in or eur_out:
            eur_chart = pygal.Bar(style=custom_style)
            eur_chart.title = 'Currency EUR, million'
            years = list(set(eur_in.keys()).union(set(eur_out.keys())))
            years.sort()
            data_in = []
            data_out = []
            for x in years:
                if eur_in.get(x):
                    data_in.append(round(sum(eur_in.get(x)) / 1000000))
                else:
                    data_in.append(0)
                if eur_out.get(x):
                    data_out.append(round(sum(eur_out.get(x)) / 1000000))
                else:
                    data_out.append(0)
            eur_chart.x_labels = map(str, years)
            eur_chart.add('In', data_in)
            eur_chart.add('Out', data_out)
            eur_chart.render_to_file(path_to_report + 'report_stat_eur.svg')

        return "auctions_stat(): The report is ready."
    else:
        return "auctions_stat(): No data."


def auctions_year(check_year=None):
    """Auction statistics for the year."""
    if check_year:
        uah_in = {}
        uah_out = {}
        usd_in = {}
        usd_out = {}
        eur_in = {}
        eur_out = {}
        for value in info_auctions.values():
            year_auct = int(value['auctiondate'].split(".")[2])
            year_repay = int(value['repaydate'].split(".")[2])
            money = value['attraction']
            if check_year == year_auct:
                if money > 0:
                    month_auct = int(value['auctiondate'].split(".")[1])
                    if value['valcode'] == 'UAH':
                        if uah_in.get(month_auct) is None:
                            uah_in[month_auct] = []
                        uah_in[month_auct].append(money)
                    elif value['valcode'] == 'USD':
                        if usd_in.get(month_auct) is None:
                            usd_in[month_auct] = []
                        usd_in[month_auct].append(money)
                    elif value['valcode'] == 'EUR':
                        if eur_in.get(month_auct) is None:
                            eur_in[month_auct] = []
                        eur_in[month_auct].append(money)
            if check_year == year_repay:
                if money > 0:
                    month_repay = int(value['repaydate'].split(".")[1])
                    if value['valcode'] == 'UAH':
                        if uah_out.get(month_repay) is None:
                            uah_out[month_repay] = []
                        uah_out[month_repay].append(money)
                    elif value['valcode'] == 'USD':
                        if usd_out.get(month_repay) is None:
                            usd_out[month_repay] = []
                        usd_out[month_repay].append(money)
                    elif value['valcode'] == 'EUR':
                        if eur_out.get(month_repay) is None:
                            eur_out[month_repay] = []
                        eur_out[month_repay].append(money)

        if uah_in or uah_out or usd_in or usd_out or eur_in or eur_out:
            months = [i for i in range(1, 13)]
            if uah_in or uah_out:
                uah_chart = pygal.Bar(style=custom_style)
                uah_chart.title = 'Year: {} - Currency UAH, billion'.format(check_year)
                data_in = []
                data_out = []
                for x in months:
                    if uah_in.get(x):
                        data_in.append(round(sum(uah_in.get(x)) / 1000000000))
                    else:
                        data_in.append(0)
                    if uah_out.get(x):
                        data_out.append(round(sum(uah_out.get(x)) / 1000000000))
                    else:
                        data_out.append(0)
                uah_chart.x_labels = map(str, months)
                uah_chart.add('In', data_in)
                uah_chart.add('Out', data_out)
                uah_chart.render_to_file(path_to_report + 'report_' + str(check_year) + '_uah.svg')
            if usd_in or usd_out:
                usd_chart = pygal.Bar(style=custom_style)
                usd_chart.title = 'Year: {} - Currency USD, million'.format(check_year)
                data_in = []
                data_out = []
                for x in months:
                    if usd_in.get(x):
                        data_in.append(round(sum(usd_in.get(x)) / 1000000))
                    else:
                        data_in.append(0)
                    if usd_out.get(x):
                        data_out.append(round(sum(usd_out.get(x)) / 1000000))
                    else:
                        data_out.append(0)
                usd_chart.x_labels = map(str, months)
                usd_chart.add('In', data_in)
                usd_chart.add('Out', data_out)
                usd_chart.render_to_file(path_to_report + 'report_' + str(check_year) + '_usd.svg')
            if eur_in or eur_out:
                eur_chart = pygal.Bar(style=custom_style)
                eur_chart.title = 'Year: {} - Currency EUR, million'.format(check_year)
                data_in = []
                data_out = []
                for x in months:
                    if eur_in.get(x):
                        data_in.append(round(sum(eur_in.get(x)) / 1000000))
                    else:
                        data_in.append(0)
                    if eur_out.get(x):
                        data_out.append(round(sum(eur_out.get(x)) / 1000000))
                    else:
                        data_out.append(0)
                eur_chart.x_labels = map(str, months)
                eur_chart.add('In', data_in)
                eur_chart.add('Out', data_out)
                eur_chart.render_to_file(path_to_report + 'report_' + str(check_year) + '_eur.svg')

            return "auctions_year(): The report is ready."
        else:
            return "auctions_year(): For this parameter '{}' - no data.".format(check_year)
    else:
        return "auctions_year(): There is no year for data analysis."


if __name__ == '__main__':
    save_log(load_data())
    save_log(convert_data())
    save_log(auctions_stat())
    save_log(auctions_year(2019))
