from os import abort
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)


class TaskModel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"(Task(id = {self.id}, title = {self.title}, description = {self.description})"


# db.create_all()


task_post_args = reqparse.RequestParser()
task_post_args.add_argument(
    "title", type=str, help="Title of task", required=True)
task_post_args.add_argument("description", type=str,
                            help="Description of task", required=True)


task_put_args = reqparse.RequestParser()
task_put_args.add_argument(
    'title', type=str, help="Change title of task")

task_put_args.add_argument(
    'description', type=str, help="Change description of task")


resource_fields = {
    "id": fields.Integer,
    'title': fields.String,
    "description": fields.String
}


class AllTasks(Resource):
    @marshal_with(resource_fields)
    def get(self):
        tasks = TaskModel.query.all()

        return tasks


class Task(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message='Cannot find task with this id..')
        return result

    @marshal_with(resource_fields)
    def post(self, task_id):
        args = task_post_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()
        if result:
            abort(409, message='Task id taken..')

        task = TaskModel(
            id=task_id, title=args['title'], description=args['description'])
        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_put_args.parse_args()
        result = TaskModel.query.filter_by(id=task_id).first()

        if not result:
            abort(404, message='Task doesnt exist, cannot update.')

        if args['title']:
            result.title = args['title']
        if args['description']:
            result.description = args['description']

        db.session.commit()
        return result

    def delete(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()

        if not result:
            abort(404, message='Task doesnt exist, cannot delete.')

        db.session.delete(result)
        db.session.commit()

        return {"message": "Task deleted successfully"}, 204


api.add_resource(Task, '/tasks/<int:task_id>')
api.add_resource(AllTasks, '/tasks')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050)
