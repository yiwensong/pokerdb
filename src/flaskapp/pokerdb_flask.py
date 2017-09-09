# from flask import Flask, render_template, request
import flask
from pydb import dbconn
import pandas as pd
import numpy as np
import re
import datetime

app = flask.Flask(__name__)

@app.route('/')
def index():
    data = dict()
    games = dbconn.query('SELECT * FROM sng_summary')
    data['cashed_percent'] = games.query('pl > 0').shape[0]\
            / games.shape[0] * 100
    data['total_buyin'] = games.buyin.sum() + games.rake.sum()
    data['total_cash'] = games.pl.sum() + data['total_buyin']
    data['rake'] = games.rake.sum()
    data['pl'] = games.pl.sum()
    data['ev'] = games.pl.mean()
    data['dev'] = games.pl.std()
    data['sharpe'] = data['ev']/data['dev']
    data['ROI'] = (data['pl']/data['total_buyin']) * 100
    today = datetime.date.today()
    yest = today - datetime.timedelta(1)
    data['today_pl'] = games.query('time_played > @today').pl.sum()
    data['yesterday_pl'] = games.query('time_played > @yest').pl.sum()\
            - data['today_pl']
    data = {k: "{:.2f}".format(v) for k,v in data.items()}
    data['games_played'] = games.shape[0]
    return flask.render_template('default_welcome_child.html', data=data)
    # return 'hey bb'

@app.route('/tournaments', methods=['GET', 'POST'])
def tournaments():
    if flask.request.method == 'GET':
        return flask.render_template('add_tournament.html')
    params = {k: flask.request.form[k] for k in flask.request.form}
    params['date_added'] = datetime.date.today()
    sng_types_params = ['date_added', 'name', 'buyin', 'rake', 'players']
    sng_prizes_params = ['sng_id', 'place', 'prize']
    dbconn.insert('sng_types', {k: params[k] for k in sng_types_params})
    # find sng_id
    sng_id = dbconn.query('''
        SELECT id
            FROM sng_types
            WHERE date_added = %(date_added)s
                AND name = %(name)s
                AND buyin = %(buyin)s
                AND rake = %(rake)s
                AND players = %(players)s
        ''', params=params).iloc[-1].id
    prizes = params['prizes'].split(',')
    for i, prize in enumerate(prizes):
        place = i + 1
        prize_dict = {'sng_id': int(sng_id), 'place': place, 'prize': float(prize)}
        print(prize_dict)
        dbconn.insert('sng_prizes', prize_dict)
    while i + 1 < int(params['players']):
        i += 1
        place = i + 1
        prize_dict = {'sng_id': int(sng_id), 'place': place, 'prize': 0.}
        dbconn.insert('sng_prizes', prize_dict)
    return flask.render_template('add_tournament.html', success=True)

@app.route('/add_result', methods=['GET', 'POST'])
def add_result():
    sng_types = dbconn.query('SELECT * FROM sng_types')
    sng_data = [v.to_dict() for i,v in sng_types.iterrows()]
    if flask.request.method == 'GET':
        return flask.render_template('add_result.html', tournaments=sng_data)
    params = {k: flask.request.form[k] for k in flask.request.form}
    params['time_played'] = datetime.datetime.now()
    params['place'] = int(params['place'])
    dbconn.insert('sng_results', params)
    return flask.render_template('add_result.html', tournaments=sng_data, success=True)
    

# @app.route('/yiwen')
# def yiwen():
#     return flask.render_template('default.html')

if __name__=='__main__':
    app.run(host='0.0.0.0')
