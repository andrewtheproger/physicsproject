import jsonschema

from flask import Flask, jsonify, abort, request, Response
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from flask_jsonschema_validator import JSONSchemaValidator

from models import db, Task
import helpers

app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.session.query(Task).all()

    return jsonify(helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.query(Task).get(task_id)

    if not task:
        abort(404)

    return jsonify(helpers.to_model(task))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'upsert')
def upsert_task():
    body = request.json
    task = helpers.from_model(body)
    should_insert = task.id is None

    if should_insert:
        if helpers.does_task_exists(db.session, task.number):
            abort(409)

        db.session.add(task)
    else:
        db_task = db.session.query(Task).filter_by(id=task.id).first()

        if db_task is None:
            abort(404)

        db_task.number = task.number

    db.session.commit()

    return jsonify({'id': task.id})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.session.query(Task).filter(Task.id == task_id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'id': task_id})


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return Response(f'There was a request body validation error: {str(e)}', 400)


if __name__ == '__main__':
    app.run(debug=True)
