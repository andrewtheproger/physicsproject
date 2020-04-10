from flask import Flask, jsonify, abort, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from flask_jsonschema_validator import JSONSchemaValidator
import jsonschema


def to_model_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    return {
        'id': task.id,
        'number': task.number
    }


def from_model(model):
    get_or_none = lambda x: model[x] if x in model.keys() else None

    return Tasks(number=get_or_none('number'))


app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(16))

    def __repr__(self):
        return '<User %r>' % self.number


@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Tasks.query.all()
    return jsonify(to_model_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.get(task_id)
    if not task:
        abort(404)
    return jsonify(to_model(task))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'add')
def add_task():
    body = request.json

    print(type(body))

    task = from_model(body)

    db.session.add(task)
    db.session.commit()

    return jsonify({})


@app.errorhandler( jsonschema.ValidationError )
def on_validation_error( e ):
    return Response(f'There was a validation error: {str(e)}', 400)


if __name__ == '__main__':
    app.run(debug=True)
