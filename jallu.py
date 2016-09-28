#!/usr/bin/env python3

from flask import Flask, render_template
from collections import OrderedDict
import requests
import json

app = Flask(__name__)


def getJalluLitrat():

    # 0 = *
    # 1 = ***
    jallut = [
        ('107088', 'Jaloviina * muovipullo', 1.0, 0),
        ('107067', 'Jaloviina *', 0.7, 0),
        ('107076', 'Jaloviina * muovipullo', 0.5, 0),
        ('000706', 'Jaloviina *', 0.5, 0),
        ('101121', 'Jaloviina *', 0.04, 0),
        ('106927', 'Jaloviina ***', 0.7, 1),
        ('000692', 'Jaloviina ***', 0.5, 1),
        ('106933', 'Jaloviina *** muovipullo', 0.2, 1),
    ]

    stores = OrderedDict()

    for jallu in jallut:
        r = requests.get(
            'http://www.alko.fi/api/product/Availability?productId={}&cityId=jyv%C3%A4skyl%C3%A4&language=fi'.format(jallu[0]))
        for store in json.loads(r.text):
            StoreName = store['StoreName']
            productLitres = float(store['Amount']) * jallu[2]
            productType = jallu[3]

            if (StoreName not in stores.keys()):
                stores[StoreName] = [productLitres, 0.0]
            else:
                stores[StoreName][productType] += productLitres

    jalluLitroja = [sum([stores[x][0] for x in stores.keys()]),
                    sum([stores[x][1] for x in stores.keys()])]  # MAGIC

    return (jalluLitroja, stores)


@app.route('/')
def jallua():
    jalluLitroja, stores = getJalluLitrat()
    return render_template('index.html',
                           # yks="{0:.2f}".format(jalluLitroja[0]),
                           # kolme="{0:.2f}".format(jalluLitroja[1]),
                           # sum="{0:.2f}".format(sum(jalluLitroja)),
                           yks=jalluLitroja[0],
                           kolme=jalluLitroja[1],
                           jallusum=sum(jalluLitroja),
                           stores=stores
                           )
