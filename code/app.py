#imports
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

#imports from packages within the project folder
from security import authenticate, identity
from resources.task import Task, TaskList
from resources.user import UserRegister


#Flask Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kulu'
api = Api(app)
#auth endpoint
jwt = JWT(app, authenticate, identity) 
#create db with sqlalchemy

#resources endpoints
api.add_resource(Task, '/task/<integer:id')
api.add_resource(TaskList, '/tasks')
api.add_resource(UserRegister, '/register')


#run app with if name main
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)