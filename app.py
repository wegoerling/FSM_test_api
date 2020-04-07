import os

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True
    CSRF_ENABLED = True

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'curd.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Kit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    brand = db.Column(db.String(120), unique=True)
    def __init__(self, name, brand):
        self.name = name
        self.brand = brand

class KitSchema(ma.Schema):
    class Meta:
        fields = ('brand', 'name')

kit_schema = KitSchema()
kits_schema = KitSchema(many=True)


@app.route('/')
def hello_world():
    return 'Hello, Fraunhofer!'


@app.route("/kit", methods=["POST"])
def add_kit():
    name = request.json['name']
    brand = request.json['brand']
    new_kit = Kit(name, brand)
    db.session.add(new_kit)
    db.session.commit()
    return jsonify(kit_schema.dump(new_kit))


@app.route("/kit", methods=["GET"])
def get_kit():
    all_kits = Kit.query.all()
    result = kits_schema.dump(all_kits)
    return jsonify(result)


@app.route("/kit/<id>", methods = ["GET"])
def kit_detail(id):
    kit = Kit.query.get(id)
    return kit_schema.jsonify(kit)


@app.route("/kit/<id>", methods = ["PUT"])
def kit_update(id):
    kit = Kit.query.get(id)
    name = request.json['name']
    brand = request.json['brand']
    kit.brand = brand
    kit.name = name
    db.session.commit()
    return kit_schema.jsonify(kit)


@app.route("/kit/<id>", methods = ["DELETE"])
def kit_delete(id):
    kit = Kit.query.get(id)
    db.session.delete(kit)
    db.session.commit()
    return kit_schema.jsonify(kit)


if __name__ == "__main__":
    app.run(debug=True)
