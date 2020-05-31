import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="Username must be present"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password is not valid"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that name already exists"}, 400

        user = UserModel(data['username'], data['password'])

        user.save_to_db()

        return {"message": "User created successfully"}, 201