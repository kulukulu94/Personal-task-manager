from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.task import  TaskModel


class Task(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
        type= str,
        required=True,
        help="every task must have a name"
        )
    parser.add_argument('description',
        type= str,
        required=True,
        help="every task must have description"
        )
    parser.add_argument('created',
        type= str,
        required=True,
        help="every task must have description"
        )
    parser.add_argument('user_id',
        type= int,
        required=True,
        help="every task is related to a user"
        )


    @jwt_required
    def get(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            return task.json()
        return {'message': 'Task not found'}, 404

    def post(self):
        user_data = Task.parser.parse_args()
        print(user_data)
        task = TaskModel(**user_data)
        print(task)
        try:
            task.save_to_db()
        except:
            return {"message": "error inserting task data"}

        return task.json(), 201

    def delete(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            task.delete_from_db()
            return {"message": "task deleted"}
        return{'message': 'task not found'}, 404

    def put(self, id, name, description):
        user_data = Task.parser.parse_args()
        task = Taskmodel.find_by_id(id)
        if task in None:
            task = TaskModel(name, description, user_data)
        else:
            task.name = name
            task.description = description
            task.user_id = user_data
        
        task.save_to_db()
        return task.json()


class TaskList(Resource):
    def get(self):
        return {'task': [x.json() for x in TaskModel.query.all()]}