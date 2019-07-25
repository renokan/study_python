"""OVDP Flask."""

from flask import Flask
from flask import render_template, abort
import json

app = Flask(__name__)

current_year = 2019
years = [x for x in range(2012, current_year)]


def show_auctions(quantity=None):
    try:
        import os
        path_to_db = os.path.dirname(os.path.realpath(__file__)) + os.sep
        data = json.load(open(path_to_db + 'db_auctions.json', encoding='utf-8'))
    except Exception:
        pass
    else:
        temp = {}
        if data[0].get('auctiondate'):
            for i in range(len(data)):
                auct_year = int(data[i]['auctiondate'].split(".")[2])
                auct_num = data[i]['auctionnum']
                temp[(auct_year, auct_num)] = data[i]
        result = []
        i = 0
        for key, value in sorted(temp.items(), reverse=True):
            if i == quantity:
                break
            result.append(value)
            i += 1
        return result


@app.route('/')
def index():
    return render_template("index.html", auctions=show_auctions(5))


@app.route('/auctions')
def auctions():
    return render_template("auctions.html", auctions=show_auctions(12))


@app.route('/stats')
def stats():
    return render_template("stats.html", show_year=current_year, list_year=years)


@app.route('/year')
def year():
    return render_template("year.html", show_year=current_year, list_year=years)


@app.route('/year/<int:num_year>')
def show_year(num_year):
    if num_year in years:
        return render_template("year.html", show_year=num_year, list_year=years)
    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.context_processor
def inject_year():
    return dict(menu_year=current_year)


if __name__ == '__main__':
    app.debug = True
    app.run()
