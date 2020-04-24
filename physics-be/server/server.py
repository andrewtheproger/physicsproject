import jsonschema
import uuid
import time
import os
import urllib.request
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from flask import Flask, jsonify, abort, request, Response
from flask_migrate import Migrate
from sqlalchemy import and_, or_
from flask_jsonschema_validator import JSONSchemaValidator
from flask_cors import CORS
from sqlalchemy.sql import text

from .models import db, Task, Hint, HintStatus, Image
from .config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from . import tasks_helpers
from . import hints_helpers

app = Flask(__name__)
JSONSchemaValidator(app=app, root="schemas")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_MIGRATE_REPO"] = SQLALCHEMY_MIGRATE_REPO

db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": "*", "allow_headers": "*", "max_age": 86400}})


# todo: extract to controller files

# helpers

@app.route('/api/health', methods=['GET'])
def health():
    return {'status': 'ok'}


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return Response(f'There was a request body validation error: {str(e)}', 400)


def get_query_parameters(request):
    get = lambda name, default, convert: convert(request.args.get(name)) if request.args.get(name) else default

    page = get('page', 0, int)
    count = get('count', 10, int)
    order = get('order', 'number', str)
    order_direction = get('order_direction', 'asc', str)

    allowed_properties = ['number']
    allowed_directions = ['asc', 'desc']

    if (page < 0) or \
        (count <= 0) or \
        (not order in allowed_properties) or \
        (not order_direction in allowed_directions):
        abort(400)

    return {
        'page': page + 1, #  due to flask counter starts from 1 but the common approach is to start from 0
        'count': count,
        'order': order,
        'order_direction': order_direction
    }


# tasks


@app.route('/api/images', methods=['POST'])
def upload_images():
    now = int(time.time() * 1000)  # ms
    ids = []

    print(request.form)

    for i in request.form:
        item = request.form[i]
        filename = uuid.uuid4().hex

        print(i)

        if 'links' in i:
            urllib.request.urlretrieve(item, filename)
        elif 'files' in i:
            item.save(filename)
        else:
            raise Exception(f'Unknown form filetype {i}')
    
        upload_result = upload(filename)
        thumbnail_url, options = cloudinary_url(upload_result['public_id'], format="png", crop="fit", width=200, height=200)
        os.remove(filename)

        image = Image(created_date=now,
            updated_date=now,
            url=upload_result['url'],
            thumbnail_url=thumbnail_url)

        db.session.add(image)
        db.session.commit()

        ids.append(image.id)


    return jsonify({
        'ids': ids
    })


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    query_parameters = get_query_parameters(request)
    filter_number = request.args.get('filter_by_number')
    tasks = db.session.query(Task)

    if filter_number:
        tasks = tasks.filter_by(number=filter_number)

    tasks = tasks \
            .order_by(text(f"{query_parameters['order']} {query_parameters['order_direction']}")) \
            .paginate(query_parameters['page'], query_parameters['count'], False) \
            .items
    return jsonify(tasks_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.query(Task).get(task_id)

    if not task:
        abort(404)

    return jsonify(tasks_helpers.to_model(task))


@app.route('/api/tasks', methods=['POST'])
@app.validate('task', 'upsert')
def upsert_task():
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
    task = db.session.query(Task).filter(Task.id == task_id).first()

    if not task:
        abort(404)

    db.session.delete(task)
    db.session.commit()

    return jsonify({'id': task_id})


# hints


@app.route('/api/tasks/<int:task_id>/hints', methods=['GET'])
def get_hints(task_id):
    tasks = db.session.query(Hint).filter_by(task_id=task_id).all()

    return jsonify(hints_helpers.to_models_list(tasks))


@app.route('/api/tasks/<int:task_id>/hints/<int:hint_id>', methods=['DELETE'])
def delete_hint(task_id, hint_id):
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
        hint.created_date = now
        hint.updated_date = now
        hint.status = HintStatus.pending

        db.session.add(hint)
    else:
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
    now = int(time.time() * 1000)  # ms
    db_hint = db.session.query(Hint).filter(Hint.id == hint_id).filter(Hint.status != HintStatus.declined).first()

    if db_hint is None:
        abort(404)

    db_hint.updated_date = now
    db_hint.status = HintStatus.declined

    db.session.commit()

    return jsonify({'id': hint_id})


if __name__ == '__main__':
    app.run(debug=True)
