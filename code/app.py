#imports
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
#imports from packages within the project folder

#Flask Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kulu'
api = Api(app)

jwt = JWT(app, authenticate, identity) #auth endpoint
#create db with sqlalchemy

#endpoints

#run app with if name main
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)