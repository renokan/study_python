"""OVDP Flask."""

from flask import Flask
from flask import render_template, request, abort
import json

app = Flask(__name__)

current_year = 2019
years = [x for x in range(2012, current_year)]


def show_auctions(year=None):
    try:
        import os
        path_to_db = os.path.dirname(os.path.realpath(__file__)) + os.sep
        data = json.load(open(path_to_db + 'db_auctions.json', encoding='utf-8'))
    except Exception:
        return None
    else:
        temp = {}
        if data[0].get('auctiondate'):
            for i in range(len(data)):
                auct_year = int(data[i]['auctiondate'].split(".")[2])
                auct_num = data[i]['auctionnum']
                if auct_year > 2011 and data[i]['attraction'] > 0:
                    if year:
                        if year == auct_year:
                            temp[(auct_year, auct_num)] = data[i]
                    else:
                        temp[(auct_year, auct_num)] = data[i]

        return [value for key, value in sorted(temp.items(), reverse=True)]


@app.route('/')
def index():
    auctions = show_auctions()
    if auctions:
        return render_template("index.html", auctions=auctions[:2])
    else:
        return render_template("index.html")


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


@app.route('/auctions')
def auctions():
    show_list = 16
    next = 0
    previous = 0

    year = request.args.get('year')
    if year:
        try:
            year = int(year)
        except Exception:
            abort(404)
        else:
            if year in years:
                auctions = show_auctions(year)
            else:
                abort(404)
    else:
        year = None
        auctions = show_auctions()

    if auctions:
        pages = len(auctions) // show_list
        if (len(auctions) % show_list) != 0:
            pages += 1

        page = request.args.get('page')
        if page:
            try:
                page = int(page)
            except Exception:
                abort(404)
            else:
                if page > pages or page < 0:
                    abort(404)
                if page < pages:
                    next = page + 1
                    show = auctions[(page - 1) * show_list:page * show_list]
                else:
                    show = auctions[(page - 1) * show_list:]
                if page > 1:
                    previous = page - 1
        else:
            page = 1
            next = 2
            show = auctions[:show_list]

        return render_template("auctions.html", auctions=show,
                               previous=previous, page=page, pages=pages, next=next,
                               year=year, list_year=years
                               )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.context_processor
def inject_year():
    return dict(menu_year=current_year)


@app.template_filter()
def money_format(value):
    return format(round(value), ',d')


if __name__ == '__main__':
    app.debug = True
    app.run()
