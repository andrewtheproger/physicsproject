from models import Task
import hints_helpers
import json


def to_models_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    return {
        'id': task.id,
        'created_date': task.created_date,
        'updated_date': task.updated_date,
        'number': task.number,
        'body': {
            'latex': task.latex,
            'image_hrefs': json.loads(task.image_hrefs_json)
        },
        'hints': hints_helpers.to_models_list(task.hints)
    }


def from_model(model):
    get_or_none = lambda item, key: item[key] if key in item.keys() else None

    id = get_or_none(model, 'id')
    created_date = get_or_none(model, 'created_date')
    updated_date = get_or_none(model, 'updated_date')
    number = get_or_none(model, 'number')
    body = get_or_none(model, 'body')
    latex = get_or_none(body, 'latex')
    hrefs = get_or_none(body, 'image_hrefs')

    return Task(id=id,
                created_date=created_date,
                updated_date=updated_date,
                number=number,
                latex=latex,
                image_hrefs_json=json.dumps(hrefs))


def does_task_exists(session, number):
    q = session.query(Task).filter_by(number=number)
    res = session.query(q.exists()).scalar()

    return res
