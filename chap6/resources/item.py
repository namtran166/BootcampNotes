from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel
from utils import check_internal_server, validate_input


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='This item needs a name.'
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This item needs a price.'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='This item needs a store.'
    )

    # No need for authentication since GET method is safe
    @staticmethod
    @check_internal_server
    def get(store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        if item[1] == 404:
            return item

        return item.json(), 200

    @jwt_required()
    @check_internal_server
    def delete(self, store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        if item[1] == 404:
            return item

        item.delete_from_db()
        return {'message': 'Item deleted.'}, 200

    @jwt_required()
    @check_internal_server
    def put(self, store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        if item[1] == 404:
            return item

        data = Item.parser.parse_args()
        item.update(**data)
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @staticmethod
    @check_internal_server
    def get(store_id):
        store = validate_input(store_id=store_id)
        if store[1] == 404:
            return store

        return store.json()['items'], 200

    @jwt_required()
    @check_internal_server
    def post(self, store_id):
        store = validate_input(store_id=store_id)
        if store[1] == 404:
            return store

        data = Item.parser.parse_args()
        item = ItemModel(**data)
        item.save_to_db()
        return item.json(), 201
