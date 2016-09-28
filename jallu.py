#!/usr/bin/env python3

from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

def getJalluLitrat():

    jallut = [
        ('107088', 'Jaloviina * muovipullo', 1.0, 1),
        ('107067', 'Jaloviina *', 0.7, 1),
        ('107076', 'Jaloviina * muovipullo', 0.5, 1),
        ('000706', 'Jaloviina *', 0.5, 1),
        ('101121', 'Jaloviina *', 0.04, 1),
        ('106927', 'Jaloviina ***', 0.7, 3),
        ('000692', 'Jaloviina ***', 0.5, 3),
        ('106933', 'Jaloviina *** muovipullo', 0.2, 3),
    ]

    jalluLitroja = [0.0, 0.0] # [yhden, kolmen]

    for jallu in jallut:
        r = requests.get('http://www.alko.fi/api/product/Availability?productId={}&cityId=jyv%C3%A4skyl%C3%A4&language=fi'.format(jallu[0]))
        for store in json.loads(r.text):
            if jallu[3] == 1:
                jalluLitroja[0] += (float(store['Amount']) * jallu[2])
            elif jallu[3] == 3:
                jalluLitroja[1] += (float(store['Amount']) * jallu[2])

    return jalluLitroja

@app.route('/')
def jallua():
    jalluLitroja = getJalluLitrat()
    return render_template('index.html',
        yks   = "{0:.2f}".format(jalluLitroja[0]),
        kolme = "{0:.2f}".format(jalluLitroja[1]),
        sum   = "{0:.2f}".format(sum(jalluLitroja))
    )
