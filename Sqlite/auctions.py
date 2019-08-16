"""We analyze auctions data.

We analyze data from a json file using SQL queries.
To do this, the data was loaded into the sqlite3 database.
"""

from utils import create_connection, insert_row_data, get_from_db
import os
import json


path_to_app = os.path.dirname(os.path.realpath(__file__)) + os.sep


def get_data(path_to_data):
    """We get data from json file."""
    try:
        data = json.load(open(path_to_data, encoding='utf-8'))
    except Exception as err_load:
        print("Error json_load: ", err_load)
    else:
        if data[0].get('auctiondate'):
            result = []
            for i in range(len(data)):
                if data[i]['attraction'] > 0:
                    auctiondate = data[i]['auctiondate'].split(".")
                    # Convert date to desired (for strftime) format
                    # 24.03.2021 -> 2021-03-24
                    date_start = "-".join(auctiondate[::-1])
                    # PRIMARY KEY -> start_year, auct_num
                    start_year = int(auctiondate[2])
                    auct_num = int(data[i]['auctionnum'])
                    repaydate = data[i]['repaydate'].split(".")
                    # Convert date to desired (for strftime) format
                    date_end = "-".join(repaydate[::-1])
                    money = data[i]['attraction']
                    percent = data[i]['incomelevel']
                    val_code = data[i]['valcode'].strip()
                    stock_code = data[i]['stockcode'].strip()
                    row_data = (start_year, auct_num, date_start, date_end,
                                money, percent, val_code, stock_code
                                )
                    result.append(row_data)
            return result


def get_connect(db_file):
    """Get connect to the database."""
    db_schema = """
        CREATE TABLE IF NOT EXISTS auctions (
            start_year  integer not NULL,
            auct_num    integer not NULL,
            date_start  text not NULL,
            date_end    text not NULL,
            money       real not NULL,
            percent     real not NULL,
            val_code    text not NULL,
            stock_code  text not NULL,
            PRIMARY KEY (start_year, auct_num)
        );
    """
    return create_connection(db_file, db_schema)


def insert_data(conn, data_file):
    """We connect to the database and record data."""
    check_data = "SELECT * FROM auctions WHERE start_year = ? AND auct_num = ?;"
    insert_data = "INSERT INTO auctions (start_year, auct_num, \
                                            date_start, date_end, money, percent, \
                                            val_code, stock_code) \
                                           VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    data = get_data(data_file)
    if data:
        for row in data:
            id_exists = get_from_db(conn, check_data, (row[1], row[2]))
            if not id_exists:
                insert_row_data(conn, insert_data, row)
        if conn.total_changes:
            conn.commit()
        print("\nRows in data: {0}.\nTotal changes: {1}\n".format(len(data), conn.total_changes))


def get_valcode(conn):
    """Get a dataset valcode: ['UAH', 'USD', 'EUR']."""
    get_valcode = "SELECT val_code FROM auctions \
                                GROUP BY val_code \
                                ORDER BY val_code DESC;"
    return [x[0] for x in get_from_db(conn, get_valcode)]


def show_result(title, val_code, data):
    """Print data."""
    print("{:6} {:<6} {}, {}".format(title, 'Count', 'Money', val_code))
    print("{:6} {:<6} {}".format('-' * 4, '-' * 5, '-' * 10))
    for row in data:
        period, count, money = row
        print("{:6} {:^6} {}".format(period, count, round(money, 2)))
    print()


def auctions_stats(conn, in_out):
    """We make a report on all auctions."""
    dic_in_out = {'in': 'date_start',
                  'out': 'date_end'
                  }
    get_stats = "SELECT strftime('%Y', {}) as year, COUNT(), SUM(money) \
                                FROM auctions \
                                WHERE val_code = ? \
                                GROUP BY year \
                                ORDER BY year ASC;".format(dic_in_out.get(in_out))
    if in_out in dic_in_out.keys():
        print("\n=== Money {} ===".format(in_out.upper()))
        print()
        for val_code in get_valcode(conn):
            data = []
            for row in get_from_db(conn, get_stats, (val_code, )):
                if int(row[0]) > 2011:
                    data.append(row)

            show_result('Year', val_code, data)


def auctions_year(conn, year, in_out):
    """We draw up an auction report for the year."""
    dic_in_out = {'in': 'date_start',
                  'out': 'date_end'
                  }
    get_months = "SELECT strftime('%m', date_start) as month FROM auctions \
                                GROUP BY month \
                                ORDER BY month ASC;"
    get_stats = "SELECT strftime('%m', {0}) as month, COUNT(), SUM(money) \
                                FROM auctions \
                                WHERE val_code = ? AND {0} LIKE ? \
                                GROUP BY month \
                                ORDER BY month ASC;".format(dic_in_out.get(in_out))
    if in_out in dic_in_out.keys():
        print("\n= Money {} / Year: {} =".format(in_out.upper(), year))
        print()
        for val_code in get_valcode(conn):
            data = []
            months = [x[0] for x in get_from_db(conn, get_months)]
            for month in months:
                x = str(year) + '-' + month + '-__'
                answer = get_from_db(conn, get_stats, (val_code, x))
                if answer:
                    data.append(answer[0])
                else:
                    data.append((month, 0, 0))

            show_result('Month', val_code, data)


if __name__ == '__main__':
    data_file = path_to_app + 'auctions.json'
    db_file = path_to_app + 'auctions.db'
    conn = get_connect(db_file)
    if conn:
        if os.path.exists(data_file):
            insert_data(conn, data_file)
        # auctions_stats(conn, in_out='in')
        auctions_stats(conn, in_out='out')
        auctions_year(conn, 2018, in_out='in')
        conn.close()
