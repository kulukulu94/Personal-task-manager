from flask import render_template, make_response
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.task import  TaskModel


class Create_Task(Resource):
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

    def post(self):
        user_data = Create_Task.parser.parse_args()
        task = TaskModel(**user_data)
        try:
            task.save_to_db()
        except:
            return {"message": "error inserting task data"}

        return task.json(), 201


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


    @jwt_required()
    def get(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            return task.json()
        return {'message': 'Task not found'}, 404

    def delete(self, id):
        task = TaskModel.find_by_id(id)
        if task:
            task.delete_from_db()
            return {"message": "task deleted"}
        return{'message': 'task not found'}, 404

    def put(self, id):
        data = Task.parser.parse_args()
        #print(data)
        task = TaskModel.find_by_id(id)
        print(task)
        if task is None:
            task = TaskModel(**data)
        else:
            task.name = data['name']
            task.description = data['description']
        
        task.save_to_db()
        return task.json()

class TaskList(Resource):
    def get(self):
        tlist = [x.json() for x in TaskModel.find_all()]
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('form.jinja2', tasklist=tlist),200, headers)
        
        #return {'task': [x.json() for x in TaskModel.query.all()]}
        
        #return  render_template('form.html', tasklist=tlist)
        #return Response(render_template('test.html', result=test, mimetype='text/html'))