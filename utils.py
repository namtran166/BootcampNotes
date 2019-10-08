import functools

from models.item import ItemModel
from models.store import StoreModel


def check_internal_server(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return {'message': 'An unexpected Internal Server Error occurred.'}, 500

    return check_error


def check_not_found(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return {'message': str(e)}, 404

    return check_error


def validate_input(**kwargs):
    store = StoreModel.find_by_id(kwargs['store_id'])
    if store is None:
        raise ValueError('Store not found.')
    if 'item_id' not in kwargs:
        return store
    item = ItemModel.find_by_id(kwargs['item_id'])
    if item is None:
        raise ValueError('Item not found.')
    return item
