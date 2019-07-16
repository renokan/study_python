"""OVDP / Отчет по аукционам ОВГЗ.

Что анализируем: Результати розміщення облігацій внутрішніх державних позик.

Источник данных: API (в формате json) Национального банка Украины (НБУ).

Что хотим узнать: Сколько денег получено (за период) в рамках аукционов и сколько
                  нужно вернуть (за период).

Чего нет в цифрах: Не анализируются выплаченные проценты, т.е. суммируем
                   значения "Залучено коштів від розміщення облігацій" для
                   даты "розміщення облігацій" и эту же сумму для даты
                   "термін погашення облігацій".

Описание терминов: "In" - получено денег; "Out" - нужно вернуть;
                   billion - млрд. грн; million - млн. USD/EUR.
"""
from lib_ovdp import check_data, info_auctions, path_to_db
from lib_ovdp import os


def auctions_stat():
    """Общая информация по аукционам."""
    uah_in = {}   # для данных по аукционам в грн (по годам)
    uah_out = {}  # это для данных по выплатам (по годам)
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

    uah_chart = pygal.Bar(style=custom_style, x_label_rotation=50)
    uah_chart.title = 'Currency UAH, billion'
    years = list(set(uah_in.keys()).union(set(uah_out.keys())))
    years = [x for x in years if x > 2008]
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
    uah_chart.render_to_file(path_to_report + 'svg_report_uah.svg')

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
    usd_chart.render_to_file(path_to_report + 'svg_report_usd.svg')

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
    eur_chart.render_to_file(path_to_report + 'svg_report_eur.svg')


if __name__ == '__main__':
    check = check_data()
    if check:
        print(check)
    else:
        path_to_report = path_to_db + 'report' + os.sep
        if os.path.isdir(path_to_report):
            try:
                import pygal
                from pygal.style import Style
            except ImportError as error_import:
                print("\n\n\tError:", error_import, "\n")
            else:
                custom_style = Style(colors=('#0d00d6', '#ff0000'),
                                     background='#ffffff'
                                     )
                auctions_stat()
        else:
            print("\n\n\tError: No directory", path_to_report, "\n")
