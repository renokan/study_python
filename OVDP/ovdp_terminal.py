"""OVDP / Данные по ОВГЗ.

Что анализируем:
    1. Результати розміщення облігацій внутрішніх державних позик / auctions
    2. Довідник державних цінних паперів та облігацій місцевих позик / stocks

Источник данных: API (в формате json) Национального банка Украины (НБУ).

Особенности реализации:
    Для обновления данных нужно удалить файлы *.json и запустить программу.
    Важно!!! Для обновления нужен модуль requests, должен быть установлен отдельно.
    Если же работать с локальными данными (*.json) - requests не требуется.
"""

from lib_ovdp import check_data, info_stocks, info_auctions


def stocks_stat():
    """Общая информация по справочнику ISIN."""
    valcode = []
    cptype = []
    cpdescr = []
    emitname = []
    for value in info_stocks.values():
        valcode.append(value['val_code'])
        cptype.append(value['cptype'])
        cpdescr.append(value['cpdescr'])
        emitname.append(value['emit_name'])

    if valcode or cptype or cpdescr or emitname:
        # Готовим данные
        output = []
        # Считаем данные по номиналам
        if valcode:
            stat_valcode = {key: valcode.count(key) for key in set(valcode)}
            output.append("Кіл\tНомінал (UAH/USD/EUR) цінних паперів")
            output.append("---\t---------------")
            for key, value in sorted(stat_valcode.items(), reverse=True, key=lambda x: x[1]):
                output.append("{0}\t{1}".format(value, key))
            output.append("")
        # Считаем данные по типам ЦП
        if cptype:
            stat_cptype = {key: cptype.count(key) for key in set(cptype)}
            output.append("Кіл\tТип ЦП цінних паперів")
            output.append("---\t---------------")
            for key, value in sorted(stat_cptype.items(), reverse=True, key=lambda x: x[1]):
                if key == 'DCP':
                    key += ' / облігації внутрішньої ДП'
                if key == 'OMP':
                    key += ' / облігації місцевих позик'
                if key == 'OZDP':
                    key += ' / облігації зовнішньої ДП'
                output.append("{0}\t{1}".format(value, key))
            output.append("")
        # Считаем данные по видам ЦП
        if cpdescr:
            stat_cpdescr = {key: cpdescr.count(key) for key in set(cpdescr)}
            output.append("Кіл\tВид ЦП цінних паперів")
            output.append("---\t---------------")
            for key, value in sorted(stat_cpdescr.items(), reverse=True, key=lambda x: x[1]):
                output.append("{0}\t{1}".format(value, key))
            output.append("")
        # Считаем данные по емітентам
        if emitname:
            stat_emitname = {key: emitname.count(key) for key in set(emitname)}
            output.append("Кіл\tЕмітент цінних паперів")
            output.append("---\t---------------")
            for key, value in sorted(stat_emitname.items(), reverse=True, key=lambda x: x[1]):
                output.append("{0}\t{1}".format(value, key))
            output.append("")
        # Возвращаем итоговые данные
        return output
    else:
        return "stocks_stat(): No data."


def stocks_isin(isin=None, pay_show=None):
    """Детальная информация по ISIN."""
    if isin:
        data = info_stocks.get(isin)
        if data:
            # Готовим данные
            output = []
            output.append("{} / ISIN цінного паперу".format(isin))
            output.append("Номінал\t{}".format(data['nominal']))
            output.append("Валюта\t{}".format(data['val_code']))
            output.append("Ставка\t{}%".format(data['auk_proc']))
            if data['cptype'] == 'DCP':
                cptype = '(облігації внутрішньої ДП)'
            elif data['cptype'] == 'OMP':
                cptype = '(облігації місцевих позик)'
            elif data['cptype'] == 'OZDP':
                cptype = '(облігації зовнішньої ДП)'
            else:
                cptype = ''
            output.append("Тип ЦП\t{0} {1}".format(data['cptype'], cptype))
            output.append("Вид ЦП\t{0}".format(data['cpdescr']))
            output.append("Емітент\t{0}".format(data['emit_name']))
            output.append("ЄДРПОУ\t{0}".format(data['emit_okpo']))
            output.append("Дата випуску\t{0}".format(data['val_date']))
            # Если нужно показать список платежей
            if pay_show == 'payments':
                payments = data['payments']
                for i in range(len(payments)):
                    output.append('')
                    output.append("\t{0} дата сплати".format(payments[i]['pay_date']))
                    output.append("\tтип виплати {0} (1–відсотки, 2-погаш., 3-достр.погаш)".format(payments[i]['pay_type']))
                    output.append("\t{0} {1} розмір купонного платежу на 1 ЦП".format(payments[i]['pay_val'], data['val_code']))
                output.append('')
            output.append("Дата погашення\t{0}".format(data['pgs_date']))
            # Возвращаем итоговые данные
            return output
        return "stocks_isin(): No data is available on this ISIN."
    return "stocks_isin(): Error data entry, not specified ISIN."


def auctions_stat():
    """Общая информация по аукционам."""
    uah_in = {}   # для данных по аукционам в грн (по годам)
    uah_out = {}  # это для данных по выплатам (по годам)
    usd_in = {}
    usd_out = {}
    eur_in = {}
    eur_out = {}
    auct_ok = 0  # считаем кол-во успешных аукционов, есть деньги
    auct_no = 0  # считаем кол-во тех, что закончились с 0-вой суммой
    for value in info_auctions.values():
        year_auct = int(value['auctiondate'].split(".")[2])
        year_repay = int(value['repaydate'].split(".")[2])
        money = value['attraction']
        if money > 0:
            auct_ok += 1
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
        else:
            auct_no += 1

    # print("auct_ok: ", auct_ok)  # 1576
    # print("auct_no: ", auct_no)  # 1377
    # print("auct_am: ", (auct_ok + auct_no))  # 2953

    if uah_in or uah_out or usd_in or usd_out or eur_in or eur_out:
        # Готовим данные
        output = []
        # "Получено денег"
        if uah_in:
            output.append("Год \tКол\tПолучено денег (UAH)")
            output.append("----\t---\t---------------------")
            for key, value in sorted(uah_in.items()):
                # round(sum(value)) --> 284665159.998555 --> 284665160
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        if usd_in:
            output.append("Год \tКол\tПолучено денег (USD)")
            output.append("----\t---\t---------------------")
            for key, value in sorted(usd_in.items()):
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        if eur_in:
            output.append("Год \tКол\tПолучено денег (EUR)")
            output.append("----\t---\t---------------------")
            for key, value in sorted(eur_in.items()):
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        # "Нужно вернуть"
        if uah_out:
            output.append("Год \tКол\tНужно вернуть (UAH)")
            output.append("----\t---\t-------------------")
            for key, value in sorted(uah_out.items()):
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        if usd_out:
            output.append("Год \tКол\tНужно вернуть (USD)")
            output.append("----\t---\t-------------------")
            for key, value in sorted(usd_out.items()):
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        if eur_out:
            output.append("Год \tКол\tНужно вернуть (EUR)")
            output.append("----\t---\t-------------------")
            for key, value in sorted(eur_out.items()):
                output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
            output.append("")
        # Возвращаем итоговые данные
        return output
    else:
        return "auctions_stat(): No data."


def auctions_year(check_year=None):
    """Общая информация по аукционам."""
    if check_year:
        uah_in = {}   # для данных по аукционам в грн (по месяцам)
        uah_out = {}  # это для данных по выплатам (по месяцам)
        usd_in = {}
        usd_out = {}
        eur_in = {}
        eur_out = {}
        auct_in = [0, 0]   # кол-во аукционов на привлечение (успешных и нет)
        auct_out = [0, 0]  # кол-во аукционов на выплаты (успешных и нет)
        for value in info_auctions.values():
            year_auct = int(value['auctiondate'].split(".")[2])
            year_repay = int(value['repaydate'].split(".")[2])
            money = value['attraction']
            if check_year == year_auct:
                if money > 0:
                    auct_in[0] += 1
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
                else:
                    auct_in[1] += 1
            if check_year == year_repay:
                if money > 0:
                    auct_out[0] += 1
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
                else:
                    auct_out[1] += 1

        # print("auct_in: ", auct_in)  # [285, 7] <-- 2019
        # print("auct_out: ", auct_out)  # [289, 89] <-- 2019
        # print("auct_am: ", ((auct_in[0] + auct_out[0]), auct_in[1] + auct_out[1]))  # (494, 96)

        if uah_in or uah_out or usd_in or usd_out or eur_in or eur_out:
            # Готовим данные
            output = []
            # "Получено денег"
            if uah_in:
                output.append("Мес\tКол\tПолучено денег (UAH)")
                output.append("---\t---\t---------------------")
                for key, value in sorted(uah_in.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            if usd_in:
                output.append("Мес\tКол\tПолучено денег (USD)")
                output.append("---\t---\t---------------------")
                for key, value in sorted(usd_in.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            if eur_in:
                output.append("Мес\tКол\tПолучено денег (EUR)")
                output.append("---\t---\t---------------------")
                for key, value in sorted(eur_in.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            # "Нужно вернуть"
            if uah_out:
                output.append("Мес\tКол\tНужно вернуть (UAH)")
                output.append("---\t---\t-------------------")
                for key, value in sorted(uah_out.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            if usd_out:
                output.append("Мес\tКол\tНужно вернуть (USD)")
                output.append("---\t---\t-------------------")
                for key, value in sorted(usd_out.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            if eur_out:
                output.append("Мес\tКол\tНужно вернуть (EUR)")
                output.append("---\t---\t-------------------")
                for key, value in sorted(eur_out.items()):
                    output.append("{0}\t{1}\t{2}".format(key, len(value), round(sum(value))))
                output.append("")
            # Возвращаем итоговые данные
            return output
        else:
            return "auctions_year(): For this parameter '{}' - no data.".format(check_year)
    return "auctions_year(): There is no year for data analysis."


def show(out=None):
    """Показываем результаты."""
    if out:
        if isinstance(out, str):
            print("\n\t{}\n".format(out))
        if isinstance(out, list):
            for line in out:
                print("\t{}".format(line))
    else:
        print()


if __name__ == '__main__':
    check = check_data()
    if check:
        show(check)
    else:
        show()

        show("Общая информация по аукционам.")
        show(auctions_stat())

        show_year = 2019
        show("Информация отдельно по {} году.".format(show_year))
        show(auctions_year(show_year))

        show("Общая информация по справочнику ISIN.")
        show(stocks_stat())

        import random
        show_isin = random.choice(list(info_stocks.keys()))
        # show_isin = 'UA4000204150'  # UA4000063010
        show("Пример вывода информации ISIN: {}".format(show_isin))
        show(stocks_isin(show_isin, 'payments'))

        show()
