from models import Suggestion


def to_models_list(suggestions):
    return [to_model(s) for s in suggestions]


def to_model(suggestion):
    return {
        'id': suggestion.id,
        'hint_id': suggestion.hint_id
    }


def from_model(model, hint_id):
    get_or_none = lambda x: model[x] if x in model.keys() else None
    return Suggestion(id=get_or_none('id'),
                      hint_id=hint_id)
