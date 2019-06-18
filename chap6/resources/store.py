from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type = str,
        required = True,
        help = "What store is this?"
    )

    # No need for authentication since GET method is safe
    def get(self, storeID):
        try:
            store = StoreModel.find_by_storeID(storeID)
            if store:
                return store.json(), 200
            return {'message': 'Store not found'}, 404
        except:
            return {'message': 'An error occurred when trying to get this store.'}, 500

    @jwt_required()
    def post(self, storeID):
        if StoreModel.find_by_storeID(storeID):
            return {'message': 'A store with store ID {} already exists.'.format(storeID)}, 400

        data = Store.parser.parse_args()
        try:
            store = StoreModel(storeID, data['name'])
            store.save_to_db()
        except:
            return {'message': 'An error occurred when trying to post this store.'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, storeID):
        store = StoreModel.find_by_storeID(storeID)
        if store is None:
            return {'message': "There is no store with storeID {}.".format(storeID)}, 400
        else:
            if len(store.books.all()) == 0:
                try:
                    store.delete_from_db()
                    return {'message': 'Store deleted'}, 200
                except:
                    return {'message': 'An error occurred when trying to delete this store.'}, 500
            else:
                return {'message': 'This store still contains some books'}, 400

    @jwt_required()
    def put(self, storeID):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_storeID(storeID)
        try:
            if store is None:
                store = StoreModel(storeID, data['name'])
            else:
                store.name = data['name']
            store.save_to_db()
        except:
            return {'message': 'An error occurred when trying to put this store.'}, 500
        return store.json(), 200

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
