#!/usr/bin/env python
from collections import defaultdict

from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from users.users import create_users_blueprint, login_required
from models import *
from forms import *

app = Flask(__name__)
app.config.from_object('default_settings')

db = SQLAlchemy(app)
users = create_users_blueprint(app, db, 'map_home')
app.register_blueprint(users)

@login_required
@app.route('/')
@app.route('/map/<x>/<y>/<w>/<h>')
def map(x=0, y=0, w=20, h=20):
    objs = MapObject.query.filter(MapObject.x >= x, MapObject.x < x+w,
                                  MapObject.y >= y, MapObject.y < y+h).all()

    obj_dict = defaultdict(lambda: [])
    for obj in objs:
        obj_dict[(obj.x, obj.y)].append(obj)
    return render_template('map.html', x=x, y=y, w=w, h=h, objects=obj_dict)

if __name__ == '__main__':
    app.run(debug=True)
