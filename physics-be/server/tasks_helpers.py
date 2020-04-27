from .models import Task
from . import hints_helpers
import json


def to_predicate_models_list(tasks):
    return [to_predicate_model(t) for t in tasks]


def to_predicate_model(task):
    return {
        'id': task.id,
        'base_number': task.base_number,
        'task_number': task.task_number
    }

def to_models_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    to_view = lambda i: {
        'id': i.id,
        'url': i.url
    }

    return {
        'id': task.id,
        'created_date': task.created_date,
        'updated_date': task.updated_date,
        'base_number': task.base_number,
        'task_number': task.task_number,
        'body': {
            'latex': task.latex,
            'images': [to_view(i) for i in task.images]
        },
        'hints': hints_helpers.to_models_list(task.hints)
    }


def from_model(model):
    get_or_none = lambda item, key: item[key] if key in item.keys() else None

    id = get_or_none(model, 'id')
    created_date = get_or_none(model, 'created_date')
    updated_date = get_or_none(model, 'updated_date')
    base_number = get_or_none(model, 'base_number')
    task_number = get_or_none(model, 'task_number')
    body = get_or_none(model, 'body')
    latex = get_or_none(body, 'latex')
    image_ids = get_or_none(body, 'image_ids')

    return Task(id=id,
                created_date=created_date,
                updated_date=updated_date,
                base_number=base_number,
                task_number=task_number,
                latex=latex,
                image_ids_json=json.dumps(image_ids))


def does_task_exists(session, base_number, task_number):
    q = session.query(Task).filter_by(base_number=base_number).filter_by(task_number=task_number)
    res = session.query(q.exists()).scalar()

    return res
