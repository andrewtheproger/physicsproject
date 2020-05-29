import jsonschema
import uuid
import time
import requests
import os
import urllib.request
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import json

from flask import Flask, jsonify, abort, request, Response
from flask_restful import HTTPException
from flask_migrate import Migrate
from flask_jsonschema_validator import JSONSchemaValidator
from flask_cors import CORS
from sqlalchemy.sql import text

from .models import db, Task, Hint, HintStatus, Image, User
from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, DISCORD_WEBHOOK, \
    SECRET_JWT_KEY, SECURITY_PASSWORD_SALT
from . import tasks_helpers, hints_helpers, images_helpers, users_helpers

app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO
app.config['SECRET_JWT_KEY'] = SECRET_JWT_KEY
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ['GET', 'POST', 'DELETE'], "allow_headers": "*", "max_age": 86400}})

print(f'Using {SQLALCHEMY_DATABASE_URI}')


# todo: extract to controller files

# helpers


errors = {
    'developer': 1,
    'task_not_exists': 2,
    'task_alreay_exists': 3,
    'hint_not_exists': 4,
    'user_not_exists': 5,
    'user_already_exists': 6,
    'images_not_exists': 7,
    'user_password_is_wrong': 8,
    'unauthorized_access_requested': 9
}


@app.errorhandler(HTTPException)
def http_error(e):
    return jsonify({
        'message': str(e),
        'code': e.description
    }), e.code


def notify(msg):
    requests.post(DISCORD_WEBHOOK, data={'content': msg})


def get_user_from_request(request):
    bearer_token = request.headers.get('Authorization')

    if not bearer_token:
        return False

    bearer_value = bearer_token.split()[1]

    user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    return user;


def is_in_active_role(request, roles):
    user = get_user_from_request(request)

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


def get_query_parameters(request: object):
    get = lambda name, default, convert: convert(request.args.get(name)) if request.args.get(name) else default

    page = get('page', 0, int)
    count = get('count', 10, int)  # todo add count cap
    order = get('order', 'task_number', str)
    order_direction = get('order_direction', 'asc', str)

    allowed_properties = ['base_number', 'task_number']
    allowed_directions = ['asc', 'desc']

    if (page < 0) or \
            (count <= 0) or \
            (order not in allowed_properties) or \
            (order_direction not in allowed_directions):
        abort(400, errors['developer'])

    return {
        'page': page + 1,  # due to flask counter starts from 1 but the common approach is to start from 0
        'count': count,
        'order': order,
        'order_direction': order_direction
    }


# images


@app.route('/api/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = db.session.query(Image).get(image_id)

    if not image:
        abort(404, errors['developer'])

    return jsonify(images_helpers.to_model(image))


@app.route('/api/images', methods=['POST'])
def upload_images():
    now = int(time.time() * 1000)  # ms
    ids = []

    filename = uuid.uuid4().hex

    for i in request.form:
        if 'links' in i:
            item = request.form[i]
            urllib.request.urlretrieve(item, filename)
        else:
            raise Exception(f'Unknown form filetype {i}')

        upload_result = upload(filename)
        thumbnail_url, options = cloudinary_url(upload_result['public_id'],
                                                format="png", crop="fit",
                                                width=200, height=200)
        os.remove(filename)

        image = Image(created_date=now,
                      updated_date=now,
                      url=upload_result['url'],
                      thumbnail_url=thumbnail_url)

        db.session.add(image)
        db.session.commit()

        ids.append(image.id)

    for i in request.files:
        if 'files' in i:
            item = request.files[i]
            item.save(filename)
        else:
            raise Exception(f'Unknown form filetype {i}')

        upload_result = upload(filename)
        thumbnail_url, options = cloudinary_url(upload_result['public_id'],
                                                format="png", crop="fit",
                                                width=200, height=200)
        os.remove(filename)

        image = Image(created_date=now,
                      updated_date=now,
                      url=upload_result['url'],
                      thumbnail_url=thumbnail_url)

        db.session.add(image)
        db.session.commit()

        ids.append(image.id)

    notify(f'Added images {ids} to 3800 be')

    return jsonify({
        'ids': ids
    })


# tasks


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    query_parameters = get_query_parameters(request)
    filter_base_number = request.args.get('filter_by_base_number')
    filter_task_number = request.args.get('filter_by_task_number')
    tasks = db.session.query(Task) \
        .outerjoin(Image, Task.id == Image.task_id)
    # .add_columns()

    if filter_base_number:
        tasks = tasks.filter(Task.base_number == filter_base_number)

    if filter_task_number:
        tasks = tasks.filter(Task.task_number == filter_task_number)

    tasks = tasks \
        .order_by(text(f"{query_parameters['order']} {query_parameters['order_direction']}")) \
        .paginate(query_parameters['page'], query_parameters['count'], False) \
        .items

    return jsonify(tasks_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.query(Task) \
        .outerjoin(Image, Task.id == Image.task_id) \
        .filter(Task.id == task_id) \
        .first()

    if not task:
        abort(404, errors['task_not_exists'])

    return jsonify(tasks_helpers.to_model(task))


@app.route('/api/tasks/predicate_numbers', methods=['GET'])
def predicate_tasks_number():
    tasks = db.session.query(Task).with_entities(Task.id, Task.base_number, Task.task_number) \
        .order_by(Task.base_number, Task.task_number) \
        .all()

    if not tasks:
        return jsonify([])

    return jsonify(tasks_helpers.to_predicate_models_list(tasks))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'upsert')
def upsert_task():
    if not is_in_active_role(request, ['user', 'admin']):
        abort(403, errors['unauthorized_access_requested'])

    body = request.json

    try:
        task = tasks_helpers.from_model(body)
    except Exception as e:
        abort(400, errors['developer'])

    should_insert = task.id is None
    now = int(time.time() * 1000)  # ms
    user = get_user_from_request(request)

    if should_insert:
        if tasks_helpers.does_task_exists(db.session, task.base_number, task.task_number):
            abort(409, errors['task_alreay_exists'])

        task.created_date = now
        task.updated_date = now
        task.creator = user.id

        db.session.add(task)

        image_ids = json.loads(task.image_ids_json)
        for image_id in image_ids:
            image = db.session.query(Image).filter_by(id=image_id).first()

            if not image:
                abort(404, errors['images_not_exists'])

            image.task_id = task.id

    else:
        db_task = db.session.query(Task).filter_by(id=task.id).first()

        if db_task is None:
            abort(404, errors['task_not_exists'])

        db_task.updated_date = now

        if task.base_number:
            db_task.base_number = task.base_number

        if task.task_number:
            db_task.task_number = task.task_number

        if task.latex:
            db_task.latex = task.latex

        if task.image_ids_json:
            db_task.image_ids_json = task.image_ids_json

    db.session.commit()

    notify(f'Upsert task {tasks_helpers.to_model(task)} to 3800 be')

    return jsonify({'id': task.id})


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    task = db.session.query(Task).filter(Task.id == task_id).first()

    if not task:
        abort(404, errors['task_not_exists'])

    notify(f'Deleted task {tasks_helpers.to_model(task)} from 3800 be')

    db.session.delete(task)
    db.session.commit()

    return jsonify({'id': task_id})


# hints


@app.route('/api/tasks/<int:task_id>/hints', methods=['GET'])
def get_hints(task_id):
    if not is_in_active_role(request, ['user', 'admin']):
        abort(403, errors['unauthorized_access_requested'])

    tasks = db.session.query(Hint).filter_by(task_id=task_id).all()

    return jsonify(hints_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>', methods=['DELETE'])
def delete_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

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
            abort(403, errors['unauthorized_access_requested'])

        hint.created_date = now
        hint.updated_date = now
        hint.status = HintStatus.pending

        db.session.add(hint)
    else:
        if not is_in_active_role(request, ['admin']):
            abort(403, errors['unauthorized_access_requested'])

        db_hint = db.session.query(Hint).filter_by(id=hint.id).first()

        if db_hint is None:
            abort(404, errors['hint_not_exists'])

        db_hint.updated_date = now

        if hint.task_id:
            db_hint.task_id = hint.task_id

        if hint.latex:
            db_hint.latex = hint.latex

        if hint.image_ids_json:
            db_hint.image_ids_json = hint.image_ids_json

        if hint.status:
            db_hint.status = hint.status

    db.session.commit()

    return jsonify({'id': hint.id})


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>/approve', methods=['POST'])
def enable_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    now = int(time.time() * 1000)  # ms
    db_hint = db.session.query(Hint).filter(Hint.id == hint_id).filter(Hint.status != HintStatus.approved).first()

    if db_hint is None:
        abort(404, errors['hint_not_exists'])

    db_hint.updated_date = now
    db_hint.status = HintStatus.approved

    db.session.commit()

    return jsonify({'id': hint_id})


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>/decline', methods=['POST'])
def disable_hint(task_id, hint_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    now = int(time.time() * 1000)  # ms
    db_hint = db.session.query(Hint).filter(Hint.id == hint_id).filter(Hint.status != HintStatus.declined).first()

    if db_hint is None:
        abort(404, errors['hint_not_exists'])

    db_hint.updated_date = now
    db_hint.status = HintStatus.declined

    db.session.commit()

    return jsonify({'id': hint_id})


# users


@app.route('/api/users', methods=['GET'])
def get_users():
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    filter_email = request.args.get('filter_by_email')

    if filter_email:
        users = db.session.query(User).filter_by(email=filter_email).all()
        return jsonify(users_helpers.to_models_list(users))

    users = db.session.query(User).all()
    return jsonify(users_helpers.to_models_list(users, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/<int:user_id>', methods=['POST'])
@app.validate('user', 'update')
def update_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    body = request.json
    user, _ = users_helpers.from_register_model(body)
    db_user = db.session.query(User).filter_by(id=user_id).first()

    if db_user is None:
        abort(404)

    if user.email:
        db_user.email = user.email

    if user.role:
        db_user.role = user.role

    if user.color_background_primary:
        db_user.color_background_primary = user.color_background_primary

    if user.color_background_secondary:
        db_user.color_background_secondary = user.color_background_secondary

    if user.color_background_action:
        db_user.color_background_action = user.color_background_action

    if user.color_foreground_primary:
        db_user.color_foreground_primary = user.color_foreground_primary

    if user.color_foreground_secondary:
        db_user.color_foreground_secondary = user.color_foreground_secondary

    if user.color_foreground_action:
        db_user.color_foreground_action = user.color_foreground_action

    db.session.commit()

    return jsonify({'id': db_user.id})


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    db_user = db.session.query(User).filter_by(id=user_id).first()

    if db_user is None:
        abort(404)

    return jsonify(users_helpers.to_model(db_user, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/me', methods=['GET'])
def get_me():
    bearer_token = request.headers.get('Authorization')

    if not bearer_token:
        abort(403, errors['unauthorized_access_requested'])

    bearer_value = bearer_token.split()[1]
    db_user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    if db_user is None:
        return jsonify({})

    return jsonify(users_helpers.to_model(db_user, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/me', methods=['POST'])
def update_me():
    bearer_token = request.headers.get('Authorization')

    if not bearer_token:
        abort(403, errors['unauthorized_access_requested'])

    body = request.json
    user, _ = users_helpers.from_register_model(body)
    bearer_value = bearer_token.split()[1]
    db_user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    if db_user is None:
        return jsonify({})

    if user.email:
        db_user.email = user.email

    if user.role:
        db_user.role = user.role

    if user.color_background_primary:
        db_user.color_background_primary = user.color_background_primary

    if user.color_background_secondary:
        db_user.color_background_secondary = user.color_background_secondary

    if user.color_background_action:
        db_user.color_background_action = user.color_background_action

    if user.color_foreground_primary:
        db_user.color_foreground_primary = user.color_foreground_primary

    if user.color_foreground_secondary:
        db_user.color_foreground_secondary = user.color_foreground_secondary

    if user.color_foreground_action:
        db_user.color_foreground_action = user.color_foreground_action

    db.session.commit()

    return jsonify(users_helpers.to_model(db_user, app.config['SECRET_JWT_KEY']))


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not is_in_active_role(request, ['admin']):
        abort(403, errors['unauthorized_access_requested'])

    db.session.query(User).filter(User.id == user_id).delete(synchronize_session=False)
    db.session.commit()

    return jsonify({'id': user_id})


@app.route('/api/users/register', methods=['POST'])
@app.validate('user', 'register')
def register_user():
    body = request.json
    user, password = users_helpers.from_register_model(body)

    now = int(time.time() * 1000)  # ms

    if users_helpers.does_email_exists(db.session, user.email):
        abort(409, errors['user_already_exists'])

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

    user = db.session.query(User).filter_by(email=user.email).first()

    if user is None:
        abort(404, errors['user_not_exists'])

    if not user.check_password(password):
        abort(403, errors['user_password_is_wrong'])

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

    if not bearer_token:
        abort(403)

    bearer_value = bearer_token.split()[1]
    now = int(time.time() * 1000)  # ms

    db_user = db.session.query(User).filter_by(auth_token=f'{bearer_value}').first()

    if db_user is None:
        return abort(404, errors['user_not_exists'])

    db_user.auth_token = None
    db_user.updated_date = now
    db.session.commit()

    return jsonify({'id': db_user.id})


if __name__ == '__main__':
    app.run(debug=True)
