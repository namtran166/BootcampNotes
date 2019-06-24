from flask_restful import Resource, reqparse

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
        if UserModel.find_by_username(data['username']):
            return {'message': 'An user with that username already exists.'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201
