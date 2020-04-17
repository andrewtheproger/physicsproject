from models import Hint
import json


def to_models_list(hints):
    return [to_model(h) for h in hints]


def to_model(hint):
    return {
        'id': hint.id,
        'created_date': hint.created_date,
        'updated_date': hint.updated_date,
        'task_id': hint.task_id,
        'status': hint.status.value,
        'body': {
            'latex': hint.latex,
            'image_hrefs': json.loads(hint.image_hrefs_json)
        }
    }


def from_model(model, task_id):
    get_or_none = lambda item, key: item[key] if key in item.keys() else None

    id = get_or_none(model, 'id')
    created_date = get_or_none(model, 'created_date')
    updated_date = get_or_none(model, 'updated_date')
    status = get_or_none(model, 'status')
    body = get_or_none(model, 'body')
    latex = get_or_none(body, 'latex')
    hrefs = get_or_none(body, 'image_hrefs')

    return Hint(id=id,
                created_date=created_date,
                updated_date=updated_date,
                task_id=task_id,
                status=status,
                latex=latex,
                image_hrefs_json=json.dumps(hrefs))
