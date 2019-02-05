#!/usr/bin/env python3
# this uses a shebang to easily start script with ./app.py

import datetime
import json

from flask import (Flask, render_template, redirect,
                   url_for, request, make_response)

from options import DEFAULTS


app = Flask(__name__)


def get_saved_data():
    """Return data from cookie if found, else empty dict"""
    try:
        # loads stands for 'load string'
        data = json.loads(request.cookies.get('character'))
    except TypeError:
        data = {}
    return data


@app.route('/')
def index():
    """Show homepage with data from cookies"""
    return render_template('index.html', saves=get_saved_data())


@app.route('/builder')
def builder():
    return render_template(
        'builder.html',
        saves=get_saved_data(),
        options=DEFAULTS,
    )


@app.route('/save', methods=['POST'])
def save():
    """
    Save input of submitted form to cookie and return index.html
    """
    data = get_saved_data()
    # items from html-form with POST method are in request.form.items()
    data.update(dict(request.form.items()))

    print(data)

    # to set a cookie with Flask you first need to make the response
    response = make_response(redirect(url_for('builder')))

    cookie_expire_date = datetime.datetime.now() + datetime.timedelta(days=90)

    # we created the response above, now we can set the cookie
    response.set_cookie(
        'character',
        json.dumps(data),  # dumps stands for 'dump string'
        expires=cookie_expire_date,
    )

    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
