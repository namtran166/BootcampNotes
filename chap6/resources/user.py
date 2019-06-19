from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Username cannot be blank.'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password cannot be blank.'
                        )

    @staticmethod
    def post():
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400
        try:
            user = UserModel(**data)
            user.save_to_db()
            return {'message': 'User created successfully.'}, 201
        except:
            return {'message': 'An error occurred when trying to create this user.'}, 500
