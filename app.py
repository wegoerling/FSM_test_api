import os
# import sys.path
# from sys.path import permissions

from flask import Flask, session, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt import JWT, current_identity, jwt_required
from werkzeug.security import safe_str_cmp
from config import Config, Configdb
from permissions import UserPermission, AdminPermission


# user generation
from rules import AdminOnly


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        # self.rank = 'admin'

    def __str__(self):
        return "User(id='%s')" % self.id


users = [
    User(1, 'walter', 'abcxyz'),
    User(2, 'gudjon', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

# Define Flask app, base directory, and security
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "walter"  # Make this long, random, and secret in a real app!
jwt = JWT(app, authenticate, identity)

# establish configuration and primary objects
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'curd.sqlite')
app.config.from_object(Config)
app.config.from_object(Configdb)
app.debug = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

# SQLalchemy: Defines a class on an SQL table
class Kit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    brand = db.Column(db.String(120), unique=False)
    def __init__(self, name, brand):
        self.name = name
        self.brand = brand

# Marshmallow: Defines a schema to translate SQL entries to JSON
class KitSchema(ma.Schema):
    class Meta:
        fields = ('brand', 'name')

kit_schema = KitSchema()
kits_schema = KitSchema(many=True)

# Main page
@app.route('/home')
def index():
    return "Hello, log in for more content!"

@app.route('/protected')
@jwt_required()
def protected():
    session.user_id = current_identity
    return '%s' % current_identity

@app.route('/settings2')
@UserPermission()
def settings():
    """User settings page, only accessible for sign-in user."""
    return jsonify('settings.html')

@app.route('/settingsmaster')
@AdminPermission()
def settingsmaster():
    """User settings page, only accessible for sign-in user."""
    return jsonify('settingsmaster.html')

# Add an entry to the table using HTTP POST
@app.route("/kit", methods=["POST"])
def add_kit():
    name = request.json['name']
    brand = request.json['brand']
    if name and brand:
        old_kit = Kit.query.filter_by(name=name).first()
        if old_kit is not None:
            response = {
                'message': 'a kit with that name already exists'
            }
            return jsonify(response), 403
        new_kit = Kit(name, brand)
        db.session.add(new_kit)
        db.session.commit()
        return jsonify(kit_schema.dump(new_kit)), 202
    response = {
        'message': 'error in request body'
    }
    return jsonify(response), 400

# See all entries using HTTP GET
@app.route("/kit", methods=["GET"])
def get_kit():
    all_kits = Kit.query.all()
    result = kits_schema.dump(all_kits)
    if not result:
        response = {
            'message': 'there are no kits',
            'result': result
        }
        return jsonify(response), 201
    return jsonify(result), 202

# See one entry using HTTP GET
@app.route("/kit/<id>", methods = ["GET"])
def kit_detail(id):
    kit = Kit.query.filter_by(id=id).first()
    if kit is None:
        response = {
                 'message': 'kit does not exist'
                   }
        return jsonify(response), 404
    # kit = Kit.query.get(id)
    return kit_schema.jsonify(kit), 202

# Update one entry using HTTP PUT
@app.route("/kit/<id>", methods = ["PUT"])
def kit_update(id):
    kit = Kit.query.filter_by(id=id).first()
    if kit is None:
        response = {
                 'message': 'kit does not exist'
                   }
        return jsonify(response), 404
    # kit = Kit.query.get(id)
    name = request.json['name']
    brand = request.json['brand']
    kit.brand = brand
    kit.name = name
    db.session.commit()
    return kit_schema.jsonify(kit), 202

# Remove one entry using HTTP DELETE
@app.route("/kit/<id>", methods = ["DELETE"])
def kit_delete(id):
    kit = Kit.query.filter_by(id=id).first()
    if kit is None:
        response = {
                 'message': 'kit does not exist'
                   }
        return jsonify(response), 404
    # kit = Kit.query.get(id)
    db.session.delete(kit)
    db.session.commit()
    return kit_schema.jsonify(kit), 202


if __name__ == "__main__":
    app.run(debug=True)
