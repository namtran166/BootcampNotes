from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash

from models.user import UserModel
from utils import check_internal_server


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username cannot be blank.'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password cannot be blank.'
    )

    @staticmethod
    @check_internal_server
    def post():
        data = UserRegister.parser.parse_args()
        username = data['username'].strip()
        if UserModel.find_by_username(username):
            return {'message': 'An user with that username already exists.'}, 400
        hashed_password = generate_password_hash(data['password'])
        print(data)
        del data['username']
        del data['password']
        user = UserModel(username=username, hashed_password=hashed_password, **data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201
