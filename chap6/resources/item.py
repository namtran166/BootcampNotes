from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This item needs a name.'
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This item needs a price.'
                        )

    # No need for authentication since GET method is safe
    @staticmethod
    def get(store_id, item_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404
            item = ItemModel.find_by_item_id(item_id)
            if item is None:
                return {'message': 'Item not found.'}, 404

            return item.json(), 200
        except:
            return {'message': 'An error occurred when trying to get this item.'}, 500

    @jwt_required()
    def post(self, store_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404

            data = Item.parser.parse_args()
            item = ItemModel(data['name'], data['price'], store_id)
            item.save_to_db()
            return item.json(), 201
        except:
            return {'message': 'An error occured while trying to post to this store.'}, 500

    @jwt_required()
    def delete(self, store_id, item_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404
            item = ItemModel.find_by_item_id(item_id)
            if item is None:
                return {'message': "Item not found.".format(item_id)}, 404

            item.delete_from_db()
            return {'message': 'Item deleted'}, 200
        except:
            return {'message': 'An error occurred when trying to delete this item.'}, 500

    @jwt_required()
    def put(self, store_id, item_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404

            item = ItemModel.find_by_item_id(item_id)
            if item is None:
                return {'message': "Item not found.".format(item_id)}, 404

            data = Item.parser.parse_args()
            item.update(**data)
            item.save_to_db()
            return item.json(), 200
        except:
            return {'message': 'An error occured while trying to put this book ID'}, 500


class ItemList(Resource):
    @staticmethod
    def get(store_id):
        store = StoreModel.find_by_store_id(store_id)
        if store is None:
            return {'message': 'Store not found.'}, 404

        return store.json()['items'], 200
