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
    def get(self, store_id):
        try:
            store = StoreModel.find_by_store_id(store_id)
            if store:
                return store.json(), 200
            return {'message': 'Store not found.'}, 404
        except:
            return {'message': 'An error occurred when trying to get this store.'}, 500

    @jwt_required()
    def post(self, store_id):
        if StoreModel.find_by_store_id(store_id):
            return {'message': 'A store with store_id {} already exists.'.format(store_id)}, 400

        data = Store.parser.parse_args()
        try:
            store = StoreModel(store_id, data['name'])
            store.save_to_db()
        except:
            return {'message': 'An error occurred when trying to post this store.'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.find_by_store_id(store_id)
        if store is None:
            return {'message': "There is no store with store_id {}.".format(store_id)}, 404
        else:
            if len(store.items.all()) == 0:
                try:
                    store.delete_from_db()
                    return {'message': 'Store deleted.'}, 200
                except:
                    return {'message': 'An error occurred when trying to delete this store.'}, 500
            else:
                return {'message': 'This store still contains some items.'}, 400

    @jwt_required()
    def put(self, store_id):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_store_id(store_id)
        try:
            if store is None:
                return {'message': 'Store not found.'}, 404
            else:
                store.name = data['name']
                return store.json(), 200
        except:
            return {'message': 'An error occurred when trying to put this store.'}, 500


class StoreList(Resource):
    @staticmethod
    def get():
        return [store.json() for store in StoreModel.query.all()]
