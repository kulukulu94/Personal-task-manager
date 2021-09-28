from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from blacklist  import  BLACKLIST

_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username',
        type=str,
        required=True,
        help="this can not be blank"
        )

_user_parser.add_argument('password',
        type=str,
        required=True,
        help="this can not be blank"
        )

class UserRegister(Resource):
 

    def post(self):
        data = _user_parser.parse_args()
        print(data['password'])
        #user = UserModel.find_by_username(data['username'])
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user created successfully"}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found.'}, 404
        return user.json()
   
    
    @classmethod
    @jwt_required()
    def delete(cls, user_id):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'msg': 'You need Admin privilege!.'}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found.'}
        user.delete_from_db()
        return {'nessage': 'user deleted'}, 200

class UserLogin(Resource):


    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_access_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': ' Invalid Credentials!'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        #print(BLACKLIST)
        return  {'message': 'User logged out successfully.'}, 200
