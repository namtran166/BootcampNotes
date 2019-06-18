from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(616, 'nam', '1234'),
    User(707, 'brian', '5678'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    userID = payload['identity']
    return userid_table.get(userID, None)
