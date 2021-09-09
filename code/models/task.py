from db import db
import datetime

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(500))
    #created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created = db.Column(db.String(80))
    #json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)

    user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')

    def __init__(self, name, description, created, user_id):
        self.name = name
        self.description = description
        self.created = created
        self.user_id = user_id

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'created': self.created, 'user_id': self.user_id}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
