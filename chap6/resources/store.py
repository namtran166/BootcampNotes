from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This store needs a name.'
                        )

    # No need for authentication since GET method is safe
    @staticmethod
    def get(store_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404
            return store.json(), 200
        except:
            return {'message': 'An error occurred when trying to get this store.'}, 500

    @jwt_required()
    def post(self):
        try:
            data = Store.parser.parse_args()
            store = StoreModel(data['name'])
            store.save_to_db()
            return store.json(), 201
        except:
            return {'message': 'An error occurred when trying to post this store.'}, 500

    @jwt_required()
    def delete(self, store_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404
            else:
                if len(store.items.all()) == 0:
                    store.delete_from_db()
                    return {'message': 'Store deleted.'}, 200
                else:
                    return {'message': 'This store still contains some items.'}, 400
        except:
            return {'message': 'An error occurred when trying to delete this store.'}, 500

    @jwt_required()
    def put(self, store_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store is None:
                return {'message': 'Store not found.'}, 404
            else:
                data = Store.parser.parse_args()
                store.name = data['name']
                return store.json(), 200
        except:
            return {'message': 'An error occurred when trying to put this store.'}, 500


class StoreList(Resource):
    @staticmethod
    def get():
        return [store.json() for store in StoreModel.query.all()]
