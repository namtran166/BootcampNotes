from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel
from utils import check_internal_server, check_not_found, validate_input


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='Name is required.'
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Price is required.'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Store is required.'
    )

    # No need for authentication since GET method is safe
    @staticmethod
    @check_internal_server
    @check_not_found
    def get(store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        return item.json(), 200

    @jwt_required()
    @check_internal_server
    @check_not_found
    def delete(self, store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        item.delete_from_db()
        return {'message': 'Item deleted.'}, 200

    @jwt_required()
    @check_internal_server
    @check_not_found
    def put(self, store_id, item_id):
        item = validate_input(store_id=store_id, item_id=item_id)
        data = Item.parser.parse_args()
        item.name = data['name']
        item.price = data['price']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @staticmethod
    @check_internal_server
    @check_not_found
    def get(store_id):
        store = validate_input(store_id=store_id)
        return store.json()['items'], 200

    @jwt_required()
    @check_internal_server
    @check_not_found
    def post(self, store_id):
        validate_input(store_id=store_id)
        data = Item.parser.parse_args()
        item = ItemModel(**data)
        item.save_to_db()
        return item.json(), 201
