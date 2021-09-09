from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="this can not be blank"
    )
    parser = reqparse.RequestParser()
    parser.add_argument('password',
    type=str,
    required=True,
    help="this can not be blank"
    )

    def post(self):
        date = UserRegister.parser.parse_args()

        if UserModel.find_by_username(date['username']):
            return {"message": "A user with this username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user created successfully"}, 201
