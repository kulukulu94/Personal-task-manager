#imports
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

#imports from packages within the project folder
from resources.task import  Create_Task, Task, TaskList
from resources.user import UserRegister, User, UserLogin


#Flask Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kulu'
api = Api(app)

#auth endpoint
jwt = JWTManager(app) 

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #instead of hard coding u should read from a file or database
        return {'is_admin': True}
    return {'is_admin': False}

#create db with sqlalchemy
# @app.before_first_request
# def create_tables():
#     db.create_all()

#resources endpoints
api.add_resource(Task, '/task/<int:id>')
api.add_resource(Create_Task, '/task')
api.add_resource(TaskList, '/tasks')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')


#run app with if name main
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)