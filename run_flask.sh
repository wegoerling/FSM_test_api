#!/bin/sh

# python3
# >> from app import db
# >> db.create_all()

set FLASK_APP="app.py"
aet FLASK_ENV=development
flask run