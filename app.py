#imports
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

#imports from packages within the project folder
from resources.task import  Create_Task, Task, TaskList
from resources.user import UserRegister, User, UserLogin, UserLogout
from blacklist      import BLACKLIST


#Flask Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
#app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'kulu'
api = Api(app)

#auth endpoint
jwt = JWTManager(app) 

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #instead of hard coding u should read from a file or database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLACKLIST #jaw_payload['sub'] the id should be fetched from a db

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'request has not authorization token',
        'error': 'authorization_required'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verfication failed',
        'error': 'invalid_token'
    }), 401

@jwt.revoked_token_loader
def revocked_token_callback(jwt_header, jwt_payload):
    return jsonify(
        msg=f"Token has been revocked, I'm sorry {jwt_payload['sub']} I can't let you do that"
    ), 401


#resources endpoints
api.add_resource(Task, '/task/<int:id>')
api.add_resource(Create_Task, '/task')
api.add_resource(TaskList, '/tasks')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


#run app with if name main
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)