import jsonschema
import time

from flask import Flask, jsonify, abort, request, Response
from flask_migrate import Migrate
from sqlalchemy import and_, or_
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, SECRET_JWT_KEY, SECURITY_PASSWORD_SALT
from flask_jsonschema_validator import JSONSchemaValidator
from flask_security.utils import hash_password
from flask_security import Security, SQLAlchemyUserDatastore

from models import db, Task, Hint, HintStatus, User
import tasks_helpers, hints_helpers, users_helpers

app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO
app.config['SECRET_JWT_KEY'] = SECRET_JWT_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

db.init_app(app)
migrate = Migrate(app, db)

# todo: extract to controller files

# helpers


def is_in_active_role(request, roles):
    bearer_token = request.headers.get('Authorization')
    bearer_value = bearer_token.split()[1]

    user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    if user is None:
        return False

    if users_helpers.check_is_token_expired(user, app.config['SECRET_JWT_KEY']):
        return False

    return user.role.value in roles


@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return Response(f'There was a request body validation error: {str(e)}', 400)


# tasks


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if not is_in_active_role(request, ['user', 'admin']):
        abort(403)

    filter_number = request.args.get('filter_by_number')

    if filter_number:
        tasks = db.session.query(Task).filter_by(number=filter_number).all()
        return jsonify(tasks_helpers.to_models_list(tasks))

    tasks = db.session.query(Task).all()
    return jsonify(tasks_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if not is_in_active_role(request, ['user', 'admin']):
        abort(403)

    task = db.session.query(Task).get(task_id)

    if not task:
        abort(404)

    return jsonify(tasks_helpers.to_model(task))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'upsert')
def upsert_task():
    if not is_in_active_role(request, ['admin']):
        abort(403)

    body = request.json
    task = tasks_helpers.from_model(body)
    should_insert = task.id is None
    now = int(time.time() * 1000)  # ms

    if should_insert:
        if tasks_helpers.does_task_exists(db.session, task.number):
            abort(409)

        task.created_date = now
        task.updated_date = now

        db.session.add(task)
    else:
        db_task = db.session.query(Task).filter_by(id=task.id).first()

        if db_task is None:
            abort(404)

        db_task.updated_date = now

        if task.number:
            db_task.number = task.number

        if task.latex:
            db_task.latex = task.latex

        if task.image_hrefs_json:
            db_task.image_hrefs_json = task.image_hrefs_json

    db.session.commit()

    return jsonify({'id': task.id})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    db.session.query(Task).filter(Task.id == task_id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'id': task_id})


# hints


@app.route('/api/tasks/<int:task_id>/hints', methods=['GET'])
def get_hints(task_id):
    if not is_in_active_role(request, ['user', 'admin']):
        abort(403)

    tasks = db.session.query(Hint).filter_by(task_id=task_id).all()

    return jsonify(hints_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>', methods=['DELETE'])
def delete_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    db.session.query(Hint).filter(Hint.id == hint_id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'id': hint_id})


@app.route('/api/tasks/<int:task_id>/hints', methods=['POST'])
@app.validate('hint', 'upsert')
def upsert_hint(task_id):
    body = request.json
    hint = hints_helpers.from_model(body, task_id)
    should_insert = hint.id is None

    now = int(time.time() * 1000)  # ms

    if should_insert:
        if not is_in_active_role(request, ['user', 'admin']):
            abort(403)

        hint.created_date = now
        hint.updated_date = now
        hint.status = HintStatus.pending

        db.session.add(hint)
    else:
        if not is_in_active_role(request, ['admin']):
            abort(403)

        db_hint = db.session.query(Hint).filter_by(id=hint.id).first()

        if db_hint is None:
            abort(404)

        db_hint.updated_date = now

        if hint.task_id:
            db_hint.task_id = hint.task_id

        if hint.latex:
            db_hint.latex = hint.latex

        if hint.image_hrefs_json:
            db_hint.image_hrefs_json = hint.image_hrefs_json

        if hint.status:
            db_hint.status = hint.status

    db.session.commit()

    return jsonify({'id': hint.id})


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>/approve', methods=['POST'])
def enable_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    now = int(time.time() * 1000)  # ms
    db_hint = db.session.query(Hint).filter(Hint.id == hint_id).filter(Hint.status != HintStatus.approved).first()

    if db_hint is None:
        abort(404)

    db_hint.updated_date = now
    db_hint.status = HintStatus.approved

    db.session.commit()

    return jsonify({'id': hint_id})


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>/decline', methods=['POST'])
def disable_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    now = int(time.time() * 1000)  # ms
    db_hint = db.session.query(Hint).filter(Hint.id == hint_id).filter(Hint.status != HintStatus.declined).first()

    if db_hint is None:
        abort(404)

    db_hint.updated_date = now
    db_hint.status = HintStatus.declined

    db.session.commit()

    return jsonify({'id': hint_id})


# users


@app.route('/api/users', methods=['GET'])
def get_users():
    if not is_in_active_role(request, ['admin']):
        abort(403)

    filter_login = request.args.get('filter_by_login')

    if filter_login:
        users = db.session.query(User).filter_by(login=filter_login).all()
        return jsonify(users_helpers.to_models_list(users))

    users = db.session.query(User).all()
    return jsonify(users_helpers.to_models_list(users, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/<int:user_id>', methods=['POST'])
@app.validate('user', 'update')
def update_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    body = request.json
    user, _ = users_helpers.from_register_model(body)
    db_user = db.session.query(User).filter_by(id=user_id).first()

    if db_user is None:
        abort(404)

    if user.login:
        db_user.login = user.login

    if user.role:
        db_user.role = user.role

    db.session.commit()

    return jsonify({'id': db_user.id})


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    db_user = db.session.query(User).filter_by(id=user_id).first()

    if db_user is None:
        abort(404)

    return jsonify(users_helpers.to_model(db_user, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403)

    db.session.query(User).filter(User.id == user_id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'id': user_id})


@app.route('/api/users/register', methods=['POST'])
@app.validate('user', 'register')
def register_user():
    body = request.json
    user, password = users_helpers.from_register_model(body)

    now = int(time.time() * 1000)  # ms

    if users_helpers.does_login_exists(db.session, user.login):
        abort(409)

    user.auth_token = user.encode_auth_token(user.id, app.config['SECRET_JWT_KEY']).decode()
    user.created_date = now
    user.updated_date = now
    user.role = 'user'
    user.set_password_hash(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'token': user.auth_token
    })


@app.route('/api/users/login', methods=['POST'])
@app.validate('user', 'register')
def login():
    body = request.json
    user, password = users_helpers.from_register_model(body)
    now = int(time.time() * 1000)  # ms

    user = db.session.query(User).filter_by(login=user.login).first()

    if user is None:
        abort(404)

    if not user.check_password(password):
        abort(403)

    auth_token = user.encode_auth_token(user.id, app.config['SECRET_JWT_KEY']).decode()
    user.auth_token = auth_token  # todo add last login time and ip
    user.updated_date = now
    db.session.commit()

    return jsonify({
        'id': user.id,
        'token': auth_token
    })


@app.route('/api/users/logout', methods=['POST'])
def logout():
    bearer_token = request.headers.get('Authorization')
    bearer_value = bearer_token.split()[1]
    now = int(time.time() * 1000)  # ms

    db_user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    if db_user is None:
        return abort(404)

    db_user.auth_token = None
    db_user.updated_date = now
    db.session.commit()

    return jsonify({'id': db_user.id})


if __name__ == '__main__':
    app.run(debug=True)
