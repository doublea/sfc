#!/usr/bin/env python
from collections import defaultdict
from operator import itemgetter

from flask import Flask, render_template, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from users.users import create_users_blueprint, login_required
from models import *
from forms import *

app = Flask(__name__)
app.config.from_object('default_settings')

db = SQLAlchemy(app)
users = create_users_blueprint(app, db, 'map_home')
app.register_blueprint(users)

@app.route('/')
@app.route('/map/')
@app.route('/map/<int:x>/<int:y>/<int:w>/<int:h>')
@login_required
def map_home(x=0, y=0, w=20, h=20):
    objs = MapObject.query.filter(MapObject.x >= x, MapObject.x < x+w,
                                  MapObject.y >= y, MapObject.y < y+h).all()

    obj_dict = defaultdict(lambda: [])
    for obj in objs:
        obj_dict["%s, %s" % (obj.x, obj.y)].append(obj.to_dict())
    return render_template('map.html', x=x, y=y, w=w, h=h, objects=obj_dict)

@app.route('/canvasmap/')
@app.route('/canvasmap/<int:x>/<int:y>/<int:w>/<int:h>')
def canvasmap(x=0, y=0, w=20, h=20):
    objs = MapObject.query.filter(MapObject.x >= x, MapObject.x < x+w,
                                  MapObject.y >= y, MapObject.y < y+h).all()

    obj_dict = defaultdict(lambda: [])
    for obj in objs:
        obj_dict["%s, %s" % (obj.x, obj.y)].append(obj.to_dict())
    return render_template('canvasmap.html', x=x, y=y, w=w, h=h, objects=obj_dict)

@app.route('/shiplist/')
@app.route('/shiplist/<race>/')
@app.route('/shiplist/<race>/<type>/')
@app.route('/shiplist/<race>/<type>/<model>/')
@login_required
def shiplist(race=None, type=None, model=None):
    if model is None:
        if type is None:
            if race is None:
                races = map(itemgetter(0), db.session.query(func.distinct(ShipModel.race)).all())
                return render_template('shiplist/main.html', races=races)
            types = map(itemgetter(0),
                        db.session.query(
                            func.distinct(ShipModel.hull_type))
                            .filter(ShipModel.race == race).all())
            return render_template('shiplist/types_list.html', race=race, types=types)
        models = ShipModel.query.filter(ShipModel.race == race, ShipModel.hull_type == type).values(ShipModel.ship_class)
        return render_template('shiplist/models_list.html', race=race, type=type, models=map(itemgetter(0), models))
    return render_template('shiplist/ship.html', ship=ShipModel.query.filter(ShipModel.ship_class == model).one())

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
