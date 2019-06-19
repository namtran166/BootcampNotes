from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


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
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This item needs a store to sell.'
                        )

    # No need for authentication since GET method is safe
    @staticmethod
    def get(item_id):
        try:
            item = ItemModel.find_by_item_id(item_id)
            if item:
                return item.json(), 200
            return {'message': 'Item not found.'}, 404
        except:
            return {'message': 'An error occurred when trying to get this item.'}, 500

    @jwt_required()
    def post(self, item_id):
        if ItemModel.find_by_item_id(item_id):
            return {'message': "An item with item_id '{}' already exists.".format(item_id)}, 400

        data = Item.parser.parse_args()
        try:
            item = ItemModel(item_id, **data)
            item.save_to_db()
        except:
            return {'message': 'An error occured while trying to post this item.'}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.find_by_item_id(item_id)
        if item is None:
            return {'message': "There is no item with item_id '{}'.".format(item_id)}, 404
        else:
            try:
                item.delete_from_db()
                return {'message': 'Item deleted'}, 200
            except:
                return {'message': 'An error occurred when trying to delete this item.'}, 500

    @jwt_required()
    def put(self, item_id):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_item_id(item_id)

        try:
            if item is None:
                return {'message': 'Item not found.'}, 404
            else:
                item.name = data['name']
                item.price = data['price']
                item.store_id = data['store_id']
                item.save_to_db()
                return item.json(), 200
        except:
            return {'message': 'An error occured while trying to put this item ID'}, 500


class ItemList(Resource):
    @staticmethod
    def get():
        return [item.json() for item in ItemModel.query.all()], 200
