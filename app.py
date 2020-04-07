import os

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from config import Config, Configdb

# Define Flask app and base directory
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# establish configuration and primary objects
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'curd.sqlite')
app.config.from_object(Config)
app.config.from_object(Configdb)
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
@app.route('/')
def hello_world():
    return 'Hello, Fraunhofer!'

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
