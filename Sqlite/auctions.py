"""We analyze auctions data.

We analyze data from a json file using SQL queries.
To do this, the data was loaded into the sqlite3 database.
"""

from utils import create_connection, insert_in_db, get_from_db, init_db
import os
import json
import re

basedir = os.path.abspath(os.path.dirname(__file__))

DATA_FILE = os.path.join(basedir, 'auctions.json')
DB_FILE = os.path.join(basedir, 'auctions.db')
REPORT_FILE = os.path.join(basedir, 'auctions.txt')
# To save report (status=True) or not (status=False) - only print data.
DEFAULT_SAVE = False
save_report = {'status': DEFAULT_SAVE,
               'path': REPORT_FILE}


def show_report(data=None, mode_open='a'):
    """We display or save a report."""
    if save_report['status'] is True:
        try:
            with open(save_report['path'], mode_open, encoding='utf-8') as report:
                if data:
                    report.write(data + "\n")
                else:
                    report.write("\n")
        except Exception as err:
            return "Open/Write Error: {}".format(str(err))
        else:
            return True
    else:
        if data:
            print(data)
        else:
            print()


def check_date(date_string):
    """We check the date and change the format (for strftime) if necessary."""
    if re.search(r'\d\d\d\d-\d\d-\d\d', date_string):
        # 2021-03-24 -> Ok
        return date_string
    if re.search(r'\d\d\d\d\.\d\d\.\d\d', date_string):
        # 2021.03.24 -> 2021-03-24 -> Ok
        temp = date_string.split(".")
        return "-".join(temp)
    if re.search(r'\d\d\.\d\d\.\d\d\d\d', date_string):
        # 24.03.2021 -> 2021-03-24 -> Ok
        temp = date_string.split(".")
        return "-".join(temp[::-1])


def get_data(path_to_data):
    """We get data from json file."""
    try:
        data = json.load(open(path_to_data, encoding='utf-8'))
    except Exception as err_load:
        show_report("Error json_load: {}".format(str(err_load)))
    else:
        if data[0].get('auctiondate'):
            result = []
            for i in range(len(data)):
                if data[i]['attraction'] > 0:
                    auct_num = data[i]['auctionnum']
                    date_in = check_date(data[i]['auctiondate'])
                    date_out = check_date(data[i]['repaydate'])
                    money = data[i]['attraction']
                    percent = data[i]['incomelevel']
                    val_code = data[i]['valcode'].strip()
                    stock_code = data[i]['stockcode'].strip()
                    # Collect data in a tuple.
                    row_data = (auct_num, date_in, date_out,
                                money, percent, val_code, stock_code)
                    result.append(row_data)
            return result


def get_connect(db_file):
    """Get connect to the database."""
    db_schema = """
        CREATE TABLE IF NOT EXISTS auctions (
            auct_num    integer not NULL,
            date_in     text not NULL,
            date_out    text not NULL,
            money       real not NULL,
            percent     real not NULL,
            val_code    text not NULL,
            stock_code  text not NULL,
            PRIMARY KEY (auct_num, date_in)
        );
    """
    if not os.path.exists(db_file):
        result = init_db(db_file, db_schema)
        if result is not True:
            show_report("Database initialization error: {}".format(result))
    return create_connection(db_file)


def insert_data(conn, data_file):
    """We connect to the database and record data."""
    check_data = "SELECT * FROM auctions WHERE auct_num = ? AND date_in = ?;"
    insert_data = "INSERT INTO auctions (auct_num, date_in, date_out, money, \
                                            percent, val_code, stock_code) \
                                         VALUES (?, ?, ?, ?, ?, ?, ?);"
    data = get_data(data_file)
    if data:
        PRIMARY_KEY = slice(0, 2)
        for row in data:
            id_exists = get_from_db(conn, check_data, row[PRIMARY_KEY])
            if not id_exists:
                insert_in_db(conn, insert_data, row)
        if conn.total_changes:
            conn.commit()
            # show_report the result.
            show_report()
            show_report("Rows in data: {}".format(len(data)))
            show_report("Total changes: {}".format(conn.total_changes))
            show_report()


def get_valcode(conn):
    """Get a dataset valcode: ['UAH', 'USD', 'EUR']."""
    get_valcode = "SELECT DISTINCT val_code FROM auctions \
                                            ORDER BY val_code DESC;"
    return [x[0] for x in get_from_db(conn, get_valcode)]


def get_date_inout(in_out_key):
    """Get a dataset date_(in/out)."""
    in_out = {'in': 'date_in',
              'out': 'date_out'}
    return in_out.get(in_out_key)


def show_result(title, val_code, data):
    """Show report data."""
    show_report("{:^7} {:<6} {}, {}".format(title, 'Count', 'Money', val_code))
    show_report("{:^7} {:<6} {}".format('-' * 7, '-' * 5, '-' * 10))
    for row in data:
        period, count, money = row
        money = round(money, 2)
        show_report("{:^7} {:^6} {}".format(period, count, money))
    show_report()


def auctions_stats(conn, in_out):
    """We make a report on all auctions."""
    column_inout = get_date_inout(in_out)
    if not column_inout:
        show_report("Invalid parameter '{}' in function 'auctions_stats()'.".format(in_out))
        return False

    # We can't make a year selection "> 2011" in the request,
    # because then the SUM(money) is erroneously calculated.
    query = "SELECT CAST(strftime('%Y', {}) as INTEGER) as year, COUNT(), SUM(money) \
                                    FROM auctions \
                                    WHERE val_code = ? \
                                    GROUP BY year \
                                    ORDER BY year ASC;".format(column_inout)

    show_report("\n=== Money {} ===".format(in_out.upper()))
    show_report()
    for val_code in get_valcode(conn):
        data = get_from_db(conn, query, (val_code, ))
        result = [row for row in data if row[0] > 2011]
        show_result('Year', val_code, result)


def auctions_year(conn, year, in_out):
    """We draw up an auction report for the year."""
    column_inout = get_date_inout(in_out)
    if not column_inout:
        show_report("Invalid parameter '{}' in function 'auctions_year()'.".format(in_out))
        return False

    query = "SELECT CAST(strftime('%m', {0}) as INTEGER) as month, COUNT(), SUM(money) \
                            FROM auctions \
                            WHERE val_code = ? AND  \
                                  CAST(strftime('%Y', {0}) as INTEGER) = ? \
                            GROUP BY month \
                            ORDER BY month ASC;".format(column_inout)

    show_report("\n= Money {} / Year: {} =".format(in_out.upper(), year))
    show_report()
    for val_code in get_valcode(conn):
        result = []
        data = get_from_db(conn, query, (val_code, year))
        for month in range(1, 13):
            count = 0
            money = 0
            for row in data:
                if row[0] == month:
                    _, count, money = row
            result.append((month, count, money))
        show_result('Month', val_code, result)


def auctions_all(conn):
    """We get all the records."""
    get_all = "SELECT * FROM auctions \
                        WHERE CAST(strftime('%Y', date_in) as INTEGER) > 2011 \
                        ORDER BY date_in DESC, auct_num DESC;"
    for row in get_from_db(conn, get_all):
        show_report(row)


def auctions_paginated(conn):
    """We get paginated reports."""
    def paginate(item_all, item_qty, page=1):
        if not item_all:
            raise ConnectionError

        pages = len(item_all[::item_qty])
        if page < 1 or page > pages:
            raise ValueError

        page_prev = None
        page_next = None
        slice_start = None
        slice_end = None
        if pages != 1:
            if page == 1:
                page_next = page + 1
                slice_end = page * item_qty
            elif page == pages:
                page_prev = page - 1
                slice_start = ((page - 1) * item_qty)
            else:
                page_prev = page - 1
                page_next = page + 1
                slice_start = ((page - 1) * item_qty)
                slice_end = (page * item_qty)
        data = item_all[slice_start:slice_end]

        output = {'page': page, 'pages': pages,
                  'previous': page_prev, 'next': page_next,
                  'data': data}

        return output

    query = "SELECT * FROM auctions \
                      WHERE CAST(strftime('%Y', date_in) as INTEGER) > 2011 \
                      ORDER BY date_in DESC, auct_num DESC;"
    item_qty = 16
    page = 1
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        item_all = cursor.fetchall()
        result = paginate(item_all, item_qty, page)
    except ConnectionError:
        print("No Items. Error 500.")
    except ValueError:
        print("Error param. Error 404.")
    else:
        print("Code 200.")
        print(result)


def auctions_report(conn, to_save=DEFAULT_SAVE):
    """We prepare reports."""
    if to_save is True:
        save_report['status'] = True
        empty_report = show_report(mode_open='w')
        if empty_report is not True:
            save_report['status'] = DEFAULT_SAVE
            print(empty_report)
            return False
    else:
        save_report['status'] = DEFAULT_SAVE

    auctions_stats(conn, in_out='in')
    auctions_stats(conn, in_out='out')
    # auctions_year(conn, 2018, in_out='in')
    # auctions_year(conn, 2018, in_out='out')
    # auctions_all(conn)
    # auctions_paginated(conn)


if __name__ == '__main__':
    conn = get_connect(DB_FILE)
    if conn:
        if os.path.exists(DATA_FILE):
            insert_data(conn, DATA_FILE)
        auctions_report(conn)
        # auctions_report(conn, to_save=True)
        conn.close()
