from models import Task
import hints_helpers


def to_models_list(tasks):
    return [to_model(t) for t in tasks]


def to_model(task):
    return {
        'id': task.id,
        'number': task.number,
        'hints': hints_helpers.to_models_list(task.hints)
    }


def from_model(model):
    get_or_none = lambda x: model[x] if x in model.keys() else None
    return Task(id=get_or_none('id'),
                number=get_or_none('number'))


def does_task_exists(session, number):
    q = session.query(Task).filter_by(number=number)
    res = session.query(q.exists()).scalar()

    return res