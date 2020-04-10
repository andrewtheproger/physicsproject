from models import Hint


def to_models_list(hints):
    return [to_model(h) for h in hints]


def to_model(hint):
    return {
        'id': hint.id,
        'task_id': hint.task_id
    }


def from_model(model, task_id):
    get_or_none = lambda x: model[x] if x in model.keys() else None
    return Hint(id=get_or_none('id'),
                task_id=task_id)
