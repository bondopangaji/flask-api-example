from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Init App
app = Flask(__name__)
if __name__ == '__main__':
    app.run()


# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


# Data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


db.create_all()


# Routes
@app.route('/user', methods=['GET'])
def get_users():
    items = []
    for item in db.session.query(User).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    db.session.add(User(body['first_name'], body['last_name'], body['email']))
    db.session.commit()
    return "user created"


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    del user.__dict__['_sa_instance_state']
    return jsonify(user.__dict__)


@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    db.session.query(User).filter_by(id=id).update(
        dict(first_name=body['first_name'], last_name=body['last_name'], email=body['email']))
    db.session.commit()
    return "user updated"


@app.route('/user/<id>', methods=['DELETE'])
def delete_item(id):
    db.session.query(User).filter_by(id=id).delete()
    db.session.commit()
    return "user deleted"
