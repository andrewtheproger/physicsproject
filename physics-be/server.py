from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from flask_jsonschema_validator import JSONSchemaValidator
import jsonschema
import json


def to_model_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    return {
        'id': task.id,
        'number': task.number
    }


def from_model(model):
    get_or_none = lambda x: model[x] if x in model.keys() else None

    return Task(number=get_or_none('number'))


def does_task_exists(number):
    q = db.session.query(Task).filter_by(number=number)
    res = db.session.query(q.exists()).scalar()

    return res


app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'number': self.number,
        })


@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.session.query(Task).all()
    return jsonify(to_model_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.query(Task).get(task_id)
    if not task:
        abort(404)
    return jsonify(to_model(task))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'add')
def add_task():
    body = request.json

    task = from_model(body)
    task.id = None

    if does_task_exists(task.number):
        abort(409)

    db.session.add(task)
    db.session.commit()

    return jsonify({'id': task.id})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.session.query(Task).filter(Task.id == task_id).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({'id': task_id})


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error( e ):
    return Response(f'There was a validation error: {str(e)}', 400)


if __name__ == '__main__':
    app.run(debug=True)
