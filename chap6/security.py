from werkzeug.security import check_password_hash

from models.user import UserModel
from utils import check_internal_server


@check_internal_server
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and check_password_hash(user.hashed_password, password):
        return user


@check_internal_server
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
