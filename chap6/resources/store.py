from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.store import StoreModel
from utils import check_internal_server, validate_input


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This store needs a name.'
    )

    @staticmethod
    @check_internal_server
    def get(store_id):
        store = validate_input(store_id=store_id)
        if store[1] == 404:
            return store

        return store.json(), 200

    @jwt_required()
    @check_internal_server
    def delete(self, store_id):
        store = validate_input(store_id=store_id)
        if store[1] == 404:
            return store
        if store.items.first() is not None:
            return {'message': 'This store still contains some items.'}, 400

        store.delete_from_db()
        return {'message': 'Store deleted.'}, 200

    @jwt_required()
    @check_internal_server
    def put(self, store_id):
        store = validate_input(store_id=store_id)
        if store[1] == 404:
            return store

        data = Store.parser.parse_args()
        store.name = data['name']
        return store.json(), 200


class StoreList(Resource):
    @staticmethod
    @check_internal_server
    def get():
        return [store.json() for store in StoreModel.query.all()]

    @jwt_required()
    @check_internal_server
    def post(self):
        data = Store.parser.parse_args()
        store = StoreModel(**data)
        store.save_to_db()
        return store.json(), 201
