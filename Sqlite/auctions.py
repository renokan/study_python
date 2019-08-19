"""We analyze auctions data.

We analyze data from a json file using SQL queries.
To do this, the data was loaded into the sqlite3 database.
"""

from utils import create_connection, insert_row_data, get_from_db
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

DATA_FILE = os.path.join(basedir, 'auctions.json')
DB_FILE = os.path.join(basedir, 'auctions.db')
REPORT_FILE = os.path.join(basedir, 'auctions.txt')

save_report = [False, REPORT_FILE]


def show_report(data=None, mode_open='a'):
    """We display or save a report."""
    if save_report[0] is True:
        path_to_report = save_report[1]
        try:
            with open(path_to_report, mode_open, encoding='utf-8') as report:
                if data:
                    report.write(data + "\n")
                else:
                    report.write("\n")
        except Exception as err:
            return "Open/Write Error: {}".format(err)
        else:
            return True
    else:
        if data:
            print(data)
        else:
            print()


def get_data(path_to_data):
    """We get data from json file."""
    try:
        data = json.load(open(path_to_data, encoding='utf-8'))
    except Exception as err_load:
        show_report("Error json_load: ", err_load)
    else:
        if data[0].get('auctiondate'):
            result = []
            for i in range(len(data)):
                if data[i]['attraction'] > 0:
                    auct_num = int(data[i]['auctionnum'])
                    auctiondate = data[i]['auctiondate'].split(".")
                    # Convert date to desired (for strftime) format
                    # 24.03.2021 -> 2021-03-24
                    date_in = "-".join(auctiondate[::-1])
                    repaydate = data[i]['repaydate'].split(".")
                    # Convert date to desired (for strftime) format
                    date_out = "-".join(repaydate[::-1])
                    money = data[i]['attraction']
                    percent = data[i]['incomelevel']
                    val_code = data[i]['valcode'].strip()
                    stock_code = data[i]['stockcode'].strip()
                    # Collect data in a tuple.
                    row_data = (auct_num, date_in, date_out,
                                money, percent, val_code, stock_code
                                )
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
    if os.path.exists(db_file):
        return create_connection(db_file)
    else:
        return create_connection(db_file, db_schema)


def insert_data(conn, data_file):
    """We connect to the database and record data."""
    check_data = "SELECT * FROM auctions WHERE auct_num = ? AND date_in = ?;"
    insert_data = "INSERT INTO auctions (auct_num, date_in, date_out, money, \
                                            percent, val_code, stock_code) \
                                         VALUES (?, ?, ?, ?, ?, ?, ?);"
    data = get_data(data_file)
    if data:
        for row in data:
            # Check in db -> (auct_num, date_in)
            id_exists = get_from_db(conn, check_data, (row[0], row[1]))
            if not id_exists:
                insert_row_data(conn, insert_data, row)
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
              'out': 'date_out'
              }
    if in_out_key in in_out.keys():
        return in_out.get(in_out_key)
    else:
        return False


def show_result(title, val_code, data):
    """show_report data."""
    show_report("{:6} {:<6} {}, {}".format(title, 'Count', 'Money', val_code))
    show_report("{:6} {:<6} {}".format('-' * 4, '-' * 5, '-' * 10))
    for row in data:
        period, count, money = row
        show_report("{:6} {:^6} {}".format(period, count, round(money, 2)))
    show_report()


def auctions_stats(conn, in_out):
    """We make a report on all auctions."""
    date_field_inout = get_date_inout(in_out)
    get_stats = "SELECT strftime('%Y', {}) as year, COUNT(), SUM(money) \
                                FROM auctions \
                                WHERE val_code = ? \
                                GROUP BY year \
                                ORDER BY year ASC;".format(date_field_inout)
    if date_field_inout:
        show_report("\n=== Money {} ===".format(in_out.upper()))
        show_report()
        for val_code in get_valcode(conn):
            data = []
            for row in get_from_db(conn, get_stats, (val_code, )):
                year = int(row[0])
                if year > 2011:
                    data.append(row)
            show_result('Year', val_code, data)
    else:
        show_report("Invalid parameter '{}' in function 'auctions_stats()'.".format(in_out))


def auctions_year(conn, year, in_out):
    """We draw up an auction report for the year."""
    date_field_inout = get_date_inout(in_out)
    get_months = "SELECT DISTINCT strftime('%m', date_in) as month \
                                                    FROM auctions \
                                                    ORDER BY month ASC;"
    get_stats = "SELECT strftime('%m', {0}) as month, COUNT(), SUM(money) \
                                FROM auctions \
                                WHERE val_code = ? AND {0} LIKE ? \
                                GROUP BY month \
                                ORDER BY month ASC;".format(date_field_inout)
    if date_field_inout:
        show_report("\n= Money {} / Year: {} =".format(in_out.upper(), year))
        show_report()
        for val_code in get_valcode(conn):
            data = []
            months = [x[0] for x in get_from_db(conn, get_months)]
            for month in months:
                # Format date '2019-08-__' for sql query LIKE
                date_search = '-'.join((str(year), month, '__'))
                answer = get_from_db(conn, get_stats, (val_code, date_search))
                if answer:
                    month, count, money = answer[0]
                    data.append((month, count, money))
                else:
                    data.append((month, 0, 0))
            show_result('Month', val_code, data)
    else:
        show_report("Invalid parameter '{}' in function 'auctions_year()'.".format(in_out))


def auctions_all(conn):
    """We get all the records."""
    get_all = "SELECT * FROM auctions ORDER BY date_in DESC;"
    for row in get_from_db(conn, get_all):
        show_report(row)



def auctions_report(conn, to_save=False):
    """We prepare reports."""
    if to_save is True:
        save_report[0] = True
        answer = show_report(mode_open='w')  # cleared report file
        if answer is not True:
            save_report[0] = False
            print(answer)
            return False

    # auctions_stats(conn, in_out='in')
    # auctions_stats(conn, in_out='out')
    # auctions_year(conn, 2018, in_out='in')
    # auctions_year(conn, 2018, in_out='out')
    auctions_all(conn)


if __name__ == '__main__':
    conn = get_connect(DB_FILE)
    if conn:
        if os.path.exists(DATA_FILE):
            insert_data(conn, DATA_FILE)
        auctions_report(conn)  # (conn, to_save=True)
        conn.close()
