import functools

from models.item import ItemModel
from models.store import StoreModel


def check_internal_server(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            return {'message': 'An unexpected Internal Server Error occurred.'}, 500
        return func(*args, **kwargs)

    return check_error


def validate_input(**kwargs):
    store = StoreModel.find_by_store_id(kwargs['store_id'])
    if store is None:
        return {'message': 'Store not found.'}, 404
    if kwargs['item_id'] is None:
        return store
    item = ItemModel.find_by_item_id(kwargs['item_id'])
    if item is None:
        return {'message': "Item not found."}, 404
    return item
