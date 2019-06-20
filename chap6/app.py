#!/usr/local/bin/python3
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'brian'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/stores/<int:store_id>', '/stores')
api.add_resource(StoreList, '/store_list')
api.add_resource(Item, '/stores/<int:store_id>/items/<int:item_id>', '/stores/<int:store_id>/items')
api.add_resource(ItemList, '/stores/<int:store_id>/item_list')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)
